# imports all openGL functions
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders

# we will use numpy to store data in arrays
import numpy as np

class Uniform:
    '''
    We create a simple class to handle uniforms, this is not necessary,
    but allow to put all relevant code in one place
    '''
    def __init__(self, name):
        '''
        Initialise the uniform parameter
        :param name: the name of the uniform, as stated in the GLSL code
        '''
        self.name = name
        self.value = None
        self.location = -1

    def link(self, program):
        '''
        This function needs to be called after compiling the GLSL program to fetch the location of the uniform
        in the program from its name
        :param program: the GLSL program where the uniform is used
        '''
        self.location = glGetUniformLocation(program=program, name=self.name)
        if self.location == -1:
            print('(E) Warning, no uniform {}'.format(self.name))

    def bind_matrix(self, number=1, transpose=True):
        '''
        Call this before rendering to bind the Python matrix to the GLSL uniform mat4.
        You will need different methods for different types of uniform, but for now this will
        do for the PVM matrix
        :param number: the number of matrices sent, leave that to 1 for now
        :param transpose: Whether the matrix should be transposed
        '''
        glUniformMatrix4fv(self.location, number, transpose, self.value)

    def set(self, value):
        '''
        function to set the uniform value (could also access it directly, of course)
        '''
        self.value = value

class Shaders:
    '''
    This is the base class for loading and compiling the GLSL shaders.
    '''
    def __init__(self, vertex_shader = None, fragment_shader = None):
        '''
        Initialises the shaders
        :param vertex_shader: the name of the file containing the vertex shader GLSL code
        :param fragment_shader: the name of the file containing the fragment shader GLSL code
        '''

        # We create one uniform for the Projection-View-Model matrix,
        # This will allow us to send this matrix as a parameter of the shader program
        # use this as an example for adding
        # more uniforms when needed.
        self.PVM = Uniform('PVM')

        # load the vertex shader GLSL code
        if vertex_shader is None:
            self.vertex_shader_source = '''
                #version 130
                in vec3 position;
                out vec4 vertex_color;  // the output of the shader will be the colour of the vertex
                uniform mat4 PVM; // the Perspective-View-Model matrix is received as a Uniform
                
                void main() {
                    gl_Position = PVM * vec4(position, 1.0f);  // first we transform the position using PVM matrix
                    //gl_Position = gl_ModelViewProjectionMatrix * vec4(position, 1.0f);
                    vertex_color = gl_Color;        // at this stage, the colour simply passed on. 
                }
            '''
        else:
            self.vertex_shader_source = open(vertex_shader)

        # load the fragment shader GLSL code
        if fragment_shader is None:
            self.fragment_shader_source = '''
                #version 130
                in vec4 vertex_color;      // the vertex colour is received from the vertex shader
                
                void main() {                   
                      gl_FragColor = vertex_color;      // for now, we just apply the colour uniformly
                }
            '''
        else:
            self.fragment_shader_source = open(fragment_shader)

    def compile(self):
        '''
        Call this function to compile the GLSL codes for both shaders.
        :return:
        '''
        print('Compiling GLSL shaders...')
        self.program = shaders.compileProgram(
            shaders.compileShader(self.vertex_shader_source, shaders.GL_VERTEX_SHADER),
            shaders.compileShader(self.fragment_shader_source, shaders.GL_FRAGMENT_SHADER)
        )

        # tell OpenGL to use this shader program for rendering
        glUseProgram(self.program)

        # and link the PVM matrix in the python code to the matrix in the GLSL program
        self.PVM.link(self.program)


    def bind(self, P, V, M):
        '''
        Call this function to enable this GLSL Program (you can have multiple GLSL programs used during rendering!)
        :return:
        '''

        # tell OpenGL to use this shader program for rendering
        glUseProgram(self.program)

        # set the PVM matrix uniform
        self.PVM.set( np.matmul(P,np.matmul(V,M)) )

        # and send it to the program
        self.PVM.bind_matrix()

    def unbind(self):
        glUseProgram(0)