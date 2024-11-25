from numpy import array, float32
from OpenGL.GL import *

class Buffer(object):
    def __init__(self, data):
        self.data = array(data, float32)

        # Vertex Buffer
        self.bufferObject = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferObject)
        glBufferData(GL_ARRAY_BUFFER,
                     self.data.nbytes,
                     self.data,
                     GL_STATIC_DRAW)
    
    def Use(self, attribNumber, size):
		
		# Atar los buffer objects a la tarjeta de video
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferObject)
		
		# Atributo
        glEnableVertexAttribArray(attribNumber)
		
        glVertexAttribPointer(attribNumber,			# Attribute number
            size,					# Size
			GL_FLOAT,				# Type
			GL_FALSE,				# Is it normalized?
			0,					# Stride size in bytes
			ctypes.c_void_p(0))	# Offset

