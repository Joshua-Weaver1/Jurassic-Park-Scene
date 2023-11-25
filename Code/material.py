# Description: Material class and MaterialLibrary class

class Material:
    """
    This class represents a material in the scene.
    """
    def __init__(self, name=None, Ka=[1.,1.,1.], Kd=[1.,1.,1.], Ks=[1.,1.,1.], Ns=10.0, texture=None):
        """
        Initialises the material.
        :param name: The name of the material.
        :param Ka: The ambient reflection coefficient.
        :param Kd: The diffuse reflection coefficient.
        :param Ks: The specular reflection coefficient.
        :param Ns: The specular exponent.
        :param texture: The texture to use.
        """
        self.name = name
        self.Ka = Ka
        self.Kd = Kd
        self.Ks = Ks
        self.Ns = Ns
        self.texture = texture
        self.alpha = 1.0

class MaterialLibrary:
    """
    This class represents a material library.
    """
    def __init__(self):
        """
        Initialises the material library.
        """
        self.materials = []
        self.names = {}

    def add_material(self, material):
        """
        Adds a material to the library.
        :param material: The material to add.
        :return: None
        """
        self.names[material.name] = len(self.materials)
        self.materials.append(material)

