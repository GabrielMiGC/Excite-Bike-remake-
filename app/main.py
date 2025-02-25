import glfw
from classes.pista import Pista
from classes.moto import Moto
from classes.barreira import *
from classes.stone import *
from classes.carro import *
from classes.skybox import Skybox
from OpenGL.GL import *
from OpenGL.GLU import *
import consts
import util
import glm

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
    pistas = []
    # Cria uma única pista com 3 texturas diferentes
    pista = Pista(
        comprimento=consts.COMPRIMENTO_PISTA,
        largura=15,
        texturas_path=consts.texturas_pista  # Deve ser uma lista com 3 caminhos de textura
    )
    pista.posicao_inicial = 0  # Ajuste conforme necessário
    pistas.append(pista)
    
    return pistas



# Programa principal
def main():
    window, largura_tela, altura_tela = inicializar_glfw()
    glfw.set_key_callback(window, util.key_callback)
    glfw.set_mouse_button_callback(window, util.mouse_callback)

    pistas = inicializar_pistas()
    moto = Moto()
    consts.obstaculo1 = Barreira(0, 0, 5, 1.5)
    consts.obstaculo2 = Carro(0, 0, 5, 1.5)
    consts.obstaculo3 = Pedra(0, 0, 5, 1.5)
    
    # Carregar texturar dos botões de criação da pista e iniciar
    for chave, textura in consts.texturas_botoes.items():
        if chave == "Vidas":
            for vida in textura:
                vida[1] = util.carregar_textura(vida[0])  # Carrega a textura e armazena no índice [1]
        else:
            textura[1] = util.carregar_textura(textura[0])

        
    sky = Skybox(consts.cube_textures)
    posicao_jogador = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        util.update_movimento(consts.movimentando_esq, consts.movimentando_dir) # movimento da moto
        sky.update_offset(consts.offset_sky)  # Update the offset for the side faces
        
        if consts.tela == "criacao":
            util.desenharMenu(largura_tela, altura_tela)
        elif consts.tela == "jogo":
            consts.colisao = util.calc_colision(posicao_jogador)
            if consts.colisao:
                print("Colisão detectada!")
            else:
                posicao_jogador += 0.25
            util.desenharCena(pistas, posicao_jogador, sky, consts.posicoes_camera, consts.index_camera_atual, moto, largura_tela, altura_tela)
        glfw.swap_buffers(window)
    glfw.terminate()
    
if __name__ == "__main__":
    main()