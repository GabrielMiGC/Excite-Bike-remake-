import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import time
from PIL import Image
from OpenGL.GL import *
import glfw
import consts
import classes.camera as cam
import glm
import numpy as np


# Crie uma instância global
camera_state = cam.CameraState()

def desenharMenu(largura_tela, altura_tela):
    
    NUM_LINHAS = consts.NUM_LINHAS
    NUM_COLUNAS = consts.NUM_COLUNAS
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, largura_tela, altura_tela, 0, -1, 1)  # Define um sistema de coordenadas (3 linhas, 11 colunas)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    largura_matriz = largura_tela * 0.5
    altura_matriz = altura_tela * 0.3
    
    x_inicio = (largura_tela - largura_matriz) / 2
    y_inicio = (altura_tela - altura_matriz) / 2
    celula_largura = largura_matriz / NUM_COLUNAS
    celula_altura = altura_matriz / NUM_LINHAS
    
    # --- Configurações dos Botões ---
    largura_botao = largura_tela * 0.1
    altura_botao = altura_tela * 0.05
    espaco_botao = largura_tela * 0.02
    xBot_inicio = (largura_tela - (3 * largura_botao + 2 * espaco_botao)) / 2
    yBot_inicio = y_inicio - altura_botao - 20  # Espaço acima da matriz

    # --- Desenhar os botões de criação de objetos ---
    for i, cor in enumerate(consts.CORES_BOTOES):
        glColor3f(*cor)
        glBegin(GL_QUADS)
        x_min = xBot_inicio + i * (largura_botao + espaco_botao)
        x_max = x_min + largura_botao
        y_min = yBot_inicio
        y_max = yBot_inicio + altura_botao
        glVertex2f(x_min, y_min)
        glVertex2f(x_max, y_min)
        glVertex2f(x_max, y_max)
        glVertex2f(x_min, y_max)
        glEnd()

    # --- Botão de Iniciar ---
    largura_botao_iniciar = largura_tela * 0.2
    altura_botao_iniciar = altura_tela * 0.06
    x_inicio_botao = (largura_tela - largura_botao_iniciar) / 2
    y_inicio_botao = yBot_inicio + 2 * altura_matriz  # Abaixo dos botões de cor

    glColor3f(0.8, 0.8, 0.8)  # Cor do botão
    glBegin(GL_QUADS)
    glVertex2f(x_inicio_botao, y_inicio_botao)
    glVertex2f(x_inicio_botao + largura_botao_iniciar, y_inicio_botao)
    glVertex2f(x_inicio_botao + largura_botao_iniciar, y_inicio_botao + altura_botao_iniciar)
    glVertex2f(x_inicio_botao, y_inicio_botao + altura_botao_iniciar)
    glEnd()

    # desenhando a grade da matriz
    glColor3f(1, 1, 1)
    glLineWidth(3)
    glBegin(GL_LINES)
    
    # Linhas horizontais
    for i in range(NUM_LINHAS + 1):
        y = y_inicio + i * celula_altura
        glVertex2f(x_inicio, y)
        glVertex2f(x_inicio + largura_matriz, y)
        
    # Linhas verticais
    for j in range(NUM_COLUNAS + 1):
        x = x_inicio + j * celula_largura
        glVertex2f(x, y_inicio)
        glVertex2f(x, y_inicio + altura_matriz)
        
    glEnd()

    # --- Desenhando a Matriz ---
    for i in range(NUM_LINHAS):
        for j in range(NUM_COLUNAS):
            glColor3f(*consts.matriz_cores[i][j])  # Cor de fundo das células
            x_min = x_inicio + j * celula_largura
            x_max = x_min + celula_largura
            y_min = y_inicio + i * celula_altura
            y_max = y_min + celula_altura

            glBegin(GL_QUADS)
            glVertex2f(x_min, y_min)
            glVertex2f(x_max, y_min)
            glVertex2f(x_max, y_max)
            glVertex2f(x_min, y_max)
            glEnd()

def desenharCena(pistas, posicao_jogador, skybox, posicoes_camera, index_camera, moto):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(50, 1440 / 1040, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
            
    glClearColor(0, 0, 0.5, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Controle da transição da câmera
    target_cam_pos = posicoes_camera[index_camera]
    
    # Iniciar nova transição se a câmera mudar
    if camera_state.target_cam_pos != target_cam_pos:
        camera_state.start_cam_pos = camera_state.current_cam_pos or target_cam_pos
        camera_state.target_cam_pos = target_cam_pos
        camera_state.transition_start_time = time.time()
        camera_state.is_transitioning = True

    # Calcular progresso da animação
    if camera_state.is_transitioning:
        elapsed = time.time() - camera_state.transition_start_time
        t = min(elapsed / camera_state.transition_duration, 1.0)
        
        t_ease = t * t * (3 - 2 * t)
        
        # Interpolar todos os componentes da câmera
        cam_pos = [
            lerp(camera_state.start_cam_pos[i], camera_state.target_cam_pos[i], t_ease)
            for i in range(9)
        ]
        
        if t >= 1.0:
            camera_state.is_transitioning = False
        camera_state.current_cam_pos = cam_pos
    else:
        cam_pos = camera_state.target_cam_pos

    gluLookAt(
        cam_pos[0], cam_pos[1], posicao_jogador + cam_pos[2], 
        cam_pos[3], cam_pos[4], posicao_jogador + cam_pos[5],
        cam_pos[6], cam_pos[7], cam_pos[8]
    )
    
    glPushMatrix()
    glTranslatef(0, -1, cam_pos[2] + posicao_jogador + 6)
    glRotatef(90, 0, 1, 0)
    glTranslatef(0, 0, 0)
    glScalef(0.6, 0.6, 0.6)
    moto.desenhar()
    glPopMatrix()

    for pista in pistas:
        glPushMatrix()
        glTranslate(0,0,-pista.posicao_inicial)
        pista.desenhar()
        glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, posicao_jogador + 10)
    skybox.draw_cube()
    glPopMatrix()

def lerp(a, b, t):
    return a + (b - a) * t

def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_C and action == glfw.PRESS:
        consts.index_camera_atual = (consts.index_camera_atual + 1) % len(consts.posicoes_camera)
        print(f"Alterando para a câmera {consts.index_camera_atual}")  # Debug
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if key == glfw.KEY_LEFT:
        if action == glfw.PRESS:
            consts.movimentando_esq = True
        elif action == glfw.RELEASE:
            consts.movimentando_esq = False
    if key == glfw.KEY_RIGHT:
        if action == glfw.PRESS:
            consts.movimentando_dir = True
        elif action == glfw.RELEASE:
            consts.movimentando_dir = False


def mouse_callback(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS :
        xpos, ypos = glfw.get_cursor_pos(window)
        largura_janela, altura_janela = glfw.get_framebuffer_size(window)

        # --- Configurações dos botões ---
        largura_botao = largura_janela * 0.1
        altura_botao = altura_janela * 0.05
        espaco_botao = largura_janela * 0.02
        xBot_inicio = (largura_janela - (3 * largura_botao + 2 * espaco_botao)) / 2
        yBot_inicio = ((altura_janela - (altura_janela * 0.3)) / 2) - altura_botao - 20 

        # Posição do botão de iniciar
        largura_botao_iniciar = largura_janela * 0.2
        altura_botao_iniciar = altura_janela * 0.06
        x_inicio_botao = (largura_janela - largura_botao_iniciar) / 2
        y_inicio_botao = yBot_inicio + 2*altura_janela * 0.3

        # Verifica se o clique está no botão de iniciar
        if x_inicio_botao <= xpos <= x_inicio_botao + largura_botao_iniciar and \
           y_inicio_botao <= ypos <= y_inicio_botao + altura_botao_iniciar:
            matriz_exported = [
                [consts.cor_para_numero.get(consts.matriz_cores[i][j], -1) for j in range(consts.NUM_COLUNAS)]
                for i in range(consts.NUM_LINHAS)
            ]            
            consts.tela = "jogo"
            
            z_values = [2.5, -2.5, -7.5]
            matriz = np.array(matriz_exported)
            consts.coordenadas_obstaculos = [
                [(idx * 5, z_values[seg]) for idx, val in enumerate(linha) if val == 1]  
                for seg, linha in enumerate(matriz)
            ]
            print("Matriz exportada: ", matriz_exported)
            print("Coordenadas dos obstáculos: ", consts.coordenadas_obstaculos)
            print("Mudando para a tela do jogo!")

        # Verificar se o clique foi em algum botão
        for i, cor in enumerate(consts.CORES_BOTOES):
            x_min = xBot_inicio + i * (largura_botao + espaco_botao)
            x_max = x_min + largura_botao
            y_min = yBot_inicio
            y_max = yBot_inicio + altura_botao

            if x_min <= xpos <= x_max and y_min <= ypos <= y_max:
                consts.botao_selecionado = cor
                print(f"Cor selecionada: {cor}")
                return  # Sai da função para evitar trocar célula ao mesmo tempo


        # Ajuste para coordenadas normalizadas
        largura_matriz = largura_janela * 0.5  # 50% da largura da tela
        altura_matriz = altura_janela * 0.3  # 30% da altura da tela

        # Posição inicial da matriz (centrada na tela)
        x_inicio = (largura_janela - largura_matriz) / 2
        y_inicio = (altura_janela - altura_matriz) / 2
 
        # Verifica se o clique está dentro da matriz
        if x_inicio <= xpos <= x_inicio + largura_matriz and y_inicio <= ypos <= y_inicio + altura_matriz:
            celula_largura = largura_matriz / consts.NUM_COLUNAS
            celula_altura = altura_matriz / consts.NUM_LINHAS

            # Converter as coordenadas do clique para células da matriz
            x = int((xpos - x_inicio) / celula_largura)
            y = int((ypos - y_inicio) / celula_altura)

            consts.matriz_cores[y][x] = consts.botao_selecionado

def shading (): #Phong
    # Reflexão do ambiente (Ra = Ia * Ka)
    ambientShading = CONSTS.light

    return shades

def load_obj(filename):
    vertices = []
    textures = []
    normals = []
    faces = []
    current_material = None

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Linha de vértice
                parts = line.split()
                vertex = list(map(float, parts[1:4]))
                vertices.append(vertex)
            elif line.startswith('vt '):  # Linha de textura
                parts = line.split()
                texture = list(map(float, parts[1:3]))
                textures.append(texture)
            elif line.startswith('vn '):  # Linha de normal
                parts = line.split()
                normal = list(map(float, parts[1:4]))
                normals.append(normal)
            elif line.startswith('usemtl '):  # Linha de material
                parts = line.split()
                current_material = parts[1]
            elif line.startswith('f '):  # Linha de face
                parts = line.split()
                face = []
                for part in parts[1:]:
                    vals = part.split('/')
                    vertex_index = int(vals[0]) - 1
                    texture_index = int(vals[1]) - 1 if len(vals) > 1 and vals[1] else None
                    normal_index = int(vals[2]) - 1 if len(vals) > 2 and vals[2] else None
                    face.append((vertex_index, texture_index, normal_index, current_material))
                faces.append(face)

    return vertices, textures, normals, faces

def update_movimento(movimentando_esq, movimentando_dir):
    if movimentando_esq:
        consts.positionBike.z = glm.clamp(consts.positionBike.z + 0.2, -12, 12)
    elif movimentando_dir:
        consts.positionBike.z = glm.clamp(consts.positionBike.z - 0.2, -12, 12)
        
def converter_posicao_moto():
    # posição da moto varia de -12 a 12, a pista varia de -7.5 a 7.5
    return (((consts.positionBike.z + 12) * (7.5 - (-7.5)) / (12 - (-12))) - 7.5)

def calc_colision(posição_jogador):
    for seg in consts.coordenadas_obstaculos:
        for (z, x) in seg:
            if (
                x + consts.LARGURA_OBSTACULO > converter_posicao_moto() - consts.LARGURA_MOTO and 
                x < converter_posicao_moto() + consts.LARGURA_MOTO and 
                z == (posição_jogador + 6 + consts.COMPRIMENTO_MOTO)
            ):
                return True
    return False