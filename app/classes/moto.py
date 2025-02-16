import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from classes.obstaculos import *
from util import shading, load_obj_gol
import glm
import consts


class Moto:
    def __init__(self):
        self.vertices, _, self.normals, self.faces = load_obj_gol('app/objetos/motoSimples.obj')

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
        
        color_map = {
            'engine': glm.vec3(0.46, 0.46, 0.46),  # Cinza
            'tire': glm.vec3(0.0, 0.0, 0.0),    # Preto
            'tank': glm.vec3(0.0, 0.0, 1.0),    # Azul
            'plate': glm.vec3(1.0, 1.0, 1.0),    # Branca
            'exhaust': glm.vec3(0.46, 0.46, 0.46),    # Cinza
            'rear_light': glm.vec3(1.0, 1.0, 0.0),    # Amarelo
            'seat': glm.vec3(0.0, 0.0, 0.0),    # Preto
        }
        
        glPushMatrix()
        glTranslatef(consts.positionBike.x, consts.positionBike.y, consts.positionBike.z)
        
        # Desenha a moto
        for face in self.faces:
            if len(face) == 3:
                glBegin(GL_TRIANGLES)
            else:
                glBegin(GL_POLYGON)
                
            
            
            for vertex, _, normal, material in face:
                color = color_map.get(material, glm.vec3(1.0, 1.0, 1.0))
                glColor3f(color.x, color.y, color.z)
                glVertex3f(*self.vertices[vertex])
            
            glEnd()

        glPopMatrix()