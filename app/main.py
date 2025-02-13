import glfw
from classes.pista import Pista
from classes.skybox import Skybox
from OpenGL.GL import *
from OpenGL.GLU import *
import consts
import os
import util



def inicializar_glfw():
    if not glfw.init():
        raise Exception("Falha ao inicializar o GLFW")

    # Criar janela
    window = glfw.create_window(1440, 1040, "Excite Bike 3D - GLFW", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Falha ao criar janela GLFW")

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    #glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1,1,-1,1,-1,1)
    #gluPerspective(50, 1440 / 1040, 0.1, 100) # FOV, aspecto, plano próximo, plano distante
    glMatrixMode(GL_MODELVIEW)
    return window


def inicializar_pistas():
    texturas = [
        os.path.join("textures", "dirt.jpg"),
        os.path.join("textures", "dirt2.jpg"),
        os.path.join("textures", "dirt3.jpg"),
        os.path.join("textures", "dirt4.jpg")
    ]

    comprimento_pista = 100
    largura_pista = 15
    pistas = []
    for i, textura in enumerate(texturas):  
        pista = Pista(comprimento=comprimento_pista, largura=largura_pista, textura_path=textura)
        pista.posicao_inicial = -(i * comprimento_pista)
        pistas.append(pista)
    
    return pistas



# Programa principal
def main():
    window = inicializar_glfw()
    glfw.set_key_callback(window, util.key_callback)

    pistas = inicializar_pistas()
    cube_textures = [
        os.path.join("textures", "front.jpg"),
        os.path.join("textures", "back.jpg"),
        os.path.join("textures", "sky.jpg"),
        os.path.join("textures", "dirt.jpg"),
        os.path.join("textures", "lado.jpg"),
        os.path.join("textures", "lado.jpg")
    ]

    sky = Skybox(cube_textures)
    posicao_jogador = 0
    while not glfw.window_should_close(window):
        print(f"Frame renderizado - posição do jogador: {posicao_jogador}")
        glfw.poll_events()
        posicao_jogador += 0.015
        sky.update_offset(0.015)  # Update the offset for the side faces

        #util.desenharCena(pistas, posicao_jogador, sky)
        util.desenharMenu()
        glfw.swap_buffers(window)
    glfw.terminate()
    
if __name__ == "__main__":
    main()