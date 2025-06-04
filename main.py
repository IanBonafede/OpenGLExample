import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader

class App:

    def __init__(self):

        #initialize python
        pg.init()
        pg.display.set_mode((640, 480), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        #initialize opengl
        glClearColor(0.1, 0.2, 0.2, 1)
        self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shader)

        self.triangle = Triangle()
        

        self.mainloop()

    def createShader(self, vertexFilepath, fragmentFilepath):

        with open(vertexFilepath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    def mainloop(self):

        running = True

        while(running):
            #check events
            for event in pg.event.get():
                if(event.type == pg.QUIT):
                    running = False

            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT)

            #draw triangle
            glUseProgram(self.shader) # use correct shader
            glBindVertexArray(self.triangle.vao) # prepare vertex
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count) #draw arrays (triangles, first point, # points)

            pg.display.flip()

            #timing
            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.triangle.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

class Triangle:

    def __init__(self):

        # x, y, z, r, g, b
        self.vertices = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            0.0, 0.5, 0.0, 0.0, 0.0, 1.0
        )

        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = 3

        self.vao = glGenVertexArrays(1) # Vertex Attribute Array
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        #glBufferData( GL_ARRAY_BUFFER, sizeof( self.vertices[0] * 3 ), &vertices[0], GL_STATIC_DRAW );

        #enable attribute
        glEnableVertexAttribArray(0) 
        #attrib 0 = position
        #define attribute
        # 0 = position, 3 points in attrib, float type, normalize numbers?, stride = 6#s x 4 bytes = 24, offset for first point 0 
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0)) 

        glEnableVertexAttribArray(1) 
        #attrib 1 = color
         # 1 = color, 3 points in attrib, float type, normalize numbers?, stride = 6#s x 4 bytes = 24, offset for first point 3#s x 4bytes = 12 bytes
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    def destroy(self):

        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


if __name__ == "__main__":
    myApp = App()
