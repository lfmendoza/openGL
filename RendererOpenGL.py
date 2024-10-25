import pygame
from pygame.locals import *
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from gl import Renderer
from model import Model
from shaders import *

width = 1000
height = 1000

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.SCALED | pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

# rend.scene.append(Buffer(triangle))

faceModel = Model("models/model.obj")
faceModel.AddTexture("textures/model.bmp")
# faceModel.rotation.y = 180
faceModel.translation.z = -5
faceModel.scale.x = 2
faceModel.scale.y = 2
faceModel.scale.z = 2

rend.scene.append(faceModel)

vShader = vertex_shader
fShader = fragment_shader
rend.SetShaders(vShader, fShader)

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
                rend.FilledMode()
            elif event.key == pygame.K_2:
                rend.WireframeMode()
            elif event.key == pygame.K_3:
                vShader = vertex_shader
                rend.SetShaders(vShader, fShader)
            elif event.key == pygame.K_4:
                vShader = fat_shader
                rend.SetShaders(vShader, fShader)
            elif event.key == pygame.K_5:
                vShader = water_shader
                rend.SetShaders(vShader, fShader)
            elif event.key == pygame.K_6:
                fShader = fragment_shader
                rend.SetShaders(vShader, fShader)
            elif event.key == pygame.K_6:
                fShader = negative_shader
                rend.SetShaders(vShader, fShader)

    if keys[K_LEFT]:
        rend.pointLigth.x -= 1 * deltaTime

    if keys[K_RIGHT]:
        rend.pointLigth.x += 1 * deltaTime

    if keys[K_UP]:
        rend.pointLigth.z += 1 * deltaTime

    if keys[K_DOWN]:
        rend.pointLigth.z -= 1 * deltaTime
    
    if keys[K_PAGEUP]:
        rend.pointLigth.y -= 1 * deltaTime

    if keys[K_PAGEDOWN]:
        rend.pointLigth.y += 1 * deltaTime
    
    if keys[K_a]:
        rend.camera.position.x -= 1 * deltaTime
    
    if keys[K_d]:
        rend.camera.position.x += 1 * deltaTime
    
    if keys[K_w]:
        rend.camera.position.y += 1 * deltaTime

    if keys[K_s]:
        rend.camera.position.y -= 1 * deltaTime
    
    rend.time += deltaTime
    rend.camera.LookAt(faceModel.translation)

    rend.Render()
    pygame.display.flip()

pygame.quit()