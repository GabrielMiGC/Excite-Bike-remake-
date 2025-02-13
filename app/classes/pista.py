import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image



class Pista:
    def __init__(self, comprimento, largura, textura_path):
        self.comprimento = comprimento
        self.largura = largura
        self.textura_path = textura_path
        self.textura = self.carregar_textura(textura_path)
        self.velocidade = 0.1
        self.offset = 0.0

    def carregar_textura(self, textura_path):
        img = Image.open(textura_path).convert("RGBA")
        img_data = np.array(img, dtype=np.uint8)
        width, height = img.size

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        return texture_id

    def pistaMatrix(self):
        pass      

    def desenhar(self):
        if self.textura:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textura) 

        self.offset = self.velocidade
        if self.offset >= 1.0: # Limitador
            self.offset -= 1.0

        glColor3f(1, 1, 1) 
        glBegin(GL_QUADS)

        # coordenadas de textura
        glTexCoord2f(self.offset, 0)
        glVertex3f(-self.largura / 2, 0, 0)

        glTexCoord2f(self.offset, 10)
        glVertex3f(self.largura / 2, 0, 0)

        glTexCoord2f(1000 + self.offset, 10)
        glVertex3f(self.largura / 2, 0, self.comprimento)

        glTexCoord2f(1000 + self.offset, 0)
        glVertex3f(-self.largura / 2, 0, self.comprimento)

        glEnd()

        if self.textura:
            glBindTexture(GL_TEXTURE_2D, 0)  
            glDisable(GL_TEXTURE_2D)
