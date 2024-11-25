
# Vertex Shaders
vertex_shader_default = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    outPosition = modelMatrix * vec4(position, 1.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

vertex_shader_wave = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normal;
layout (location = 3) in vec3 tangent;

out vec2 outTexCoords;
out vec4 outPosition;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float wave = sin(position.x * 2.0 + time) * 0.1 + cos(position.z * 2.0 + time) * 0.1;
    vec3 displacedPosition = position + normal * wave;
    outPosition = modelMatrix * vec4(displacedPosition, 1.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;

    outTexCoords = texCoords;
    outNormals = mat3(modelMatrix) * normal;
}
'''

vertex_shader_twist = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float angle = position.y * 5.0;
    float s = sin(angle);
    float c = cos(angle);
    mat4 twistMatrix = mat4(
        c, 0.0, -s, 0.0,
        0.0, 1.0, 0.0, 0.0,
        s, 0.0, c, 0.0,
        0.0, 0.0, 0.0, 1.0
    );
    outPosition = modelMatrix * twistMatrix * vec4(position, 1.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

vertex_shader_fire = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normal;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float offset = sin(position.y * 3.0 + time * 5.0) * 0.1;
    vec3 animatedPosition = position + normal * offset;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(animatedPosition, 1.0);

    outTexCoords = texCoords;
    outNormals = mat3(modelMatrix) * normal;
}
'''

vertex_shader_hologram = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;

out vec2 outTexCoords;
out vec3 outColorShift;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float flicker = sin(time * 10.0) * 0.05;
    vec3 displacedPosition = position + vec3(0.0, flicker, 0.0);
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(displacedPosition, 1.0);

    outTexCoords = texCoords;
    outColorShift = vec3(sin(time * 5.0), cos(time * 5.0), sin(time * 2.0));
}

'''

vertex_shader_ripple = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;

out vec2 outTexCoords;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float distance = length(position.xz);
    float ripple = sin(distance * 10.0 - time * 5.0) * 0.05;
    vec3 displacedPosition = position + vec3(0.0, ripple, 0.0);
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(displacedPosition, 1.0);

    outTexCoords = texCoords;
}
'''

vertex_shader_explosion = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normal;

out vec2 outTexCoords;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float expansion = time * 0.5;
    vec3 explodedPosition = position + normalize(position) * expansion;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(explodedPosition, 1.0);

    outTexCoords = texCoords;
}
'''

# Fragment Shaders
fragment_shader_default = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec4 outPosition;

uniform sampler2D tex;
uniform vec3 pointLight;

out vec4 fragColor;

void main()
{
    vec3 lightDir = normalize(pointLight - outPosition.xyz);
    float intensity = max(dot(outNormals, lightDir), 0.0);
    vec4 color = texture(tex, outTexCoords);
    fragColor = color * intensity;
}
'''

fragment_shader_grayscale = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec4 outPosition;

uniform sampler2D tex;
uniform vec3 pointLight;

out vec4 fragColor;

void main()
{
    vec3 lightDir = normalize(pointLight - outPosition.xyz);
    float intensity = max(dot(outNormals, lightDir), 0.0);
    vec4 color = texture(tex, outTexCoords);
    float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
    fragColor = vec4(vec3(gray * intensity), color.a);
}
'''

fragment_shader_inversion = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec4 outPosition;

uniform sampler2D tex;
uniform vec3 pointLight;

out vec4 fragColor;

void main()
{
    vec3 lightDir = normalize(pointLight - outPosition.xyz);
    float intensity = max(dot(outNormals, lightDir), 0.0);
    vec4 color = texture(tex, outTexCoords);
    fragColor = vec4((1.0 - color.rgb) * intensity, color.a);
}
'''

fragment_shader_glowing = '''
#version 450 core

in vec2 outTexCoords;

uniform sampler2D tex0;
uniform vec3 glowColor;

out vec4 fragColor;

void main()
{
    vec4 baseColor = texture(tex0, outTexCoords);
    fragColor = baseColor + vec4(glowColor, 1.0) * 0.5;
}

'''

fragment_shader_distorion = '''
#version 450 core

in vec2 outTexCoords;

uniform sampler2D tex0;
uniform float time;

out vec4 fragColor;

void main()
{
    vec2 distortedTexCoords = outTexCoords + sin(outTexCoords.yx * 10.0 + time) * 0.05;
    fragColor = texture(tex0, distortedTexCoords);
}
'''

fragment_shader_pixelation = '''
#version 450 core

in vec2 outTexCoords;

uniform sampler2D tex0;
uniform vec2 resolution;
uniform float pixelSize;

out vec4 fragColor;

void main()
{
    vec2 pixelatedCoords = floor(outTexCoords * resolution / pixelSize) * pixelSize / resolution;
    fragColor = texture(tex0, pixelatedCoords);
}
'''

fragment_shader_fire = '''
#version 450 core

in vec2 outTexCoords;

uniform float time;

out vec4 fragColor;

void main()
{
    float fire = sin(outTexCoords.y * 10.0 + time * 5.0) * 0.5 + 0.5;
    fragColor = vec4(1.0, fire, 0.0, 1.0);
}
'''

fragment_shader_chromatic_aberration = '''
#version 450 core

in vec2 outTexCoords;

uniform sampler2D tex0;

out vec4 fragColor;

void main()
{
    float offset = 0.01;
    vec4 red = texture(tex0, outTexCoords + vec2(-offset, 0.0));
    vec4 green = texture(tex0, outTexCoords);
    vec4 blue = texture(tex0, outTexCoords + vec2(offset, 0.0));

    fragColor = vec4(red.r, green.g, blue.b, 1.0);
}
'''