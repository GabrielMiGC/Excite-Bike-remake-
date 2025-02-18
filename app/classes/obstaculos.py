from OpenGL.GL import *
from OpenGL.GLU import *

class Obstaculos:
    
    def __init__(self, x, y, largura, altura, position=None):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.position = position

    def desenhar(self):
        """Desenha a barreira como um retângulo."""
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.largura, self.y)
        glVertex2f(self.x + self.largura, self.y + self.altura)
        glVertex2f(self.x, self.y + self.altura)
        glEnd()
        
    def calc_colision(self, player):
        """Calcula a colisão entre o jogador e a barreira."""
        # posição da moto varia de -12 a 12, a pista varia de -5 a 5
        return (player.x > self.position.x and
                player.x < self.position.x + self.largura)
