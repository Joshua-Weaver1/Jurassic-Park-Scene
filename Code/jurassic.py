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

import numpy as np

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
        city = load_obj_file('models/city.obj')
        self.city = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([7,-23,17]), scaleMatrix([0.02,0.08,0.02])), mesh=city[0], shader=PhongShader())

        triceratops = load_obj_file('models/TRIKERATOPS_CAGE_MODEL.obj')
        self.triceratops = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([0,-20,1.5]), scaleMatrix([0.4,0.4,0.4])), mesh=triceratops[0], shader=PhongShader())

        box = load_obj_file('models/postbox.obj')
        self.box = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-4,-20, 4]), scaleMatrix([10, 10, 10])), mesh=box[0], shader=PhongShader())
        
        car = load_obj_file('models/car.obj')
        self.car = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-12,-20, 5]), scaleMatrix([0.4, 0.4, 0.4])), mesh=car[0], shader=PhongShader())

        tank = load_obj_file('models/tank.obj')
        self.tank = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-12,-20, 2]), scaleMatrix([0.015, 0.015, 0.015])), rotationMatrixY(1.5708)), mesh=tank[0], shader=PhongShader())

        # Set the initial and target positions for the raptor
        self.raptor_start_position = np.array([-12,-20, -17])
        self.raptor_target_position = np.array([12, -20, -17])  # Replace with your desired target position
        self.raptor_current_position = self.raptor_start_position
        self.lerp_factor = 0.0  # Initial interpolation factor

        raptor = load_obj_file('models/RAPTOR_CAGE_MODEL.obj')
        self.raptor = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-12,-20, -17]), scaleMatrix([1, 1, 1])), mesh=raptor[0], shader=PhongShader())
        self.raptor2 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([9,-20, 15]), scaleMatrix([1, 1, 1])), rotationMatrixY(4.71239)), mesh=raptor[0], shader=PhongShader())

        # road pieces
        r1 = load_obj_file('models/3Roads.obj')
        self.r1 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-1.7,-20, -7]), scaleMatrix([0.8, 0.8, 0.8])), mesh=r1[0], shader=PhongShader())
        self.r2 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-1.7,-20, -4]), scaleMatrix([0.8, 0.8, 0.8])), mesh=r1[0], shader=PhongShader())
        self.r3 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-1.7,-20, -1]), scaleMatrix([0.8, 0.8, 0.8])), mesh=r1[0], shader=PhongShader())
        self.r4 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-1.7,-20, 2]), scaleMatrix([0.8, 0.8, 0.8])), mesh=r1[0], shader=PhongShader())
        self.r5 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-1.7,-20, 5]), scaleMatrix([0.8, 0.8, 0.8])), mesh=r1[0], shader=PhongShader())
        self.r6 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-1.7,-20, 8]), scaleMatrix([0.8, 0.8, 0.8])), mesh=r1[0], shader=PhongShader())
        self.r7 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([-1.7,-20, 11]), scaleMatrix([0.8, 0.8, 0.8])), mesh=r1[0], shader=PhongShader())

        self.r8 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-4.7,-20, 2]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r9 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-7.7,-20, 2]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r10 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-10.7,-20, 2]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r11 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-13.7,-20, 2]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r12 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-15.7,-20, 2]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r13 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([1.5,-20, 2]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r14 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([4.5,-20, 2]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r15 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([7.5,-20, 2]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r16 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([10.5,-20, 2]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())

        self.r17 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([10.5,-20, -7]), scaleMatrix([0.8, 0.8, 0.8])), mesh=r1[0], shader=PhongShader())
        self.r18 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([10.5,-20, -4]), scaleMatrix([0.8, 0.8, 0.8])), mesh=r1[0], shader=PhongShader())
        self.r19 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([10.5,-20, -1]), scaleMatrix([0.8, 0.8, 0.8])), mesh=r1[0], shader=PhongShader())

        self.r20 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([10.5,-20, -9]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r21 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([13.5,-20, -9]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r22 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([16.5,-20, -9]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        
        self.r23 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([1.5,-20, 12]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r24 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([4.5,-20, 12]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r25 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([7.5,-20, 12]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r26 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-1.5,-20, 12]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        
        self.r27 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([9,-20, 12]), scaleMatrix([0.8, 0.8, 0.8])), mesh=r1[0], shader=PhongShader())
        self.r28 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([9,-20, 15]), scaleMatrix([0.8, 0.8, 0.8])), mesh=r1[0], shader=PhongShader())
        self.r29 = DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([9,-20, 17]), scaleMatrix([0.8, 0.8, 0.8])), mesh=r1[0], shader=PhongShader())

        self.r30 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-1.7,-20, -8]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r31 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-4.7,-20, -8]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r32 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-7.7,-20, -8]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r33 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-10.7,-20, -8]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r34 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-13.7,-20, -8]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())

        self.r35 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-4.7,-20, -17]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r36 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-7.7,-20, -17]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r37 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-10.7,-20, -17]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r38 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-13.7,-20, -17]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r39 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-15.7,-20, -17]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r40 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([1.5,-20, -17]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r41 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([4.5,-20, -17]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r42 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([7.5,-20, -17]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r43 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([10.5,-20, -17]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())
        self.r44 = DrawModelFromMesh(scene=self, M=np.matmul(np.matmul(translationMatrix([-1.7,-20, -17]), scaleMatrix([0.8, 0.8, 0.8])), rotationMatrixY(1.5708)), mesh=r1[0], shader=PhongShader())

        self.flattened_cube = FlattenCubeMap(scene=self, cube=self.environment)

        # show the texture to the ticeratops
        self.show_texture = ShowTexture(self, Texture('triceratops_diffuse.bmp'))
    
    def update_raptor_position(self):
        # Update the raptor's position
        self.lerp_factor += 0.002
        if self.lerp_factor >= 1.0:
            # Reset lerp_factor to restart the movement
            self.lerp_factor = 0.0
            # Swap start and target positions for continuous loop
            self.raptor_start_position, self.raptor_target_position = self.raptor_target_position, self.raptor_start_position
        self.lerp_factor = min(1.0, max(0.0, self.lerp_factor))
        self.raptor_current_position = (
            self.raptor_start_position
            + self.lerp_factor * (self.raptor_target_position - self.raptor_start_position)
        )
        self.raptor.M = np.matmul(translationMatrix(self.raptor_current_position), scaleMatrix([1, 1, 1]))

    def draw_shadow_map(self):
        """
        Draw the shadow map.
        :return: None
        """

        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for model in self.models:
            model.draw()

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
        # Update raptor position
        self.update_raptor_position()

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

            self.triceratops.draw()
            self.city.draw()
            self.box.draw()
            self.raptor.draw()
            self.raptor2.draw()
            self.car.draw()
            self.tank.draw()

            self.r1.draw()
            self.r2.draw()
            self.r3.draw()
            self.r4.draw()
            self.r5.draw()
            self.r6.draw()
            self.r7.draw()
            self.r8.draw()
            self.r9.draw()
            self.r10.draw()
            self.r11.draw()
            self.r12.draw()
            self.r13.draw()
            self.r14.draw()
            self.r15.draw()
            self.r16.draw()
            self.r17.draw()
            self.r18.draw()
            self.r19.draw()
            self.r20.draw()
            self.r21.draw()
            self.r22.draw()
            self.r23.draw()
            self.r24.draw()
            self.r25.draw()
            self.r26.draw()
            self.r27.draw()
            self.r28.draw()
            self.r29.draw()
            self.r30.draw()
            self.r31.draw()
            self.r32.draw()
            self.r33.draw()
            self.r34.draw()
            self.r35.draw()
            self.r36.draw()
            self.r37.draw()
            self.r38.draw()
            self.r39.draw()
            self.r40.draw()
            self.r41.draw()
            self.r42.draw()
            self.r43.draw()
            self.r44.draw()


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
            self.triceratops.use_textures = True
            self.triceratops.bind_shader('flat')

        if event.key == pygame.K_2:
            print('--> using Phong shading')
            self.triceratops.use_textures = True
            self.triceratops.bind_shader('phong')

        elif event.key == pygame.K_4:
            print('--> using original texture')
            self.triceratops.shader.mode = 1

        elif event.key == pygame.K_6:
            self.triceratops.mesh.material.alpha += 0.1
            print('--> triceratops alpha={}'.format(self.triceratops.mesh.material.alpha))
            if self.triceratops.mesh.material.alpha > 1.0:
                self.triceratops.mesh.material.alpha = 0.0

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
