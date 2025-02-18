
import os
import glm

movimentando_esq = False
movimentando_dir = False

tela ="criacao"
botao_selecionado = (0.1, 0.1, 0.1)

NUM_LINHAS = 3
NUM_COLUNAS = 10

LARGURA_MOTO = 0.6
LARGURA_OBSTACULO = 5
COMPRIMENTO_MOTO = 1.75

CORES_BOTOES = [
    (1.0, 0.0, 0.0),  # Vermelho
    (0.0, 1.0, 0.0),  # Verde
    (0.0, 0.0, 1.0)   # Azul
]

cor_para_numero = {
    (0.1, 0.1, 0.1): 0,
    (1.0, 0.0, 0.0): 1,  # Vermelho
    (0.0, 1.0, 0.0): 2,  # Verde
    (0.0, 0.0, 1.0): 3   # Azul
}

matriz_cores = [[(0.1, 0.1, 0.1) for _ in range(NUM_COLUNAS)] for _ in range(NUM_LINHAS)]  # Branco por padrão

coordenadas_obstaculos = []
obstaculo1 = None

positionBike = glm.vec3(0.0, 0.0, 0.0)

posicoes_camera = [
    (0, 10, 0,   0, 0, 10,   0, 1, 0), #terceira pessoa
    (10, 10, 0,  0, 0, 10,   0, 1, 0), #canto superior esquerdo (atrás)
    (0, 2.5, 0,    0, 6, 10,   0, 1, 0), # primeira pessoa
    (-10, 10,0,  0, 0, 10,   0, 1, 0), #canto superior direito (atrás)
    (0, 6, 10,  5, 5, 0,   0, 1, 0)  # visão lateral (2D)
]
index_camera_atual = 0

texturas_pista = [
        os.path.join("textures", "dirt.jpg"),
        os.path.join("textures", "dirt2.jpg"),
        os.path.join("textures", "dirt3.jpg"),
    ]

cube_textures = [
        os.path.join("textures", "front.jpg"),
        os.path.join("textures", "front.jpg"),
        os.path.join("textures", "sky.jpg"),
        os.path.join("textures", "dirt.jpg"),
        os.path.join("textures", "lado.jpg"),
        os.path.join("textures", "lado.jpg")
    ]