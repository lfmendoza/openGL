from array import array
from OpenGL.GL import *

class Buffer(object):
    def __init__(self, data):
        self.vertexBuffer = array('f', data)
        self.VBO = glGenBuffers(1)
        self.VAO = glGenVertexArrays(1)

    def Render(self):
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        glBufferData(
            GL_ARRAY_BUFFER,
            self.vertexBuffer.buffer_info()[1] * self.vertexBuffer.itemsize,
            self.vertexBuffer.tobytes(),
            GL_STATIC_DRAW
        )

        # Atributo de posiciones
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Atributo de coordenadas de textura
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)

        # Atributo de normales
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(5 * 4))
        glEnableVertexAttribArray(2)

        glDrawArrays(GL_TRIANGLES, 0, len(self.vertexBuffer) // 8)
