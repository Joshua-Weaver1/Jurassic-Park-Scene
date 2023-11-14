# pygame is just used to create a window with the operating system on which to draw.
import pygame

# imports all openGL functions
from OpenGL.GL import *
from OpenGL.GLU import *

# we will use numpy to store data in arrays
import numpy as np

# we will use numpy to store data in arrays
import numpy as np

# import the shader class
from shaders import Shaders

# import the camera class
from camera import Camera

# import the scene class
from scene import Scene

# and we import a bunch of helper functions
from matutils import *

class BaseModel:
    '''
    Base class for all models, implementing the basic draw function for triangular meshes.
    Inherit from this to create new models.
    '''

    def __init__(self, scene, M, color=[1,1,1], primitive=GL_TRIANGLES):
        '''
        Initialises the model data
        '''

        print('+ Initializing {}'.format(self.__class__.__name__))

        self.scene = scene

        self.primitive = primitive

        # store the object's color
        self.color = color

        # store the position of the model in the scene, ...
        self.M = M

    def bind(self):
        '''
        This method stores the vertex data in a Vertex Buffer Object (VBO) that can be uploaded
        to the GPU at render time.
        '''
        # create a buffer object
        self.vbo = glGenBuffers(1)

        # bind the buffer so that following operations will affect it
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        # and we set the data in the buffer as the vertex array
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)


    def draw(self, Mp):
        '''
        Draws the model using OpenGL functions
        :return:
        '''

        #print('Drawing {}'.format(self.__class__.__name__))

        # then set the colour
        glColor(self.color)

        # setup the shader program and provide it the Model, View and Projection matrices to use
        # for rendering this model
        self.scene.shaders.bind(M=np.matmul(Mp, self.M), V=self.scene.camera.V, P=self.scene.P)

        # bind the buffer so that the following operations affect it
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        # bind the location of the vertex position in the GLSL program to the location zero
        # the name of the location must correspond to a 'in' variable in the GLSL vertex shader code
        vertex_loc = glGetAttribLocation(program=self.scene.shaders.program, name='position')

        # Associate the bound buffer to the corresponding input location in the shader
        # Each instance of the vertex shader will get one row of the array
        # so this can be processed in parallel!
        glVertexAttribPointer(index=vertex_loc, size=self.vertices.shape[1], type=GL_FLOAT, normalized=False, stride=0, pointer=None)
        glEnableVertexAttribArray(vertex_loc)

        # draw the data in the buffer using the GL_TRIANGLES primitive
        glDrawArrays(self.primitive, 0, self.vertices.shape[0])

        self.scene.shaders.unbind()

class TriangleModel(BaseModel):
    '''
    A very simple model for drawing a single triangle. This is only for illustration purpose.
    '''
    def __init__(self, scene, M, color=[1, 1, 1]):
        BaseModel.__init__(self, scene, M=M, color=color)

        # each row encodes the coordinate for one vertex.
        # given that we are drawing in 2D, the last coordinate is always zero.
        self.vertices = np.array(
            [
                [0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [1.0, 0.0, 0.0]
            ], 'f')
        self.bind()

class FlatTriangleModel(BaseModel):
    '''
    A very simple model for drawing a single triangle. This is only for illustration purpose.
    '''
    def __init__(self, scene, M, color=[1, 1, 1]):
        BaseModel.__init__(self, scene, M=M, color=color)

        # each row encodes the coordinate for one vertex.
        # given that we are drawing in 2D, the last coordinate is always zero.
        self.vertices = np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 0.0, 1.0]
            ], 'f')
        self.bind()

class ComplexModel(BaseModel):
    def draw(self, Mp):
        # draw all component primitives
        for component in self.components:
            component.draw(np.matmul(Mp, self.M))

class SquareModel(BaseModel):
    def __init__(self, scene, M, color=[1, 1, 1]):
        BaseModel.__init__(self, scene, M=M, color=color, primitive=GL_QUADS)
        self.vertices = np.array([
            [0., 0., 0.],
            [1., 0., 0.],
            [1., 1., 0.],
            [0., 1., 0.]
        ], 'f')
        self.bind()

class TreeModel(ComplexModel):
    def __init__(self, scene, M ):
        BaseModel.__init__(self, scene=scene, M=M)

        # list of simple components
        self.components = [
            SquareModel(scene, M=poseMatrix(position=[-0.125, 0., 0], scale=[0.25,0.5,1.], orientation=0), color=[0.6, 0.2, 0.2]),
            TriangleModel(scene, M=poseMatrix(position=[0, 0.5, 0], scale=[0.25,0.5,1]), color=[0, 1, 0]),
            TriangleModel(scene, M=poseMatrix(position=[0, 0.5, 0], scale=[-0.25,0.5,1]), color=[0, 1, 0]),
            TriangleModel(scene, M=poseMatrix(position=[0, 0.75, 0], scale=[0.25, 0.5, 1]), color=[0, 1, 0]),
            TriangleModel(scene, M=poseMatrix(position=[0, 0.75, 0], scale=[-0.25, 0.5, 1]), color=[0, 1, 0]),
            TriangleModel(scene, M=poseMatrix(position=[0, 1.0, 0], scale=[0.25, 0.5, 1]), color=[0, 1, 0]),
            TriangleModel(scene, M=poseMatrix(position=[0, 1.0, 0], scale=[-0.25, 0.5, 1]), color=[0, 1, 0]),
        ]

class HouseModel(ComplexModel):
    def __init__(self, scene, M):
        BaseModel.__init__(self, scene, M=M)

        # list of simple components
        self.components = [
            SquareModel(scene, M=poseMatrix(position=[0, 0, 0], scale=0.5, orientation=0), color=[0.9, 0.9, 0.9]),
            TriangleModel(scene, M=poseMatrix(position=[0.25, 0.5, 0], scale=0.25), color=[0.9, 0.1, 0]),
            TriangleModel(scene, M=poseMatrix(position=[0.25, 0.5, 0], scale=[-0.25,0.25,1]), color=[0.9, 0.1, 0]),
            SquareModel(scene, M=poseMatrix(position=[0.05, 0.25, 0], scale=0.15), color=[0.7, 0.7, 0.9]),
            SquareModel(scene, M=poseMatrix(position=[0.30, 0.25, 0], scale=0.15), color=[0.7, 0.7, 0.9]),
            SquareModel(scene, M=poseMatrix(position=[0.20, 0., 0], scale=[0.1,0.2,1.]), color=[0.6, 0.2, 0.2]),
        ]

if __name__ == '__main__':
    # initialises the scene object
    scene = Scene()

    # adds a few objects to the scene
    scene.add_model(TreeModel(scene, M=poseMatrix(position=[0.4, 0., -1], scale=0.5)))
    scene.add_model(TreeModel(scene, M=poseMatrix(position=[0.7, 0, -4], scale=0.5)))
    scene.add_model(TreeModel(scene, M=poseMatrix(position=[0.3, 0, -3], scale=0.5)))
    scene.add_model(TreeModel(scene, M=poseMatrix(position=[-0.1, 0, -2], scale=0.5)))
    scene.add_model(HouseModel(scene, M=poseMatrix(position=[-0.9, 0, -1])))

    # starts drawing the scene
    scene.run()
