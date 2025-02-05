from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np

class Renderer:
    def __init__(self, cube_textures):
        self.cube_textures = cube_textures
        self.textures = self.load_textures(cube_textures)
        self.cube_vertices = [
            [-10, -10, -10],    
            [10, -10, -10],     
            [10, 10, -10],    
            [-10, 10, -10],     
            [-10, -10, 10], 
            [10, -10, 10],  
            [10, 10, 10],   
            [-10, 10, 10],
        ]

        
        self.cube_faces = [
            (0, 1, 2, 3),  # back face
            (3, 2, 6, 7),  # top face
            (7, 6, 5, 4),  # front face
            (4, 5, 1, 0),  # bottom face
            (1, 5, 6, 2),  # right face
            (4, 0, 3, 7),  # left face
        ]

    def load_textures(self, texture_paths):
        textures = glGenTextures(len(texture_paths))
        for i, path in enumerate(texture_paths):
            glBindTexture(GL_TEXTURE_2D, textures[i])
            image = Image.open(path).convert("RGB")  # Converte para RGB
            img_data = np.array(image, dtype=np.uint8)  # Ajusta o formato

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)  
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        return textures


    def draw_cube(self):
        glBegin(GL_QUADS)
        for i, face in enumerate(self.cube_faces):
            glBindTexture(GL_TEXTURE_2D, self.textures[i])

            for vertex in face:
                glTexCoord2f(vertex % 2, (vertex // 2) % 2)
                glVertex3fv(np.array(self.cube_vertices[vertex], dtype=np.float32))


        glDisable(GL_TEXTURE_2D)
        glEnd()