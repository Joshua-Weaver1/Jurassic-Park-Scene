# Desc: Main file for the Jurassic Park game

# OpenGL is used for the graphics
from OpenGL.GL import *
# pygame is used for the windowing and event handling
import pygame
# numpy is used for the matrix math
import numpy as np

class Scene:
    """
    A scene is a collection of objects to be rendered.
    """
    def __init__(self):
        """
        Initialize the scene.
        """

        # Initialize pygame
        pygame.init()
        # Create a window
        screen = pygame.display.set_mode((640,480), pygame.OPENGL|pygame.DOUBLEBUF, 24)

        # Initialize OpenGL
        glViewport(0, 0, 640, 480)
        glClearColor(0.0, 0.5, 0.5, 1.0)

        # The objects in the scene
        self.objects = []

    def add_object(self, obj):
        """
        Add an object to the scene.
        """
        self.objects.append(obj)

    def render(self):
        """
        Render all objects in the scene.
        """

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # Render all objects
        for obj in self.objects:
            obj.render()
        
        # Swap the buffers
        pygame.display.flip()

    def start(self):
        """
        Start the scene.
        """

        # Start the scene
        in_use = True
        while in_use:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_use = False

            # Render the scene
            self.render()

class SimpleObject:
    """
    A simple object is a collection of vertices that can be rendered.
    """

    def __init__(self, position=[0,0,0], orientation=0, scale=1, color=[1,1,1]):
        '''
        Initialises the model data
        '''

        self.color = color
        self.position = position
        self.orientation = orientation
        self.scale = scale


    def applyParameters(self):
        # apply the position and orientation of the object
        glTranslate(*self.position)
        glRotate(self.orientation, 0, 0, 1)

        # apply scaling across all dimensions
        glScale(self.scale, self.scale, self.scale)

        # then set the colour
        glColor(self.color)

    def render(self):
        '''
        Draws the model using OpenGL functions
        :return:
        '''

        # saves the current pose parameters
        glPushMatrix()

        self.applyParameters()

        # Here we will use the simple GL_TRIANGLES primitive, that will interpret each sequence of
        # 3 vertices as defining a triangle.
        glBegin(GL_TRIANGLES)

        # we loop over all vertices in the model
        for vertex in self.vertices:

            # This function adds the vertex to the list
            glVertex(vertex)

        # the call to glEnd() signifies that all vertices have been entered.
        glEnd()

        # retrieve the previous pose parameters
        glPopMatrix()

        def applyPose(self):
            # apply the position and orientation and size of the object
            glTranslate(*self.position)
            glRotate(self.orientation, 0, 0, 1)
            glScale(self.scale, self.scale, self.scale)
            glColor(self.color)

class TriangleModel(SimpleObject):
    '''
    A very simple model for drawing a single triangle. This is only for illustration purpose.
    '''
    def __init__(self, position=[0, 0, 0], orientation=0, scale=1, color=[1, 1, 1]):
        SimpleObject.__init__(self, position=position, orientation=orientation, scale=scale, color=color)

        # each row encodes the coordinate for one vertex.
        # given that we are drawing in 2D, the last coordinate is always zero.
        self.vertices = np.array(
            [
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0],
                [1.0, 1.0, 0.0]
            ], 'f')

class ComplexModel(SimpleObject):
    def __init__(self, position=[0,0,0], orientation=0, scale=1):
        SimpleObject.__init__(self, position=position, orientation=orientation, scale=scale)

        # list of simple components
        self.components = [
            TriangleModel(position=[0, 0, 0], scale=0.5, orientation=-45, color=[0, 1, 0]),
            TriangleModel(position=[0, 0.25, 0], scale=0.5, orientation=-45, color=[0, 1, 0]),
            TriangleModel(position=[0, 0.5, 0], scale=0.5, orientation=-45, color=[0, 1, 0]),
            TriangleModel(position=[0.25, -0.25, 0], scale=0.25, orientation=0, color=[0.6, 0.2, 0.2]),
            TriangleModel(position=[0.5, 0, 0], scale=0.25, orientation=-180, color=[0.6, 0.2, 0.2])
        ]

    def render(self):
        glPushMatrix()

        # apply the parameters for the whole model
        self.applyParameters()

        # draw all component primitives
        for component in self.components:
            component.render()

        glPopMatrix()

if __name__ == '__main__':
    # initialises the scene object
    scene = Scene()

    # adds a few objects to the scene
    scene.add_object(ComplexModel(position=[0,0,0]))

    # starts drawing the scene
    scene.start()