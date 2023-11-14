# Desc: Main file for the Jurassic Park Scene

# OpenGL is used for the graphics
from OpenGL.GL import *
# pygame is used for the windowing and event handling
import pygame
# numpy is used for the matrix math
import numpy as np

class Scene:
    """
    The scene class. This class holds all objects in the scene and renders them.
    """
    def __init__(self):
        """
        Initialize the scene.
        """

        self.window_size = (1280,720)

        # Initialize pygame
        pygame.init()
        # Create a window
        window = pygame.display.set_mode(self.window_size, pygame.OPENGL|pygame.DOUBLEBUF, 24)

        # Initialize OpenGL
        glViewport(0, 0, self.window_size[0], self.window_size[1])
        glClearColor(0.0, 0.5, 0.5, 1.0)

        self.camera = Camera(self.window_size)

        # The objects in the scene
        self.objects = []

    def add_object(self, obj):
        """
        Add an object to the scene.
        obj: The object to add.
        return: None
        """
        self.objects.append(obj)

    def render(self):
        """
        Render all objects in the scene using OpenGL.
        return: None
        """

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # saves the current position
        glPushMatrix()

        # apply the camera parameters
        self.camera.set_cam_parameters()

        # Render all objects
        for obj in self.objects:
            obj.render()

        # retrieve the last saved position
        glPopMatrix()
        
        # Swap the buffers
        pygame.display.flip()

    def key_event(self, event):
        if event.key == pygame.K_q:
            self.running = False

        elif event.key == pygame.K_0:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);

        elif event.key == pygame.K_1:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);


        self.camera.key_event(event)

    def start(self):
        """
        Start the scene.
        return: None
        """

        # Start the scene
        self.in_use = True
        while self.in_use:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.in_use = False
                # keyboard events
                elif event.type == pygame.KEYDOWN:
                    self.key_event(event)

                elif event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        dx, dy = event.rel
                        self.camera.position[0] -= dx / self.window_size[0] /10 - 0.5
                        self.camera.position[1] -= dy / self.window_size[1] /10- 0.5

            # Render the scene
            self.render()

class SimpleObject:
    """
    A simple object is a collection of vertices that can be rendered.
    """

    def __init__(self, translation=[0,0,0], rotation=0, size=1, color=[1,1,1]):
        '''
        Initialises the model data
        '''

        # variables for storing the parameters
        self.color = color
        self.translation = translation
        self.rotation = rotation
        self.size = size


    def set_obj_params(self):
        """
        Sets the params of the object
        :return: None
        """
        
        glTranslate(*self.translation)
        glRotate(self.rotation, 0, 0, 1)
        # 3 params for x, y, z
        glScale(self.size, self.size, self.size)
        glColor(self.color)

    def render(self):
        '''
        Renders the object using OpenGL
        :return: None
        '''

        # saves the current parameters
        glPushMatrix()

        self.set_obj_params()

        # we use the GL_TRIANGLES primitive to draw the model
        glBegin(GL_TRIANGLES)

        # iterate over all vertices
        for vertex in self.vertices:

            # the glVertex function takes a single vertex as parameter and adds
            # the vertex to the list.
            glVertex(vertex)

        # end the batch (we are done drawing now)
        glEnd()

        # restore the previous parameters
        glPopMatrix()

        def applyPose(self):
            # apply the translation, rotation and size of the object
            glTranslate(*self.translation)
            glRotate(self.rotation, 0, 0, 1)
            glScale(self.size, self.size, self.size)
            glColor(self.color)

class TriangleObj(SimpleObject):
    '''
    A simple triangle object
    '''
    def __init__(self, translation=[0, 0, 0], rotation=0, size=1, color=[1, 1, 1]):
        SimpleObject.__init__(self, translation=translation, rotation=rotation, size=size, color=color)

        # each row encodes the coordinate for one vertex.
        # given that we are drawing in 2D, the last coordinate is always zero.
        self.vertices = np.array(
            [
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0],
                [1.0, 1.0, 0.0]
            ], 'f')

class TreeObj(SimpleObject):
    def __init__(self, translation=[0,0,0], rotation=0, size=1):
        SimpleObject.__init__(self, translation=translation, rotation=rotation, size=size)

        # the tree consists of multiple components
        self.components = [
            TriangleObj(translation=[0, 0, 0], size=0.5, rotation=-45, color=[0, 1, 0]),
            TriangleObj(translation=[0, 0.25, 0], size=0.5, rotation=-45, color=[0, 1, 0]),
            TriangleObj(translation=[0, 0.5, 0], size=0.5, rotation=-45, color=[0, 1, 0]),
            TriangleObj(translation=[0.25, -0.25, 0], size=0.25, rotation=0, color=[0.6, 0.2, 0.2]),
            TriangleObj(translation=[0.5, 0, 0], size=0.25, rotation=-180, color=[0.6, 0.2, 0.2])
        ]

    def render(self):
        """
        Renders the object using OpenGL
        :return: None
        """
        glPushMatrix()

        # apply the parameters for the whole model
        self.set_obj_params()

        # draw all component primitives
        for component in self.components:
            component.render()

        glPopMatrix()

class Camera:
    '''
    Basic class for handling the camera pose. At this stage, just x and y offsets.
    '''
    def __init__(self,size):
        self.size = size
        self.position = [0.0,0.0,0.0]

    def set_cam_parameters(self):
        '''
        Apply the camera parameters to the current OpenGL context
        Note that this is the old fashioned API, we will use matrices in the
        future.
        '''
        glTranslate(*self.position)

    def key_event(self, event):
        '''
        Handles keyboard events that are related to the camera.
        '''
        if event.key == pygame.K_PAGEDOWN:
            self.position[2] += 0.01

        if event.key == pygame.K_PAGEUP:
            self.position[2] -= 0.01

        if event.key == pygame.K_DOWN:
            self.position[1] += 0.01

        if event.key == pygame.K_UP:
            self.position[1] -= 0.01

        if event.key == pygame.K_LEFT:
            self.position[0] += 0.01

        if event.key == pygame.K_RIGHT:
            self.position[0] -= 0.01

if __name__ == '__main__':
    """
    This is the main function. It creates a scene and adds a few objects to it.
    """
    # creates a new scene
    scene = Scene()

    # adds a tree to the scene
    scene.add_object(TreeObj(translation=[0,0,0]))

    # start the scene
    scene.start()