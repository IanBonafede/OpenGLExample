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
        #aplha blend
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
        

        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        self.triangle = Triangle()
        self.wood_texture = Material("gfx/wood.jpg")
        self.cat_texture = Material("gfx/cat.png")

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
            #self.wood_texture.use()
            self.cat_texture.use()
            glBindVertexArray(self.triangle.vao) # prepare vertex
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count) #draw arrays (triangles, first point, # points)

            pg.display.flip()

            #timing
            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.triangle.destroy()
        self.wood_texture.destroy()
        self.cat_texture.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

class Triangle:

    def __init__(self):

        # x, y, z, r, g, b, s, t
        self.vertices = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
            0.0, 0.5, 0.0, 0.0, 0.0, 1.0, 0.5, 0.5
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
        # 0 = position, 3 points in attrib, float type, normalize numbers?, stride = 8#s x 4 bytes = 32, offset for first point 0 
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0)) 

        glEnableVertexAttribArray(1) 
        #attrib 1 = color
         # 1 = color, 3 points in attrib, float type, normalize numbers?, stride = 8#s x 4 bytes = 32, offset for first point 3#s x 4bytes = 12 bytes
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))

        glEnableVertexAttribArray(2) 
        #attrib 2 = coordinate
         # 1 = color, 3 points in attrib, float type, normalize numbers?, stride = 8#s x 4 bytes = 32, offset for first point 6#s x 4bytes = 24 bytes
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))

    def destroy(self):

        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))

class Material:

    def __init__(self, filepath):

        #1 texture in st format; S,T = U,V
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) #what is our wrapping mode?
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        #convert pygame image to opengl readable
        #image = pg.image.load(filepath).convert() # not working with alpha channel
        image = pg.image.load(filepath).convert_alpha()
        image_width, image_height = image.get_rect().size
        image_data = pg.image.tostring(image, "RGBA")
        #
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture,))

if __name__ == "__main__":
    myApp = App()
