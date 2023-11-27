# Description: This file contains the Scene class, which is used to represent a scene in the program.

# pygame is used to create a window on which to draw.
import pygame

# This imports all openGL functions
from OpenGL.GL import *

# import the shader class
from shaders import *

# import the camera class
from camera import Camera

# and we import a bunch of helper functions
from matutils import *

# imports the lightsource class
from lightSource import LightSource

class Scene:
    """
    This class represents a scene, which is a collection of models to draw.
    """
    def __init__(self, width=800, height=600, shaders=None):
        """
        Initialises the scene.
        :param width: the width of the window
        :param height: the height of the window
        """

        # set the window size
        self.window_size = (width, height)

        # variable to change scene to a wireframe, wireframe mode is off by default
        self.wireframe = False

        # initialise pygame window
        pygame.init()
        screen = pygame.display.set_mode(self.window_size, pygame.OPENGL | pygame.DOUBLEBUF, 24)

        # start initialising the window from the OpenGL side
        glViewport(0, 0, self.window_size[0], self.window_size[1])

        # this selects the background color
        # divides the RGB values by 255 to get the color in the range [0,1] 
        glClearColor(119/255, 136/255, 153/255, 1.0)

        # enable back face culling
        glEnable(GL_CULL_FACE)

        # enable the vertex array capability
        glEnableClientState(GL_VERTEX_ARRAY)

        # enable depth test for clean output
        glEnable(GL_DEPTH_TEST)

        # set the default shader program
        self.shaders = 'flat'

        # initialise the projective transform
        near = 1.0
        # need a sufficiently large far plane to avoid clipping
        far = 100.0
        left = -1.0
        right = 1.0
        top = -1.0
        bottom = 1.0

        # cycle through models
        self.show_model = -1

        # to start with, we use an orthographic projection
        self.P = frustumMatrix(left, right, top, bottom, near, far)

        # initialises the camera object
        self.camera = Camera()

        # initialise the light source
        self.light = LightSource(self, position=[5., 5., 5.])

        # rendering mode for the shaders
        self.mode = 1  # initialise to full interpolated shading

        # an array the class will maintain to hold a list of models to draw in the scene
        self.models = []

    def add_model(self, model):
        """
        This method adds a model to the scene.
        :param model: The model object to add to the scene
        :return: None
        """
        
        # and add to the list
        self.models.append(model)

    def add_models_list(self, models_list):
        """
        Method to add a model to the scene.
        :param model: The model object to add to the scene
        :return: None
        """
        for model in models_list:
            self.add_model(model)

    def draw(self, framebuffer=False):
        '''
        Draw all models in the scene
        :param framebuffer: if True, we do not clear the screen and do not flip the buffers
        :return: None
        '''

        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        if not framebuffer:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # ensure that the camera view matrix is up to date
            self.camera.update()

        # then we loop over all models in the list and draw them
        for model in self.models:
            model.draw()

        # draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

    def keyboard(self, event):
        """
        Method to process keyboard events. Check Pygame documentation for a list of key events
        :param event: the event object that was raised
        """
        # if the key pressed is the escape key, we exit the program
        if event.key == pygame.K_q:
            self.running = False

        # flag to switch wireframe rendering
        elif event.key == pygame.K_0:
            if self.wireframe:
                print('--> Rendering using colour fill')
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                self.wireframe = False
            else:
                print('--> Rendering using colour wireframe')
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                self.wireframe = True

    def pygameEvents(self):
        """
        Method to process pygame events (keyboard, mouse, etc) and update the scene accordingly.
        :return: None
        """
        # check whether the window has been closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # keyboard events
            elif event.type == pygame.KEYDOWN:
                self.keyboard(event)

            # mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mods = pygame.key.get_mods()
                if event.button == 4:
                    #pass
                    if mods & pygame.KMOD_CTRL:
                        self.light.position *= 1.1
                        self.light.update()
                    else:
                        self.camera.distance = max(1, self.camera.distance - 1)

                elif event.button == 5:
                    #pass
                    if mods & pygame.KMOD_CTRL:
                        self.light.position *= 0.9
                        self.light.update()
                    else:
                        self.camera.distance += 1
            # mouse motion
            elif event.type == pygame.MOUSEMOTION:
                # check whether the left mouse button is pressed
                if pygame.mouse.get_pressed()[0]:
                    if self.mouse_mvt is not None:
                        self.mouse_mvt = pygame.mouse.get_rel()
                        self.camera.center[0] -= (float(self.mouse_mvt[0]) / self.window_size[0])
                        self.camera.center[1] -= (float(self.mouse_mvt[1]) / self.window_size[1])
                    else:
                        self.mouse_mvt = pygame.mouse.get_rel()

                # check whether the right mouse button is pressed
                elif pygame.mouse.get_pressed()[2]:
                    if self.mouse_mvt is not None:
                        self.mouse_mvt = pygame.mouse.get_rel()
                        self.camera.phi -= (float(self.mouse_mvt[0]) / self.window_size[0])
                        self.camera.psi -= (float(self.mouse_mvt[1]) / self.window_size[1])
                    else:
                        self.mouse_mvt = pygame.mouse.get_rel()
                else:
                    self.mouse_mvt = None

    def run(self):
        """
        Method to run the scene.
        :return: None
        """

        # program loop
        self.running = True
        while self.running:

            self.pygameEvents()

            # otherwise, continue drawing
            self.draw()