# import numpy as np
import numpy as np

from material import Material, MaterialLibrary
from mesh import Mesh

# This file contains functions for loading Blender3D object files.

def process_line(line):
	"""
	Function for reading the Blender3D object file, line by line.
	:param line: one line from the file
	:return: a tuple containing the label and the data
	"""
    
	label = None
	# split the line
	fields = line.split()
	if len(fields) == 0:
		return None

    # check the first field
	# if it is a comment, we skip it
	if fields[0] == '#':
		label = 'comment'
		return (label, fields[1:])

    # if it is a vertex, we expect 3 entries
	elif fields[0] == 'v':
		label = 'vertex'
		if len(fields) != 4:
			print('(E) Error, 3 entries expected for vertex')
			return None

    # if it is a vertex texture, we expect 2 entries
	elif fields[0] == 'vt':
		label = 'vertex texture'
		if len(fields) != 3:
			print('(E) Error, 2 entries expected for vertex texture')
			return None

	# added for vector normals
	# should be 3 entries	
	elif fields[0] == 'vn':
		label = 'normal'
		if len(fields) != 4:
			print('(E) Error, 3 entries expected for normal')
			return None

    # if it is a material library, we expect 1 entry
	elif fields[0] == 'mtllib':
		label = 'material library'
		if len(fields) != 2:
			print('(E) Error, material library file name missing')
			return None
		else:
			return (label, fields[1])
    
	# if it is a material, we expect 1 entry
	elif fields[0] == 'usemtl':
		label = 'material'
		if len(fields) != 2:
			print('(E) Error, material file name missing')
			return None
		else:
			return (label, fields[1])
    
	# if it is a face, we expect 3 or 4 entries
	elif fields[0] == 'f':
		label = 'face'
		if len(fields) != 4 and len(fields) != 5:
			print('(E) Error, 3 or 4 entries expected for faces\n{}'.format(line))
			return None


		# multiple formats for faces lines, eg
		# f 586/1 1860/2 1781/3
		# f vi/ti/ni
		# where vi is the vertex index
		# ti is the texture index
		# ni is the normal index (optional)
		return ( label, [ [np.uint32(i) for i in v.split('/')] for v in fields[1:] ] )

	else:
		print('(E) Unknown line: {}'.format(fields))
		return None

	return (label, [float(token) for token in fields[1:]])


def load_material_library(file_name):
	"""
	Function for loading a Blender3D material library file.
	:param file_name: the name of the file
	:return: a MaterialLibrary object
	"""

	# create a new material library
	library = MaterialLibrary()
	material = None

	print('-- Loading material library {}'.format(file_name))

    # open the file
	mtlfile = open(file_name)
	# read the file line by line
	for line in mtlfile:
		fields = line.split()
		# skip empty lines
		if len(fields) != 0:
			if fields[0] == 'newmtl':
				if material is not None:
					library.add_material(material)

				material = Material(fields[1])
				print('Found material definition: {}'.format(material.name))
			elif fields[0] == 'Ka':
				material.Ka = np.array(fields[1:], 'f')
			elif fields[0] == 'Kd':
				material.Kd = np.array(fields[1:], 'f')
			elif fields[0] == 'Ks':
				material.Ks = np.array(fields[1:], 'f')
			elif fields[0] == 'Ns':
				material.Ns = float(fields[1])
			elif fields[0] == 'd':
				material.d = float(fields[1])
			elif fields[0] == 'Tr':
				material.d = 1.0 - float(fields[1])
			elif fields[0] == 'illum':
				material.illumination = int(fields[1])
			elif fields[0] == 'map_Kd':
				material.texture = fields[1]

	library.add_material(material)

	print('- Done, loaded {} materials'.format(len(library.materials)))

	return library


def load_obj_file(file_name):
	"""
	Function for loading a Blender3D object file.
	:param file_name: the name of the file
	:return: a list of Mesh objects
	"""

	print('Loading mesh(es) from Blender file: {}'.format(file_name))

	vlist = []	# list of vertices
	tlist = []	# list of texture vectors
	flist = []	# list of polygonal faces
	mlist = []	# list of material names

    # list of line numbers for error reporting
	lnlist = []
	mesh_id = 0
	mesh_list = []

	# current material object
	material = None

    # open the file
	with open(file_name) as objfile:
		line_nb = 0 # count line number for easier error locating

		# loop over all lines in the file
		for line in objfile:
			# process the line
			data = process_line(line)

			line_nb += 1 # increment line

			# skip empty lines
			if data is None:
				continue
            
			# check the label
			elif data[0] == 'vertex':
				vlist.append(data[1])

			elif data[0] == 'normal':
				vlist.append(data[1])

			elif data[0] == 'vertex texture':
				tlist.append(data[1])

			elif data[0] == 'face':
				if len(data[1]) == 3:
					flist.append(data[1])
					mesh_list.append(mesh_id)
					mlist.append(material)
					lnlist.append(line_nb)
				else:
					# converts quads into pairs of  triangles
					face1 = [data[1][0], data[1][1], data[1][2]]
					flist.append(face1)
					mesh_list.append(mesh_id)
					mlist.append(material)
					lnlist.append(line_nb)

					face2 = [data[1][0], data[1][2], data[1][3]]
					flist.append(face2)
					mesh_list.append(mesh_id)
					mlist.append(material)
					lnlist.append(line_nb)

			elif data[0] == 'material library':
				library = load_material_library('models/{}'.format(data[1]))

			# material indicate a new mesh in the file, so we store the previous one if not empty and start
			# a new one.
			elif data[0] == 'material':
				material = library.names[data[1]]
				mesh_id += 1
				print('[l.{}] Loading mesh with material: {}'.format(line_nb, data[1]))

	print('File read. Found {} vertices and {} faces.'.format(len(vlist), len(flist)))

	return create_meshes_from_blender(vlist, flist, mlist, tlist, library, mesh_list, lnlist)


def create_meshes_from_blender(vlist, flist, mlist, tlist, library, mesh_list, lnlist):
	"""
	Function for creating a list of Mesh objects from the data read from a Blender3D object file.
	:param vlist: list of vertices
	:param flist: list of faces
	:param mlist: list of materials
	:param tlist: list of texture vectors
	:param library: material library
	:param mesh_list: list of mesh ids
	:param lnlist: list of line numbers
	:return: a list of Mesh objects
	"""
	fstart = 0
	mesh_id = 1
	meshes = []

	# we start by putting all vertices in one array
	varray = np.array(vlist, dtype='f')

	# and all texture vectors
	tarray = np.array(tlist, dtype='f')

	material = mlist[fstart]

    # loop over all faces 
	for f in range(len(flist)):
		if mesh_id != mesh_list[f]:  # new mesh is denoted by change in material
			print('Creating new mesh %i, faces %i-%i, line %i, with material %i: %s' % (mesh_id, fstart, f, lnlist[fstart], mlist[fstart], library.materials[mlist[fstart]].name))
			try:
				mesh = create_mesh(varray, tarray, flist, fstart, f, library, material)
				meshes.append(mesh)
			except Exception as e:
				print('(W) could not load mesh!')
				print(e)
				raise

			mesh_id = mesh_list[f]

			# start the next mesh
			fstart = f
			material = mlist[fstart]

	# add the last mesh
	try:
		meshes.append(create_mesh(varray, tarray, flist, fstart, len(flist), library, material))
	except:
		print('(W) could not load mesh!')
		raise

	print('--- Created {} mesh(es) from Blender file.'.format(len(meshes)))
	return meshes


def create_mesh(varray, tarray, flist, fstart, f, library, material):
	"""
	Function for creating a Mesh object from the data read from a Blender3D object file.
	:param varray: array of vertices
	:param tarray: array of texture vectors
	:param flist: list of faces
	:param fstart: start index for faces
	:param f: end index for faces
	:param library: material library
	:param material: material name
	:return: a Mesh object
	"""
	# select faces for this mesh
	farray = np.array(flist[fstart:f], dtype=np.uint32)

	# and vertices
	vmax = np.max(farray[:, :, 0].flatten())
	vmin = np.min(farray[:, :, 0].flatten()) - 1

	# fix blender texture intexing
	textures = fix_blender_textures(tarray, farray, varray)
	if textures is not None:
		textures = textures[vmin:vmax, :]

    # create the mesh
	return Mesh(
			vertices=varray[vmin:vmax, :],
			faces=farray[:, :, 0] - vmin - 1,
			material=library.materials[material],
			textureCoords=textures
		)


def fix_blender_textures(textures, faces, vertices):
	"""
	Corrects the indexing of textures in Blender file for OpenGL.
	Blender allows for multiple indexing of vertices and textures, which is not supported by OpenGL.
	This function ensures that indexing is consistent.
	:param textures: Original Blender texture UV values
	:param faces: Blender faces multiple-index
	:return: a new texture array indexed according to vertices.
	"""
	# (OpenGL, unlike Blender, does not allow for multiple indexing!)

	if faces.shape[2] == 1:
		print('(W) No texture indices provided, setting texture coordinate array as None!')
		return None

	new_textures = np.zeros((vertices.shape[0], 2), dtype='f')

	for f in range(faces.shape[0]):
		for j in range(faces.shape[1]):
			new_textures[faces[f, j, 0] - 1, :] = textures[faces[f, j, 1] - 1, :]

	return new_textures
