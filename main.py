import glfw
from pista import Pista
from skybox import Skybox
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import os



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
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(50, 1440 / 1040, 0.1, 100) # FOV, aspecto, plano próximo, plano distante
    glMatrixMode(GL_MODELVIEW)
    return window

posicoes_camera = [
    (0, 10, 0,   0, 0, 10,   0, 1, 0), #terceira pessoa
    (10, 10, 0,  0, 0, 10,   0, 1, 0), #canto superior esquerdo (atrás)
    (0, 5, 0,    0, 6, 10,   0, 1, 0), # primeira pessoa
    (-10, 10,0,  0, 0, 10,   0, 1, 0), #canto superior direito (atrás)
    (0, 6, 10,  5, 5, 0,   0, 1, 0)  # visão lateral (2D)
]
index_camera_atual = 0

def key_callback(window, key, scancode, action, mods):
    global index_camera_atual
    if key == glfw.KEY_C and action == glfw.PRESS:
        index_camera_atual = (index_camera_atual + 1) % len(posicoes_camera)
        print(f"Alterando para a câmera {index_camera_atual}")  # Debug

def desenharCena(pistas, posicao_jogador, skybox):
    glClearColor(0, 0, 0.5, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    #  câmera
    cam_pos = posicoes_camera[index_camera_atual]
    gluLookAt(cam_pos[0], cam_pos[1], posicao_jogador + cam_pos[2], 
              cam_pos[3], cam_pos[4], posicao_jogador + cam_pos[5],
              cam_pos[6], cam_pos[7], cam_pos[8])


    for pista in pistas:
        glPushMatrix()
        glTranslate(0,0,-pista.posicao_inicial)
        pista.desenhar()
        glPopMatrix()

    # Desenhar o cubo
    glPushMatrix()
    glTranslatef(0, 0, posicao_jogador+ 10)
    skybox.draw_cube()
    glPopMatrix()

def inicializar_pistas():
    texturas = [
        os.path.join("textures", "dirt.jpg"),
        os.path.join("textures", "dirt2.jpg"),
        os.path.join("textures", "dirt3.jpg"),
        os.path.join("textures", "dirt4.jpg")
    ]

    comprimento_pista = 1000
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
    glfw.set_key_callback(window, key_callback)

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
        desenharCena(pistas, posicao_jogador, sky)
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()