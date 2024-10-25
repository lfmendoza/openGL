# RendererOpenGL.py
import pygame
from pygame.locals import *
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from gl import Renderer
from model import Model
from shaders import *

width = 800
height = 600

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

faceModel = Model("models/model.obj")
faceModel.AddTexture("textures/model.bmp")
faceModel.translation.z = -5

rend.scene.append(faceModel)

vertex_shaders = [vertex_shader_default, vertex_shader_wave, vertex_shader_twist]
fragment_shaders = [fragment_shader_default, fragment_shader_grayscale, fragment_shader_inversion]

current_vertex_shader = vertex_shaders[0]
current_fragment_shader = fragment_shaders[0]

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

    if keys[K_LEFT]:
        rend.pointLight.x -= 5 * deltaTime

    if keys[K_RIGHT]:
        rend.pointLight.x += 5 * deltaTime

    if keys[K_UP]:
        rend.pointLight.z += 5 * deltaTime

    if keys[K_DOWN]:
        rend.pointLight.z -= 5 * deltaTime

    if keys[K_PAGEUP]:
        rend.pointLight.y += 5 * deltaTime

    if keys[K_PAGEDOWN]:
        rend.pointLight.y -= 5 * deltaTime

    if keys[K_a]:
        rend.camera.position.x -= 5 * deltaTime

    if keys[K_d]:
        rend.camera.position.x += 5 * deltaTime

    if keys[K_w]:
        rend.camera.position.z -= 5 * deltaTime

    if keys[K_s]:
        rend.camera.position.z += 5 * deltaTime

    rend.time += deltaTime

    rend.Render()
    pygame.display.flip()

pygame.quit()
