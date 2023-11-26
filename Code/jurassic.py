# Desc: This file contains the main code for the Jurassic Park scene.

import pygame

# import the scene class
from cubeMap import FlattenCubeMap
from scene import Scene

from lightSource import LightSource

from blender import load_obj_file

from BaseModel import DrawModelFromMesh

from shaders import *

from ShadowMapping import *

from sphereModel import Sphere

from skyBox import *

from environmentMapping import *

class JurassicScene(Scene):
    """
    This class implements the Jurassic Park scene.
    """
    def __init__(self):
        """
        Initialises the scene.
        """
        Scene.__init__(self)

        # create the light source
        self.light = LightSource(self, position=[0., 4., 3.])
        # set the shader to use
        self.shaders='phong'

        # for shadow map rendering
        self.shadows = ShadowMap(light=self.light)
        self.show_shadow_map = ShowTexture(self, self.shadows)

        # load the models
        # draw a skybox
        self.skybox = SkyBox(scene=self)

        self.show_light = DrawModelFromMesh(scene=self, M=poseMatrix(position=self.light.position, scale=0.2), mesh=Sphere(material=Material(Ka=[10,10,10])), shader=FlatShader())

        self.environment = EnvironmentMappingTexture(width=400, height=400)

        self.sphere = DrawModelFromMesh(scene=self, M=poseMatrix(), mesh=Sphere(), shader=EnvironmentShader(map=self.environment))

        # triceratops
        tri = load_obj_file('models/TRIKERATOPS_CAGE_MODEL.obj')
        self.tri = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([0,-10,1]), scaleMatrix([0.15,0.15,0.15])), mesh=tri[0], shader=FlatShader())

        bunny = load_obj_file('models/city.obj')
        self.bunny = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([3,-11.5,9]), scaleMatrix([0.01,0.04,0.01])), mesh=bunny[0], shader=FlatShader())

        box = load_obj_file('models/postbox.obj')
        self.box = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([2,-10,-5]), scaleMatrix([10, 10, 10])), mesh=box[0], shader=PhongShader())

        r1 = load_obj_file('models/3Roads.obj')
        self.r1 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-1.7,-10, -1]), scaleMatrix([0.5, 0.5, 0.5])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        r2 = load_obj_file('models/3Roads.obj')
        self.r2 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-1.7,-10, 1]), scaleMatrix([0.5, 0.5, 0.5])), mesh=r2[0], shader=PhongShader())
        r3 = load_obj_file('models/3Roads.obj')
        self.r3 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-1.7,-10, 3]), scaleMatrix([0.5, 0.5, 0.5])), mesh=r3[0], shader=PhongShader())
        r4 = load_obj_file('models/3Roads.obj')
        self.r4 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-1.7,-10, 5]), scaleMatrix([0.5, 0.5, 0.5])), mesh=r4[0], shader=PhongShader())
        
        #show the flattened cube map
        self.flattened_cube = FlattenCubeMap(scene=self, cube=self.environment)

        # show the texture to the ticeratops
        self.show_texture = ShowTexture(self, Texture('triceratops_diffuse.bmp'))

    def draw_shadow_map(self):
        """
        Draw the shadow map.
        :return: None
        """

        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.tri.draw()

    def draw_reflections(self):
        """
        Draw the reflections.
        :return: None
        """

        self.skybox.draw()

        for model in self.models:
            model.draw()


    def draw(self, framebuffer=False):
        """
        Draw the scene.
        :param framebuffer: Whether to render to a framebuffer or not.
        :return: None
        """

        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # when using a framebuffer, we do not update the camera to allow for arbitrary viewpoint.
        if not framebuffer:
            self.camera.update()

        # first, we draw the skybox
        self.skybox.draw()

        # render the shadows
        self.shadows.render(self)

        # when rendering the framebuffer we ignore the reflective object
        if not framebuffer:

            self.environment.update(self)

            self.bunny.draw()
            self.tri.draw()
            self.box.draw()
            self.r1.draw()
            self.r2.draw()
            self.r3.draw()
            self.r4.draw()

            # if enabled, show flattened cube
            self.flattened_cube.draw()

            # if enabled, show texture
            self.show_texture.draw()

            self.show_shadow_map.draw()

        # then we loop over all models in the list and draw them
        for model in self.models:
            model.draw()

        self.show_light.draw()

        # flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

    def keyboard(self, event):
        """
        Handles keyboard events.
        :param event: The keyboard event.
        :return: None
        """

        Scene.keyboard(self, event)

        if event.key == pygame.K_c:
            if self.flattened_cube.visible:
                self.flattened_cube.visible = False
            else:
                print('--> showing cube map')
                self.flattened_cube.visible = True

        if event.key == pygame.K_t:
            if self.show_texture.visible:
                self.show_texture.visible = False
            else:
                print('--> showing texture map')
                self.show_texture.visible = True

        if event.key == pygame.K_s:
            if self.show_shadow_map.visible:
                self.show_shadow_map.visible = False
            else:
                print('--> showing shadow map')
                self.show_shadow_map.visible = True

        if event.key == pygame.K_1:
            print('--> using Flat shading')
            self.bunny.use_textures = True
            self.bunny.bind_shader('flat')

        if event.key == pygame.K_2:
            print('--> using Phong shading')
            self.bunny.use_textures = True
            self.bunny.bind_shader('phong')

        elif event.key == pygame.K_4:
            print('--> using original texture')
            self.bunny.shader.mode = 1

        elif event.key == pygame.K_6:
            self.bunny.mesh.material.alpha += 0.1
            print('--> bunny alpha={}'.format(self.bunny.mesh.material.alpha))
            if self.bunny.mesh.material.alpha > 1.0:
                self.bunny.mesh.material.alpha = 0.0

        elif event.key == pygame.K_7:
            print('--> no face culling')
            glDisable(GL_CULL_FACE)

        elif event.key == pygame.K_8:
            print('--> glCullFace(GL_FRONT)')
            glEnable(GL_CULL_FACE)
            glCullFace(GL_FRONT)

        elif event.key == pygame.K_9:
            print('--> glCullFace(GL_BACK)')
            glEnable(GL_CULL_FACE)
            glCullFace(GL_BACK)

        elif event.key == pygame.K_BACKQUOTE:
            if glIsEnabled(GL_DEPTH_TEST):
                print('--> disable GL_DEPTH_TEST')
                glDisable(GL_DEPTH_TEST)
            else:
                print('--> enable GL_DEPTH_TEST')
                glEnable(GL_DEPTH_TEST)


if __name__ == '__main__':
    # initialises the scene object
    scene = JurassicScene()

    # starts drawing the scene
    scene.run()
