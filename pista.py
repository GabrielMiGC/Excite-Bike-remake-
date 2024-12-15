import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image



class Pista:
    def __init__(self, comprimento, largura, textura_path= None):
        self.comprimento = comprimento
        self.largura = largura
        self.raias = 2
        self.velocidade = 0.001
        self.offset = 0.0
        self.textura = None
        if textura_path:
            self.textura = self.carregar_textura(textura_path)

    def carregar_textura(self, path):
        textura_id = glGenTextures(1) 
        glBindTexture(GL_TEXTURE_2D, textura_id)  

        # Abrir a imagem usando PIL
        imagem = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL usa o eixo Y invertido
        img_data = imagem.convert("RGB").tobytes()

        # Configura a textura no OpenGL
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, imagem.width, imagem.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)  # Permitir repetição no eixo S
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)  # Permitir repetição no eixo T
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # Filtro linear para minimizar
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # Filtro linear para ampliar

        glBindTexture(GL_TEXTURE_2D, 0)  # Desvincula a textura
        return textura_id
        

    def desenhar(self):
        """Desenha a pista com a textura carregada."""
        if self.textura:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textura)  # Usa a textura carregada

        self.offset += self.velocidade
        if self.offset >= 1.0: # Limitador
            self.offset -= 1.0

        glColor3f(1, 1, 1)  # Garante que a textura não seja influenciada pela cor
        glBegin(GL_QUADS)

        # Vértices com coordenadas de textura
        glTexCoord2f(0, self.offset)
        glVertex3f(-self.largura / 2, 0, 0)
        glTexCoord2f(1, self.offset)
        glVertex3f(self.largura / 2, 0, 0)
        glTexCoord2f(1, 1 + self.offset)
        glVertex3f(self.largura / 2, 0, self.comprimento)
        glTexCoord2f(0, 1 + self.offset)
        glVertex3f(-self.largura / 2, 0, self.comprimento)

        glEnd()

        if self.textura:
            glBindTexture(GL_TEXTURE_2D, 0)  # Desvincula a textura
            glDisable(GL_TEXTURE_2D)
