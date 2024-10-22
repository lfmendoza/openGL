from numpy import array, float32

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class Buffer(object):
    def __init__(self, data):
        self.vertexBuffer = array(data, float32)
        self.VBO = glGenBuffers(1)
        self.VAO = glGenVertexArrays(1)

    def Render(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        # Maandar la informacion de los vertices
        glBufferData(GL_ARRAY_BUFFER,
                     self.vertexBuffer.nbytes,
                     self.vertexBuffer,
                     GL_STATIC_DRAW)


        # Attributo de posiciones
        glVertexAttribPointer(0,
                            3,
                            GL_FLOAT,
                            GL_FALSE,
                            4*6,
                            ctypes.c_void_p(0)
                            )
        

        glEnableVertexAttribArray(0)

        # Attributo de colores
        glVertexAttribPointer(1,                    # Attribute number
                            3,                      # Size
                            GL_FLOAT,               # Type
                            GL_FALSE,               # Is it normalized?
                            4*8,                    # Stride size in bytes
                            ctypes.c_void_p(4*3)    # Offset
                            )
        

        glEnableVertexAttribArray(1)

         # Attributo de normales
        glVertexAttribPointer(2,                    # Attribute number
                            3,                      # Size
                            GL_FLOAT,               # Type
                            GL_FALSE,               # Is it normalized?
                            4*8,                    # Stride size in bytes
                            ctypes.c_void_p(4*5)    # Offset
                            )
        

        glEnableVertexAttribArray(2)

        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertexBuffer)/8))