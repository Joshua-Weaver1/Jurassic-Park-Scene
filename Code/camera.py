# pygame is just used to create a window with the operating system on which to draw.
import pygame

# imports all openGL functions
from OpenGL.GL import *
from OpenGL.GLU import *

# we will use numpy to store data in arrays
import numpy as np

# import a bunch of useful matrix functions (for translation, scaling etc)
from matutils import *


class Camera:
    '''
    Base class for handling the camera.
    '''
    def __init__(self, size):
        self.size = size
        self.V = np.identity(4)
        self.distance = 5.0
        self.phi = 0.0
        self.psi = 0.0
        self.center = np.zeros(3)

    def update(self):
        '''
        This method must be called before rendering to update the V matrix according to whatever changes in the
        camera parameters occurred. 
        '''

        # === WS3: Calculate V ===

        # first, we can move the centre of 
        T = translationMatrix(-self.center)
        
        # second, we rotate first around y, then around x
        R = np.matmul( rotationMatrixX(self.psi), rotationMatrixY(self.phi) )

        # last, we move the camera away from the origin, looking back
        D = translationMatrix([0, 0, -self.distance])

        # we combine all transfomations, note the ordering
        self.V = np.matmul( D, np.matmul(R,T) )
        # === End WS3 ===

        pass