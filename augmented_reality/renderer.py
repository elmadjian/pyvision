import cv2
import numpy as np
from threading import Thread
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from objloader import *

class Renderer():
    def __init__(self):
        self.object = None
        self.texture_background = None
        self.image = None
        self.rvecs = None
        self.tvecs = None


    def start(self):
        Thread(target=self.loop, args=()).start()


    def _init_gl(self, width, height):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(33.7, 1.3, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        self.object = OBJ("carro.obj")
        glEnable(GL_TEXTURE_2D)
        self.texture_background = glGenTextures(1)


    def draw_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        if self.image is not None:
            bg_image = cv2.flip(self.image, 0)
            bg_image = Image.fromarray(bg_image)
            ix = bg_image.size[0]
            iy = bg_image.size[1]
            bg_image = bg_image.tobytes("raw", "BGRX", 0, -1)
            glBindTexture(GL_TEXTURE_2D, self.texture_background)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_image)
            glBindTexture(GL_TEXTURE_2D, self.texture_background)
            glPushMatrix()
            glTranslatef(0.0,0.0,-10.0)
            self._draw_background()
            glPopMatrix()
            if self.rvecs is not None:
                print("desenhando objeto!")
                self._draw_object(self.rvecs, self.tvecs)



    def _draw_object(self, rvecs, tvecs):
        rmtx, jac = cv2.Rodrigues(rvecs)
        vmtx = np.array([[rmtx[0][0],rmtx[0][1],rmtx[0][2],tvecs[0]],
                         [rmtx[1][0],rmtx[1][1],rmtx[1][2],tvecs[1]],
                         [rmtx[2][0],rmtx[2][1],rmtx[2][2],tvecs[2]],
                         [0.0       ,0.0       ,0.0       ,1.0    ]])
        inverse_mtx = np.array([[ 1.0, 1.0, 1.0, 1.0],
                                [-1.0,-1.0,-1.0,-1.0],
                                [-1.0,-1.0,-1.0,-1.0],
                                [ 1.0, 1.0, 1.0, 1.0]])
        vmtx = vmtx * inverse_mtx
        vmtx = np.transpose(vmtx)
        glPushMatrix()
        glLoadMatrixd(vmtx)
        glCallList(self.object.gl_list)
        glPopMatrix()


    def _draw_background(self):
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 4.0,  3.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.0,  3.0, 0.0)
        glEnd()



    def loop(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(800, 400)
        self.window_id = glutCreateWindow("OpenGL Test")
        glutDisplayFunc(self.draw_scene)
        glutIdleFunc(self.draw_scene)
        self._init_gl(640, 480)
        glutMainLoop()
