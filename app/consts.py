
import os
import glm

movimentando_esq = False
movimentando_dir = False
colisao = False

offset_sky = 0.015

tela ="criacao"
botao_selecionado = (0.1, 0.1, 0.1)

COMPRIMENTO_PISTA = 300

NUM_LINHAS = 3
NUM_COLUNAS = 20
segmento_atual = 1
max_segmento = COMPRIMENTO_PISTA/100

LARGURA_MOTO = 0.6
LARGURA_OBSTACULO = 5
LARGURA_OBSTACULO_MENOR = 2.5
COMPRIMENTO_MOTO = 1.75
COMPRIMENTO_OBSTACULO = 10
COMPRIMENTO_OBSTACULO_MENOR = 2.5

CORES_BOTOES = [
    (1.0, 0.0, 0.0),  # Vermelho
    (0.0, 1.0, 0.0),  # Verde
    (0.0, 0.0, 1.0)   # Azul
]

NUM_VIDAS = 3
VIDAS = [1 for _ in range(NUM_VIDAS)]
posicoes_perda_vida = set()  # Guarda as posições onde a vida foi retirada

texturas_botoes = {
    "obs1" : [os.path.join("textures", "obs1.png"), 0],
    "obs2" : [os.path.join("textures", "obs2.png"), 0],
    "obs3" : [os.path.join("textures", "obs3.png"), 0],
    "iniciar" : [os.path.join("textures", "iniciar.png"), 0],
    "prox" : [os.path.join("textures", "proximo_seg.png"), 0],
    "ant" : [os.path.join("textures", "anterior_seg.png"), 0],
    "Vidas": [
        [os.path.join("textures", "Sem.png"), 0], 
        [os.path.join("textures", "Tem.png"), 0]
    ]
}

texturas_GameOver = {
    "game_over" : [os.path.join("textures", "game_over.png"), 0], 
    "try_again" : [os.path.join("textures", "try_again.png"), 0]
}

# Constantes para iluminação
lightAmbient = glm.vec3(0.1)    # Ia
surfaceAmbient = glm.vec3(0.1)  # Ka
lightPosition = glm.vec3(0, 10, 10)

cor_para_numero = {
    (0.1, 0.1, 0.1): 0,
    (1.0, 0.0, 0.0): 1,  # Vermelho
    (0.0, 1.0, 0.0): 2,  # Verde
    (0.0, 0.0, 1.0): 3   # Azul
}

matriz_cores = {
    chave: [[(0.1, 0.1, 0.1) for _ in range(NUM_COLUNAS)] for _ in range(NUM_LINHAS)] for chave in range(1, int(max_segmento + 1))   # Branco por padrão
}

segmentos_matrizes = {}
coordenadas_obstaculos = []
obstaculo1 = None
obstaculo2 = None
obstaculo3 = None

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