# Description: Skybox class

from BaseModel import BaseModel,DrawModelFromMesh
from mesh import *
from matutils import *
from texture import *
from shaders import *
from cubeMap import CubeMap


class SkyBoxShader(BaseShaderProgram):
    """
    Shader for the skybox.
    """
    def __init__(self, name='skybox'):
        """
        Initialises the shader.
        :param name: The name of the shader.
        """
        BaseShaderProgram.__init__(self, name=name)
        self.add_uniform('sampler_cube')

    def bind(self, model, M):
        """
        Binds the shader.
        :param model: The model to bind.
        :param M: The model matrix.
        :return: None
        """
        BaseShaderProgram.bind(self, model, M)
        P = model.scene.P  # get projection matrix from the scene
        V = model.scene.camera.V  # get view matrix from the camera
        Vr = np.identity(4)
        Vr[:3, :3] = V[:3, :3]

        self.uniforms['PVM'].bind(np.matmul(P, np.matmul(V, M)))



class SkyBox(DrawModelFromMesh):
    """
    Class for drawing a skybox.
    """
    def __init__(self, scene):
        """
        Initialises the skybox.
        :param scene: The scene object.
        """
        # scale the skybox to 20 to be large enough to cover the scene
        DrawModelFromMesh.__init__(self, scene=scene, M=poseMatrix(scale=20.0),
                                   mesh=CubeMesh(texture=CubeMap(name='skybox/london'), inside=True),
                                   shader=SkyBoxShader(), name='skybox')

    def draw(self):
        glDepthMask(GL_FALSE)
        DrawModelFromMesh.draw(self)
        glDepthMask(GL_TRUE)

