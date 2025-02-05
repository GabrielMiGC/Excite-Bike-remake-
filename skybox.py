from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np

class Skybox:
    def __init__(self, textures):
        self.textures = [self.carregar_textura(t) for t in textures]

    def carregar_textura(self, path):

        image = Image.open(path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

        img_data = np.array(list(image.getdata()), np.uint8)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, 0)
        return texture_id

    def desenhar_face(self, vertices, texture_id):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glBegin(GL_QUADS)
        for v in vertices:
            glTexCoord2f(v[3], v[4])
            glVertex3f(v[0], v[1], v[2])
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)

    def draw_cube(self):

        vertices = [
        # front
        [(-15.0, -5,  90, 1, 0), ( 15.0, -5, 90, 0, 0), ( 15.0,  12,  80, 0, 1), (-15.0,  12,  80, 1, 1)],
        # back
        [(-15.0, -6, -100, 0, 0), (15.0, -6, -100, 1, 0), (15.0, 12, -100, 1, 1), (-15.0, 12, -100, 0, 1)],
        # top
        [(-15.0,  12,  100, 1, 0), ( 15.0,  12,  100, 0, 0), ( 15.0,  12, -100, 0, 1), (-15.0,  12, -100, 1, 1)], 
        # bottom 
        [(-15.0, -6.1,  100, 10, 0), (-15.0, -6.1, -100, 0, 0), ( 15.0, -6.1, -100, 0, 1), ( 15.0, -6.1,  100, 10, 1)],  
        # left
        [( 15.0, -9,  100, 10, 0), ( 15.0,  -9,  -100, 0, 0), ( 15.0,  12, -100, 0, 1), ( 15.0, 12, 100, 10, 1)],  
        # right
        [(-15.0, -9,  100, 10, 0), (-15.0, -9, -100, 0, 0), (-15.0, 12, -100, 0, 1), (-15.0, 12, 100, 10, 1)]  
    ]
        for i in range(6):
            self.desenhar_face(vertices[i], self.textures[i])
