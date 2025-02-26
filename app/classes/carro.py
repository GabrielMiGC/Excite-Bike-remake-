from OpenGL.GL import *
from OpenGL.GLU import *
from util import load_obj_car, shading
import glm

class Carro:
    
    def __init__(self, x, y, largura, altura, position=None):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.position = position
        self.vertices, _, self.normals, self.faces = load_obj_car('app/objetos/car.obj')
        self.lightDiffuse = glm.vec3(1.0)      # Id               
        self.surfaceDiffuse = glm.vec3(1.0)    # Kd       
        self.lightSpecular = glm.vec3(1.0)     # Is
        self.surfaceSpecular = glm.vec3(0.5)   # Ks               
        self.surfaceShine = 250    

    def desenhar(self):
        """Desenha o carro"""
        
        color_map = {
            'Black': glm.vec3(0, 0, 0),  # Preto
            'Body': glm.vec3(1.0, 0.0, 0.0),    # Vermelho
            'Bottom': glm.vec3(0.0, 0.0, 0.0),    # Preto
            'Bumpers': glm.vec3(0.46, 0.46, 0.46),    # Branca
            'Lights': glm.vec3(1.0, 1.0, 0.0),    # Amarelo
            'Tires': glm.vec3(0, 0, 0),    # Preto
            'Wheels': glm.vec3(0.46, 0.46, 0.46),    # Cinza
            'Window': glm.vec3(0.46, 0.46, 0.46),    # Cinza
        }
        
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glPushMatrix()        
        
        # Desenha o carro
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
