import glfw
from pista import Pista
from OpenGL.GL import *
from OpenGL.GLU import *
import os

def inicializar_glfw():
    if not glfw.init():
        raise Exception("Falha ao inicializar o GLFW")

    # Criar janela
    window = glfw.create_window(800, 600, "Excite Bike 3D - GLFW", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Falha ao criar janela GLFW")

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()    
    gluPerspective(50, 800 / 600, 0.1, 100)  # FOV, aspecto, plano próximo, plano distante
    glMatrixMode(GL_MODELVIEW)
    return window

def desenharCena(pista, posicao_jogador):
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    #  câmera
    gluLookAt(0, 10, posicao_jogador, 
            0, 0, posicao_jogador + 10,
            0, 1, 0)

    # Instanciar e desenhar a pista
    pista.desenhar()

# Programa principal
def main():
    window = inicializar_glfw()
    textura_path = os.path.join("textures", "dirt_teste.jpg")
    pista = Pista(comprimento=10000, largura=15, textura_path=textura_path)
    posicao_jogador = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        posicao_jogador += 0.5 #adicionar limitador 

        desenharCena(pista, posicao_jogador)
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()
