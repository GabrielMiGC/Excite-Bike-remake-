from OpenGL.GL import *
from OpenGL.GLU import *
from util import load_obj
from PIL import Image
import numpy as np
import os



class Carro:
    
    def __init__(self, x, y, largura, altura, position=None):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.position = position
        self.textura = self.carregar_textura(os.path.join("textures", "car.png"))
        self.vertices, self.textures, self.normals, self.faces = load_obj('app/objetos/car.obj')

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

    def desenhar(self):
        """Desenha o carro"""
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glPushMatrix()
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textura)
        
        for face in self.faces:
            if len(face) == 3:
                glBegin(GL_TRIANGLES)
            else:
                glBegin(GL_POLYGON)
            
            for i, (vertex, tex_coord, normal, material) in enumerate(face):
                if tex_coord is not None:
                    glTexCoord2f(self.textures[tex_coord][0], self.textures[tex_coord][1])
                glVertex3f(*self.vertices[vertex])
            
            glEnd()
        
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        
    def calc_colision(self, player):
        """Calcula a colisão entre o jogador e o carro."""
        return (player.x > self.position.x and player.x < self.position.x + self.largura)
