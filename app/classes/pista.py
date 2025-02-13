import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from classes.obstaculos import *
from util import shading
import glm


class Pista:
    def __init__(self, comprimento, largura, textura_path):
        self.comprimento = comprimento
        self.largura = largura
        self.textura_path = textura_path
        self.textura = self.carregar_textura(textura_path)
        self.velocidade = 0.1
        self.offset = 0.0
        self.lightDiffuse = glm.vec3(1.0)      # Id               
        self.surfaceDiffuse = glm.vec3(1.0)    # Kd       
        self.lightSpecular = glm.vec3(1.0)     # Is
        self.surfaceSpecular = glm.vec3(0.5)   # Ks               
        self.surfaceShine = 250

        # Parâmetros da onda
        self.wave_length = 20.0  # Comprimento de onda
        self.wave_amplitude = 0.3  # Amplitude da onda
        # Pontos de controle da curva de Bézier (t, y) normalizados
        self.wave_control_points = [
            glm.vec2(0.0, 0.0),
            glm.vec2(0.25, 1.0),  # Pico no início
            glm.vec2(0.75, 1.0),  # Pico no final
            glm.vec2(1.0, 0.0)
        ]

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

    def get_y(self, z):
        z_local = z % self.wave_length
        t = z_local / self.wave_length

        # Cálculo da curva de Bézier cúbica
        p0, p1, p2, p3 = self.wave_control_points
        y = ((1 - t)**3 * p0.y + 3 * (1 - t)**2 * t * p1.y +
             3 * (1 - t) * t**2 * p2.y + t**3 * p3.y)
        
        return y * self.wave_amplitude

    def desenhar(self):
        if self.textura:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textura)

        # Atualiza o deslocamento da textura
        self.offset += self.velocidade
        if self.offset >= 1000.0:
            self.offset -= 1000.0

        glColor3f(1, 1, 1)
        glBegin(GL_QUAD_STRIP)

        segments = 200  # Número de segmentos para suavização
        delta_z = self.comprimento / segments

        for i in range(segments + 1):
            z = i * delta_z
            y = self.get_y(z)

            # Cálculo das coordenadas de textura
            s = (z / self.comprimento) * 1000 + self.offset

            # Vértice esquerdo
            glTexCoord2f(s, 0)
            glVertex3f(-self.largura / 2, y, z)

            # Vértice direito
            glTexCoord2f(s, 1)
            glVertex3f(self.largura / 2, y, z)

        glEnd()
        
        glPushMatrix()
        glTranslatef(-2.5, 0, 100)
        obstaculo1 = Obstaculos(0, 0, 10, 3)
        obstaculo1.desenhar()
        glPopMatrix()

        if self.textura:
            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_TEXTURE_2D)