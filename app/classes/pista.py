import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from util import shading
import consts
import glm


class Pista:
    def __init__(self, comprimento, largura, texturas_path):
        self.comprimento = comprimento
        self.largura = largura
        self.texturas = [self.carregar_textura(t) for t in texturas_path]  # Lista de texturas
        self.velocidade = 0.1
        self.offset = 0.0
        self.raias = 3  # Número de raias
        self.largura_raia = largura / self.raias
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
        glColor3f(1, 1, 1)
        if not consts.colisao:
            self.offset += self.velocidade
            if self.offset >= 1000.0:
                self.offset -= 1000.0
        # else:
        #     self.offset = 0
        
        # Ajuste dinâmico de segmentos baseado no comprimento da onda
        segments = int(self.comprimento / (self.wave_length / 4))  # 4 segmentos por onda
        delta_z = self.comprimento / segments

        # Desenha cada raia separadamente
        for raia in range(self.raias):
            if self.texturas:
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.texturas[raia % len(self.texturas)])

            # Calcula os limites da raia
            x_left = -self.largura/2 + raia * self.largura_raia
            x_right = x_left + self.largura_raia

            glBegin(GL_QUAD_STRIP)
            for i in range(segments + 1):
                z = i * delta_z
                y = self.get_y(z)
                s = (z / self.comprimento) * 1000 + self.offset

                # Vértices para esta raia
                glTexCoord2f(s, 0)
                glVertex3f(x_left, y, z)
                
                glTexCoord2f(s, 1)
                glVertex3f(x_right, y, z)
            glEnd()

            if self.texturas:
                glBindTexture(GL_TEXTURE_2D, 0)
                glDisable(GL_TEXTURE_2D)
        
        # Desenha obstáculo
        for segmento, coordenadas_pista in consts.segmentos_matrizes.items():
            for tipo_obstaculo, coordenadas_raias in enumerate(coordenadas_pista, start=1):
                deslocamento_z = (segmento - 1) * 100 
                for raia in coordenadas_raias:  # Itera sobre as raias 
                    for (z, x) in raia:  # Para cada par de coordenadas (z, x)
                        glPushMatrix()
                        obstaculo = getattr(consts, f"obstaculo{tipo_obstaculo}")
                        obstaculo.position = glm.vec3(x, 0, z + deslocamento_z)  # Define a posição do obstáculo
                        obstaculo.desenhar()  # Chama a função de desenhar o obstáculo
                        glPopMatrix()
            
        if self.texturas:
            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_TEXTURE_2D)

    """def desenhar(self):
        glColor3f(1, 1, 1)

        if not consts.colisao:
            self.offset += self.velocidade
            if self.offset >= 1000.0:
                self.offset -= 1000.0
        # else:
        #     self.offset = 0
        
        # Ajuste dinâmico de segmentos baseado no comprimento da onda
        segments = int(self.comprimento / (self.wave_length / 4))  # 4 segmentos por onda
        delta_z = self.comprimento / segments

        # Desenha cada raia separadamente
        for raia in range(self.raias):
            if self.texturas:
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.texturas[raia % len(self.texturas)])

            # Calcula os limites da raia
            x_left = -self.largura/2 + raia * self.largura_raia
            x_right = x_left + self.largura_raia

            glBegin(GL_QUAD_STRIP)
            for i in range(segments + 1):
                z = i * delta_z
                y = self.get_y(z)
                s = (z / self.comprimento) * 1000 + self.offset

                # Normal aproximada apontando para cima
                normal = glm.vec3(0.0, 1.0, 0.0)
                
                # Vértices para esta raia
                point_left = glm.vec3(x_left, y, z)
                point_right = glm.vec3(x_right, y, z)

                # Aplicar iluminação
                shade_left = shading(point_left, normal, self)
                shade_right = shading(point_right, normal, self)

                glColor3f(shade_left.x, shade_left.y, shade_left.z)
                glTexCoord2f(s, 0)
                glVertex3f(x_left, y, z)

                glColor3f(shade_right.x, shade_right.y, shade_right.z)
                glTexCoord2f(s, 1)
                glVertex3f(x_right, y, z)
            glEnd()

            if self.texturas:
                glBindTexture(GL_TEXTURE_2D, 0)
                glDisable(GL_TEXTURE_2D)
        
        # Desenha obstáculo
        for segmento, coordenadas_pista in consts.segmentos_matrizes.items():
            for tipo_obstaculo, coordenadas_raias in enumerate(coordenadas_pista, start=1):
                deslocamento_z = (segmento - 1) * 100 
                for raia in coordenadas_raias:  # Itera sobre as raias 
                    for (z, x) in raia:  # Para cada par de coordenadas (z, x)
                        glPushMatrix()
                        obstaculo = getattr(consts, f"obstaculo{tipo_obstaculo}")
                        obstaculo.position = glm.vec3(x, 0, z + deslocamento_z)  # Define a posição do obstáculo
                        obstaculo.desenhar()  # Chama a função de desenhar o obstáculo
                        glPopMatrix()
            
        if self.texturas:
            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_TEXTURE_2D)"""