import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image



class Pista:
    def __init__(self, comprimento, largura, textura_path= None):
        self.comprimento = comprimento
        self.largura = largura
        self.raias = 4
        self.velocidade = 0.00001
        self.offset = 0.0
        self.textura = None
        if textura_path:
            self.textura = self.carregar_textura(textura_path)

    def carregar_textura(self, path):
        image = Image.open(path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image = image.transpose(Image.FLIP_LEFT_RIGHT)

        img_data = np.array(list(image.getdata()), np.uint8)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)  # Permitir repetição no eixo X
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)  # Permitir repetição no eixo Y
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # Filtro linear para minimizar
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # Filtro linear para ampliar

        glBindTexture(GL_TEXTURE_2D, 0)  # Desvincula a textura
        return texture_id
        

    def desenhar(self):
        """Desenha a pista com a textura carregada."""
        if self.textura:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textura)  # Usa a textura carregada

        self.offset = self.velocidade
        if self.offset >= 1.0: # Limitador
            self.offset -= 1.0

        glColor3f(1, 1, 1)  # Garante que a textura não seja influenciada pela cor
        glBegin(GL_QUADS)

        # Vértices com coordenadas de textura
        glTexCoord2f(self.offset, 0)
        glVertex3f(-self.largura / 2, 0, 0)

        glTexCoord2f(self.offset, 5)
        glVertex3f(self.largura / 2, 0, 0)

        glTexCoord2f(1000 + self.offset, 5)
        glVertex3f(self.largura / 2, 0, self.comprimento)

        glTexCoord2f(1000 + self.offset, 0)
        glVertex3f(-self.largura / 2, 0, self.comprimento)

        glEnd()

        if self.textura:
            glBindTexture(GL_TEXTURE_2D, 0)  # Desvincula a textura
            glDisable(GL_TEXTURE_2D)
