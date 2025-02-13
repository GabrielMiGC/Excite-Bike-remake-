
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from PIL import Image
from OpenGL.GL import *
import consts

def desenharMenu():
    glClearColor(0, 0, 0.5, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    #  câmera
    
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    for i in range(10):
        y = -1+i*0.1
        glVertex2f(-1, y)
        glVertex2f(1, y)
    for j in range(3):
        x = -1 + j * 0.1
        glVertex2f(x,-1)
        glVertex2f(x, 1)
    glEnd()


def desenharCena(pistas, posicao_jogador, skybox, posicoes_camera, index_camera):
    glClearColor(0, 0, 0.5, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    #  câmera
    cam_pos = consts.posicoes_camera[consts.index_camera_atual]
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

def key_callback(window, key, scancode, action, mods):
    global index_camera_atual
    if key == glfw.KEY_C and action == glfw.PRESS:
        index_camera_atual = (index_camera_atual + 1) % len(posicoes_camera)
        print(f"Alterando para a câmera {index_camera_atual}")  # Debug

def shading (): #Phong
    # Reflexão do ambiente (Ra = Ia * Ka)
    ambientShading = CONSTS.light

    return shades