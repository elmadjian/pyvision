import pygame
from OpenGL.GL import *

class OBJ:
    def __init__(self, filename, swapyz=False):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.mtl = []
        self.gl_list = None
        self._parse_file(filename, swapyz)
        self._add_to_gl_list()


    def _parse_file(self, filename, swapyz):
        material = None
        for line in open(filename, "r"):
            if line.startswith("#"):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == 'v':
                self._get_vertices(values, swapyz)
            elif values[0] == 'vn':
                self._get_normals(values, swapyz)
            elif values[0] == 'vt':
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = self.MTL(values[1])
            elif values[0] == 'f':
                self._get_faces(values, material)


    def _get_vertices(self, values, swapyz):
        v = map(float, values[1:4])
        v = list(v)
        if swapyz:
            v = v[0], v[2], v[1]
        self.vertices.append(v)


    def _get_normals(self, values, swapyz):
        v = map(float, values[1:4])
        v = list(v)
        if swapyz:
            v = v[0], v[2], v[1]
        self.normals.append(v)


    def _get_faces(self, values, material):
        face = []
        texcoords = []
        norms = []
        for v in values[1:]:
            w = v.split('/')
            face.append(int(w[0]))
            if len(w) >= 2 and len(w[1]) > 0:
                texcoords.append(int(w[1]))
            else:
                texcoords.append(0)
            if len(w) >= 3 and len(w[2]) > 0:
                norms.append(int(w[2]))
            else:
                norms.append(0)
        self.faces.append((face, norms, texcoords, material))


    def _add_to_gl_list(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face
            mtl = self.mtl[material]
            # use diffuse texmap
            if 'texture_Kd' in mtl:
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
                # just use diffuse colour
            else:
                glColor(*mtl['Kd'])
            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glEndList()


    def MTL(self, filename):
        contents = {}
        mtl = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'newmtl':
                mtl = contents[values[1]] = {}
            elif mtl is None:
                raise ValueError("mtl file doesn't start with newmtl stmt")
            elif values[0] == 'map_Kd':
                # load the texture referred to by this declaration
                mtl[values[0]] = values[1]
                surf = pygame.image.load(mtl['map_Kd'])
                image = pygame.image.tostring(surf, 'RGBA', 1)
                ix, iy = surf.get_rect().size
                texid = mtl['texture_Kd'] = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, texid)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                    GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                    GL_LINEAR)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                    GL_UNSIGNED_BYTE, image)
            else:
                mtl[values[0]] = list(map(float, values[1:]))
        return contents
