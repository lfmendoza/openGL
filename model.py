from obj import Obj
from buffer import Buffer
from pygame import image
from OpenGL.GL import *
import glm

class Model(object):
    def __init__(self, filename):
        objFile = Obj(filename=filename)

        self.vertices = objFile.vertices
        self.texCoords = objFile.texcoords
        self.normals = objFile.normals
        self.faces = objFile.faces

        self.texture = None

        self.buffer = Buffer(self.BuildBuffer())

        self.translation = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0,0,0)
        self.scale = glm.vec3(1,1,1)
    
    def GetModelMatrix(self):
        # M = T * R * S
        # R = pitch * yaw * roll
        identity = glm.mat4x4(1)
        translateMat = glm.translate(identity, self.translation)
        pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
        yawMat = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
        rollMat = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

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
                for value in position:
                    vert.append(value)
                
                vts = self.texCoords[face[i][1] - 1]
                for value in vts:
                    vert.append(value)
                
                normals = self.texCoords[face[i][2] - 1]
                for value in normals:
                    vert.append(value)
                
                faceVerts.append(vert)
            
            for value in faceVerts[0]: data.append(value)
            for value in faceVerts[1]: data.append(value)
            for value in faceVerts[2]: data.append(value)

            if len(faceVerts) == 4:    
                for value in faceVerts[0]: data.append(value)
                for value in faceVerts[2]: data.append(value)
                for value in faceVerts[3]: data.append(value)
            
        return data
    
    def AddTexture(self, textureFilename):
        self.textureSurface = image.load(textureFilename)
        self.textureData = image.tostring(self.textureSurface, "RGB", True)
        self.texture = glGenTextures(1)
    
    def Render(self):

        if self.texture is not None:

            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glTexImage2D(GL_TEXTURE_2D,                         # Texture Types
                        0,                                      # Positions
                        GL_RGB,                                 # Format
                        self.textureSurface.get_width(),        # Width
                        self.textureSurface.get_height(),       # Height
                        0,                                      # Border
                        GL_RGB,                                 # Format
                        GL_UNSIGNED_BYTE,                       # Type
                        self.textureData)                       # Data

        self.buffer.Render()
