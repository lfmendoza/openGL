import pygame
from pygame.locals import *

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from gl import Renderer
from model import Model
from shaders import *

width = 1440
height = 1024

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

skyboxTexture = [
    "textures/skybox2/skyrender0001.bmp",
    "textures/skybox2/skyrender0003.bmp",
    "textures/skybox2/skyrender0005.bmp",
    "textures/skybox2/skyrender0006.bmp",
    "textures/skybox2/skyrender0004.bmp",
    "textures/skybox2/skyrender0002.bmp"
]

rend.createSkybox(skyboxTexture)

cat = Model("models/cat.obj")
cat.AddTexture("textures/cat.bmp")
cat.translation.z = 0
cat.translation.x = 0
cat.rotation.y = 180


woman = Model("models/girl.obj")
woman.translation.z = 2
woman.translation.x = 0
woman.rotation.y = 180

spider = Model("models/spider.obj")
spider.translation.z = -5
spider.translation.x = -3
spider.rotation.y = 180
spider.scale.x = 0.03
spider.scale.y = 0.03
spider.scale.z = 0.03

alien = Model("models/alien.obj")
alien.translation.z = -5
alien.translation.x = 3
alien.rotation.y = -45
alien.scale.x = 0.15
alien.scale.y = 0.15
alien.scale.z = 0.15

rend.scene.append(cat)
rend.scene.append(woman)
rend.scene.append(spider)
rend.scene.append(alien)
rend.scene.append(perro)


vShader = vertex_shader_default
fShader = fragment_shader_default

cam_distance = 5
cam_angle = 0
cam_height = 0

max_cam_height = 5
min_cam_height = -5
max_cam_distance = 15
min_cam_distance = 2

modelIndex = 0

rend.SetShaders(vShader, fShader)

isRunning = True
while isRunning:

    deltaTime = clock.tick(60) / 1000

    keys = pygame.key.get_pressed()
    mouseVel = pygame.mouse.get_rel()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.MOUSEWHEEL:

            if event.y < 0 and cam_distance < 10:
                cam_distance -= event.y * deltaTime * 10

            if event.y > 0 and cam_distance > 2:
                cam_distance -= event.y * deltaTime * 10
				
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:
                modelIndex += 1
                modelIndex %= len(rend.scene)
                for i in range(len(rend.scene)):
                    rend.scene[i].visible = i == modelIndex

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

            # Vertex Shaders
            elif event.key == pygame.K_1:
                vShader = vertex_shader_default
                rend.SetShaders(vShader, fShader)

            elif event.key == pygame.K_2:
                vShader = vertex_shader_wave
                rend.SetShaders(vShader, fShader)

            elif event.key == pygame.K_3:
                vShader = vertex_shader_twist
                rend.SetShaders(vShader, fShader)

            # Fragment Shaders
            elif event.key == pygame.K_4:
                fShader = fragment_shader_default
                rend.SetShaders(vShader, fShader)

            elif event.key == pygame.K_5:
                fShader = fragment_shader_grayscale
                rend.SetShaders(vShader, fShader)

            elif event.key == pygame.K_6:
                fShader = fragment_shader_inversion
                rend.SetShaders(vShader, fShader)

            elif event.key == pygame.K_7:
                rend.FilledMode()

            elif event.key == pygame.K_8:
                rend.WireframeMode()

    # Movimiento de la luz
    if keys[K_LEFT]:
        rend.pointLight.x -= 1 * deltaTime

    if keys[K_RIGHT]:
        rend.pointLight.x += 1 * deltaTime

    if keys[K_UP]:
        rend.pointLight.z -= 1 * deltaTime

    if keys[K_DOWN]:
        rend.pointLight.z += 1 * deltaTime

    # Movimiento de camara hacia arriba y abajo con limite
    if keys[K_a]:
        cam_angle -= 50 * deltaTime

    if keys[K_d]:
        cam_angle += 50 * deltaTime

    if keys[K_w]:
        cam_height += 5 * deltaTime
        cam_height = min(cam_height, max_cam_height)

    if keys[K_s]:
        cam_height -= 5 * deltaTime
        cam_height = max(cam_height, min_cam_height)

    # Zoom In y Zoom Out con limite
    if keys[K_q]:
        cam_distance -= 5 * deltaTime
        cam_distance = max(cam_distance, min_cam_distance)

    if keys[K_e]:
        cam_distance += 5 * deltaTime
        cam_distance = min(cam_distance, max_cam_distance)

    if pygame.mouse.get_pressed()[0]:
        cam_angle -= mouseVel[0] * deltaTime * 5
		
        if mouseVel[1] > 0 and rend.camera.position.y < 2:
            rend.camera.position.y += mouseVel[1] * deltaTime
			
        if mouseVel[1] < 0 and rend.camera.position.y > -2:
            rend.camera.position.y += mouseVel[1] * deltaTime
				
    rend.camera.Orbit( cat.translation, cam_distance, cam_angle)
    rend.camera.LookAt( cat.translation )

    rend.Render()

    rend.time += deltaTime
    pygame.display.flip()

pygame.quit()
