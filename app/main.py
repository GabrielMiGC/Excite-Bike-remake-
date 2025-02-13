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


    monitor = glfw.get_primary_monitor()
    modo_video = glfw.get_video_mode(monitor)
    
    largura_tela = modo_video.size.width
    altura_tela = modo_video.size.height

    # Criar janela
    window = glfw.create_window(largura_tela, altura_tela, "Excite Bike 3D - GLFW", monitor, None)
    if not window:
        glfw.terminate()
        raise Exception("Falha ao criar janela GLFW")

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    return window, largura_tela, altura_tela


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
    window, largura_tela, altura_tela = inicializar_glfw()
    glfw.set_key_callback(window, util.key_callback)
    glfw.set_mouse_button_callback(window, util.mouse_callback)

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
        # print(f"Frame renderizado - posição do jogador: {posicao_jogador}")
        glfw.poll_events()
        sky.update_offset(0.015)  # Update the offset for the side faces

        if consts.tela == "criacao":
            util.desenharMenu(largura_tela, altura_tela)
        elif consts.tela == "jogo":
            posicao_jogador += 0.015
            util.desenharCena(pistas, posicao_jogador, sky, consts.posicoes_camera, consts.index_camera_atual)
        glfw.swap_buffers(window)
    glfw.terminate()
    
if __name__ == "__main__":
    main()