from OpenGL.GL import *
from OpenGL.GLU import *

class Obstaculos:
    
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura

    def desenhar(self):
        """Desenha a barreira como um retângulo."""
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.largura, self.y)
        glVertex2f(self.x + self.largura, self.y + self.altura)
        glVertex2f(self.x, self.y + self.altura)
        glEnd()
