import glm
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

rend.createSkybox(skyboxTexture, skybox_vertex_shader, skybox_fragment_shader)

# Cargar un modelo OBJ diferente
model = Model("models/cat.obj")
model.AddTexture("textures/cat.bmp")
model.translation.z = 0
model.scale = glm.vec3(1, 1, 1)

rend.scene.append(model)

vertex_shaders = [vertex_shader_default, vertex_shader_wave, vertex_shader_twist]
fragment_shaders = [fragment_shader_default, fragment_shader_grayscale, fragment_shader_inversion]

current_vertex_shader = vertex_shaders[0]
current_fragment_shader = fragment_shaders[0]

# Variables para los movimientos de cámara
cam_distance = 5
cam_angle = 0
cam_height = 0

max_cam_height = 5
min_cam_height = -5
max_cam_distance = 15
min_cam_distance = 2

rend.SetShaders(current_vertex_shader, current_fragment_shader)

isRunning = True
while isRunning:

    deltaTime = clock.tick(60) / 1000

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_1:
                current_vertex_shader = vertex_shaders[0]
                rend.SetShaders(current_vertex_shader, current_fragment_shader)
            elif event.key == pygame.K_2:
                current_vertex_shader = vertex_shaders[1]
                rend.SetShaders(current_vertex_shader, current_fragment_shader)
            elif event.key == pygame.K_3:
                current_vertex_shader = vertex_shaders[2]
                rend.SetShaders(current_vertex_shader, current_fragment_shader)
            elif event.key == pygame.K_4:
                current_fragment_shader = fragment_shaders[0]
                rend.SetShaders(current_vertex_shader, current_fragment_shader)
            elif event.key == pygame.K_5:
                current_fragment_shader = fragment_shaders[1]
                rend.SetShaders(current_vertex_shader, current_fragment_shader)
            elif event.key == pygame.K_6:
                current_fragment_shader = fragment_shaders[2]
                rend.SetShaders(current_vertex_shader, current_fragment_shader)
            elif event.key == pygame.K_7:
                rend.FilledMode()
            elif event.key == pygame.K_8:
                rend.WireframeMode()

    # Movimiento circular alrededor del modelo
    if keys[K_LEFT]:
        cam_angle -= 50 * deltaTime
    if keys[K_RIGHT]:
        cam_angle += 50 * deltaTime

    # Movimiento de cámara hacia arriba y abajo con límite
    if keys[K_UP]:
        cam_height += 5 * deltaTime
        cam_height = min(cam_height, max_cam_height)
    if keys[K_DOWN]:
        cam_height -= 5 * deltaTime
        cam_height = max(cam_height, min_cam_height)

    # Zoom In y Zoom Out con límite
    if keys[K_q]:
        cam_distance -= 5 * deltaTime
        cam_distance = max(cam_distance, min_cam_distance)
    if keys[K_e]:
        cam_distance += 5 * deltaTime
        cam_distance = min(cam_distance, max_cam_distance)

    # Actualizar posición de la cámara
    rend.camera.position = glm.vec3(
        model.translation.x + glm.sin(glm.radians(cam_angle)) * cam_distance,
        model.translation.y + cam_height,
        model.translation.z + glm.cos(glm.radians(cam_angle)) * cam_distance
    )

    rend.camera.LookAt(model.translation)

    rend.Render()
    rend.time += deltaTime
    pygame.display.flip()

pygame.quit()
