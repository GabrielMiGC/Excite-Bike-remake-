from OpenGL.GL import *
from OpenGL.GLU import *
from classes.barreira import *
from util import shading, load_obj
import glm
import consts

class Moto:
    def __init__(self):
        self.vertices, _, self.normals, self.faces = load_obj('app/objetos/motoSimples.obj')
        self.lightDiffuse = glm.vec3(1.0)      # Id               
        self.surfaceDiffuse = glm.vec3(1.0)    # Kd       
        self.lightSpecular = glm.vec3(1.0)     # Is
        self.surfaceSpecular = glm.vec3(0.5)   # Ks               
        self.surfaceShine = 250 
        
    def desenhar(self):
        
        color_map = {
            'engine': glm.vec3(0.46, 0.46, 0.46),  # Cinza
            'tire': glm.vec3(0.0, 0.0, 0.0),    # Preto
            'tank': glm.vec3(0.0, 0.0, 1.0),    # Azul
            'plate': glm.vec3(1.0, 1.0, 1.0),    # Branca
            'exhaust': glm.vec3(0.46, 0.46, 0.46),    # Cinza
            'rear_light': glm.vec3(1.0, 1.0, 0.0),    # Amarelo
            'seat': glm.vec3(0.0, 0.0, 0.0),    # Preto
        }
        
        glPushMatrix()
        glTranslatef(consts.positionBike.x, consts.positionBike.y, consts.positionBike.z)
        
        # Desenha a moto
        for face in self.faces:
            if len(face) == 3:
                glBegin(GL_TRIANGLES)
            else:
                glBegin(GL_POLYGON)
                
            
            
            for vertex, _, normal, material in face:
                # Posição do vértice e normal
                point = glm.vec3(*self.vertices[vertex])  
                normal = glm.vec3(*self.normals[normal])  

                # Obtém a cor do material ou usa branco se não estiver no mapa
                base_color = color_map.get(material, glm.vec3(1.0, 1.0, 1.0))

                # Calcula a iluminação de Phong
                shade = shading(point, normal, self)

                # Multiplica a cor do material pela iluminação
                final_color = base_color * shade

                # Define a cor no OpenGL
                glColor3f(final_color.x, final_color.y, final_color.z)
                glVertex3f(*point)
            
            glEnd()

        glPopMatrix()