from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np

class rider:
    def __init__ (self, velocidade,texture_file= None):
        self.velocidade = 0.001
        self.texture = None
        if texture_file:
            self.texture = self.carregar_textura(texture_file)
    

    def carregar_textura(self,path):
        image = Image.open(path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image = image.transpose(Image.FLIP_LEFT_RIGHT)

        img_data = np.array(list(image.getdata()), np.uint8)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
