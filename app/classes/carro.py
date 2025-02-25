from OpenGL.GL import *
from OpenGL.GLU import *
from util import load_obj_car
import glm

class Carro:
    
    def __init__(self, x, y, largura, altura, position=None):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.position = position
        self.vertices, _, self.normals, self.faces = load_obj_car('app/objetos/car.obj')

    def desenhar(self):
        """Desenha o carro"""
        
        color_map = {
            'Black': glm.vec3(0, 0, 0),  # Preto
            'Body': glm.vec3(1.0, 0.0, 0.0),    # Vermelho
            'Bottom': glm.vec3(0.0, 0.0, 0.0),    # Preto
            'Bumpers': glm.vec3(0.46, 0.46, 0.46),    # Branca
            'Lights': glm.vec3(1.0, 1.0, 0.0),    # Amarelo
            'Tires': glm.vec3(0, 0, 0),    # Preto
            'Wheels': glm.vec3(0.46, 0.46, 0.46),    # Cinza
            'Window': glm.vec3(0.46, 0.46, 0.46),    # Cinza
        }
        
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glPushMatrix()        
        
        # Desenha o carro
        for face in self.faces:
            if len(face) == 3:
                glBegin(GL_TRIANGLES)
            else:
                glBegin(GL_POLYGON)
                
            for i, (vertex, material) in enumerate(face):
                color = color_map.get(material, glm.vec3(1.0, 1.0, 1.0))
                glColor3f(color.x, color.y, color.z)
                glVertex3f(*self.vertices[vertex])
            
            glEnd()

        glPopMatrix()
        
    def calc_colision(self, player):
        """Calcula a colisão entre o jogador e a barreira."""
        # posição da moto varia de -12 a 12, a pista varia de -5 a 5
        return (player.x > self.position.x and
                player.x < self.position.x + self.largura)
