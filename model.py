from obj import Obj
from buffer import Buffer
from pygame import image
from OpenGL.GL import *
import glm
from array import array

class Model(object):
    def __init__(self, filename):
        objFile = Obj(filename=filename)

        self.vertices = objFile.vertices
        self.texCoords = objFile.texcoords
        self.normals = objFile.normals
        self.faces = objFile.faces

        self.texture = None

        self.buffer = Buffer(self.BuildBuffer())

        self.translation = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)

    def GetModelMatrix(self):
        identity = glm.mat4(1)
        translateMat = glm.translate(identity, self.translation)
        pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        yawMat = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        rollMat = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))

        rotationMat = pitchMat * yawMat * rollMat
        scaleMat = glm.scale(identity, self.scale)

        return translateMat * rotationMat * scaleMat

    def BuildBuffer(self):
        data = []

        for face in self.faces:
            faceVerts = []

            for i in range(len(face)):
                vert = []

                position = self.vertices[face[i][0] - 1]
                vert.extend(position)

                vts = self.texCoords[face[i][1] - 1]
                vert.extend(vts)

                normals = self.normals[face[i][2] - 1]
                vert.extend(normals)

                faceVerts.append(vert)

            # Triangulación
            for i in range(1, len(faceVerts) - 1):
                data.extend(faceVerts[0])
                data.extend(faceVerts[i])
                data.extend(faceVerts[i + 1])

        return data

    def AddTexture(self, textureFilename):
        self.textureSurface = image.load(textureFilename).convert()
        self.textureData = image.tostring(self.textureSurface, "RGB", True)
        self.texture = glGenTextures(1)

    def Render(self):
        if self.texture is not None:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGB,
                self.textureSurface.get_width(),
                self.textureSurface.get_height(),
                0,
                GL_RGB,
                GL_UNSIGNED_BYTE,
                self.textureData
            )
            glGenerateMipmap(GL_TEXTURE_2D)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        self.buffer.Render()
