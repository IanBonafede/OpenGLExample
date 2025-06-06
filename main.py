from OpenGL import GL
import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

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
        #depthtest
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
        

        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        self.cube = Cube(
            position = [0,0,-3], 
            eulers=[0,0,0]
            )
        self.cube_mesh = CubeMesh()
        self.wood_texture = Material("gfx/wood.jpg")

        #initialize our projection view using pyrr
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=640/480,
            near=0.1, far=10, dtype=np.float32
            )

        #set projection in opengl
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1, GL_FALSE, projection_transform
            )

        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")

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

            

            #update cube
            self.cube.eulers[2] += 0.2
            if(self.cube.eulers[2] > 360):
                self.cube.eulers[2] -= 360

            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glUseProgram(self.shader) # use correct shader
            self.wood_texture.use()

            #create tranform matrix
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            #matrix = identy of position and eulers
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_eulers(
                    eulers= np.radians(self.cube.eulers),
                    dtype=np.float32
                    )
                )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec= self.cube.position,
                    dtype=np.float32
                    )
                )
            #upload transform
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            glBindVertexArray(self.cube_mesh.vao) # prepare vertex
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count) #draw arrays (triangles, first point, # points)

            pg.display.flip()

            #timing
            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.cube_mesh.destroy()
        self.wood_texture.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

class Cube:

    def __init__(self, position, eulers):

        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

class CubeMesh:

    def __init__(self):

        # x, y, z, s, t
        self.vertices = (
            -0.5, -0.5, -0.5, 0, 0,
             0.5, -0.5, -0.5, 1, 0,
             0.5,  0.5, -0.5, 1, 1,

             0.5,  0.5, -0.5, 1, 1,
            -0.5,  0.5, -0.5, 0, 1,
            -0.5, -0.5, -0.5, 0, 0,

            -0.5, -0.5,  0.5, 0, 0,
             0.5, -0.5,  0.5, 1, 0,
             0.5,  0.5,  0.5, 1, 1,

             0.5,  0.5,  0.5, 1, 1,
            -0.5,  0.5,  0.5, 0, 1,
            -0.5, -0.5,  0.5, 0, 0,

            -0.5,  0.5,  0.5, 1, 0,
            -0.5,  0.5, -0.5, 1, 1,
            -0.5, -0.5, -0.5, 0, 1,

            -0.5, -0.5, -0.5, 0, 1,
            -0.5, -0.5,  0.5, 0, 0,
            -0.5,  0.5,  0.5, 1, 0,

             0.5,  0.5,  0.5, 1, 0,
             0.5,  0.5, -0.5, 1, 1,
             0.5, -0.5, -0.5, 0, 1,

             0.5, -0.5, -0.5, 0, 1,
             0.5, -0.5,  0.5, 0, 0,
             0.5,  0.5,  0.5, 1, 0,

            -0.5, -0.5, -0.5, 0, 1,
             0.5, -0.5, -0.5, 1, 1,
             0.5, -0.5,  0.5, 1, 0,

             0.5, -0.5,  0.5, 1, 0,
            -0.5, -0.5,  0.5, 0, 0,
            -0.5, -0.5, -0.5, 0, 1,

            -0.5,  0.5, -0.5, 0, 1,
             0.5,  0.5, -0.5, 1, 1,
             0.5,  0.5,  0.5, 1, 0,

             0.5,  0.5,  0.5, 1, 0,
            -0.5,  0.5,  0.5, 0, 0,
            -0.5,  0.5, -0.5, 0, 1

        )

        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = len(self.vertices) // 5

        self.vao = glGenVertexArrays(1) # Vertex Attribute Array
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        #glBufferData( GL_ARRAY_BUFFER, sizeof( self.vertices[0] * 3 ), &vertices[0], GL_STATIC_DRAW );

        #enable attribute
        glEnableVertexAttribArray(0) 
        #attrib = position
        #define attribute
        # 0 = position, 3 points in attrib, float type, normalize numbers?, stride = 5#s x 4 bytes = 20, offset for first point 0 
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0)) 


        glEnableVertexAttribArray(1) 
        #attrib = coordinate
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))

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
