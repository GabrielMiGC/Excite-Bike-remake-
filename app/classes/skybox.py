from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np

class Skybox:
    def __init__(self, textures):
        self.textures = [self.carregar_textura(t) for t in textures]
        self.offset = 0.0

    def carregar_textura(self, path):
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        image = Image.open(path).convert("RGB")
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(image, dtype=np.uint8)
        width, height = image.size

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        return texture_id

    def desenhar_face(self, vertices, texture_id, offset=0.0):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glBegin(GL_QUADS)
        for v in vertices:
            glTexCoord2f(v[3] + offset, v[4])
            glVertex3f(v[0], v[1], v[2])
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)

    def draw_cube(self):
        front_left = [
            (-15.0, -6, 90, 10, 0),
            (0.0, -6, 90, 5, 0),
            (0.0, 12, 80, 5, 1),
            (-15.0, 12, 80, 10, 1)
        ]
        
        front_right = [
            (0.0, -6, 90, 5, 0),
            (15.0, -6, 90, 0, 0),
            (15.0, 12, 80, 0, 1),
            (0.0, 12, 80, 5, 1)
        ]

        back_left = [
            (-15.0, -6, -100, 0, 0), 
            (0, -6, -100, 5, 0), 
            (0, 12, -100, 5, 1), 
            (-15.0, 12, -100, 0, 1)
        ]

        back_right = [
            (0.0, -6, -100, 5, 0),
            (15.0, -6, -100, 1, 0),
            (15.0, 12, -100, 1, 1),
            (0.0, 12, -100, 5, 1)
        ]

        
        top = [
            (-15.0,  12,  100, 1, 0), 
            (15.0,  12,  100, 0, 0), 
            (15.0,  12, -100, 0, 1), 
            (-15.0,  12, -100, 1, 1)
        ]
        
        bottom = [
            (-15.0, -6.1,  100, 10, 0), 
            (-15.0, -6.1, -100, 0, 0), 
            (15.0, -6.1, -100, 0, 1), 
            (15.0, -6.1,  100, 10, 1)
        ]
        
        left = [
            (15.0, -9,  100, 10, 0), 
            (15.0,  -9,  -100, 0, 0), 
            (15.0,  12, -100, 0, 1), 
            (15.0, 12, 100, 10, 1)
        ]
        
        right = [
            (-15.0, -9,  100, 10, 0), 
            (-15.0, -9, -100, 0, 0), 
            (-15.0, 12, -100, 0, 1), 
            (-15.0, 12, 100, 10, 1)
        ]

        # Desenhar faces com movimento
        for face, texture_id, offset_multiplier in [
            (front_left, 0, -1),    # Movimento para esquerda (+offset)
            (front_right, 0, 1),  # Movimento para direita (-offset)
            (back_left, 0, -1),
            (back_right, 0, -1),
            (top, 2, 0),
            (bottom, 3, 0),
            (left, 4, 1),
            (right, 5, 1)
        ]:
            if offset_multiplier != 0:
                adjusted_offset = self.offset * offset_multiplier
                self.desenhar_face(face, self.textures[texture_id], adjusted_offset)
            else:
                self.desenhar_face(face, self.textures[texture_id])

    def update_offset(self, speed):
        self.offset += speed
        if self.offset >= 1.0:
            self.offset -= 1.0