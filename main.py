import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import re

assets_Directory = "./Assets/"
file_name = "Demo.obj"

class ReadDocument:

    def __init__(self,name_by_document):
        self.__name = name_by_document

    def Vericies(self):
        with open(assets_Directory+self.__name) as self.__faces_file:
            self.__faces_line = [line.strip('\n') for line in self.__faces_file] #Almacena valores quitando caracteres de salto de linea
            self.__faces_line_2 = self.__faces_line[3:] # Salta las primeras filas de informacion del formato ".obj"
            self.__faces_line.clear() #Limpieza de la primera lista
            self.__faces = []
            self.__faces_2 = []

            """ Separacion de indicadores v y vn y asignamiento a una lista nueva"""
            for data in self.__faces_line_2:
                for word in data:
                    if(word == 'v'):
                        self.__faces_line.append(data)     

            self.__faces_line_2.clear() #Limpieza de lista

            """ Separamiento de los valores v """
            for data in self.__faces_line:
                if data[0] == 'v' and data[1] == ' ':
                    self.__faces_line_2.append(data)

            self.__faces_line.clear()

            """ Separacion de las lineas guia  """
            self.__faces = [line.replace('v ','')for line in self.__faces_line_2]
            self.__faces_line_2.clear()

            """ Separacion por espacios usando biblioteca externa "re.split" """
            for data in self.__faces:
                self.__faces_2.append(re.split(' ',str(data)))

            self.__faces.clear()

            """ Separacion de valores en espacio de lista diferentes """
            for data in self.__faces_2:
                for x in data:
                    self.__faces.append(x)

            self.__faces_2.clear()

            """ Conversion de str a flotante en valores independientes asignados a una lista re utilizada """
            self.__faces_2 = [float(i) for i in self.__faces]

            """ Conversion a cordenadas X,Y,Z """
            self.__faces_2 =  tuple(zip(*(self.__faces_2[i::3] for i in range(3))))

            return self.__faces_2

    def Edges(self):
        with open(assets_Directory+self.__name) as self.__edges_file:
            self.__lines = [line.strip('\n') for line in self.__edges_file]
            self.__lines_2 = self.__lines[3:]
            self.__lines_3 = []
            self.__lines_4 = []
            self.__edges = []

            for data in self.__lines_2:
                for word in data:
                    if(word == 'f'):
                        self.__lines_4.append(data)
            
            for data in self.__lines_4:
                if data[0] == "f":
                    self.__lines_3.append(data)

            self.__lines_3 = [line.replace("f ","").replace("//","").replace(" ","") for line in self.__lines_3]

            for data in self.__lines_3:
                for x in data:
                    self.__edges.append(x)

            self.__edges = tuple(map(int,self.__edges))
            self.__edges = tuple(zip(*(self.__edges[i::3] for i in range(3))))

            """ Clear Variables """

            self.__lines = ''
            self.__lines_1 = ''
            self.__lines_2 = ''
            self.__lines_3.clear()
            self.__lines_4.clear()

            """ End """

            return self.__edges
                 
def Figura():
    glBegin(GL_TRIANGLES)
    for edge in ReadDocument(file_name).Edges():
        for vertex in edge:
            glVertex3fv(ReadDocument(file_name).Vericies()[vertex - 1])
    glEnd()

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0,-5)

    glRotatef(0,0,0,0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glRotatef(1,49,-80,5)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Figura()
        pygame.display.flip()
        pygame.time.wait(10)


if(__name__ == "__main__"):
    main()