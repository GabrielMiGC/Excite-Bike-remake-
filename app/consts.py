
tela ="criacao"
botao_selecionado = (0.1, 0.1, 0.1)

NUM_LINHAS = 3
NUM_COLUNAS = 10

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

matriz_exported = None

posicoes_camera = [
    (0, 10, 0,   0, 0, 10,   0, 1, 0), #terceira pessoa
    (10, 10, 0,  0, 0, 10,   0, 1, 0), #canto superior esquerdo (atrás)
    (0, 5, 0,    0, 6, 10,   0, 1, 0), # primeira pessoa
    (-10, 10,0,  0, 0, 10,   0, 1, 0), #canto superior direito (atrás)
    (0, 6, 10,  5, 5, 0,   0, 1, 0)  # visão lateral (2D)
]
index_camera_atual = 0

