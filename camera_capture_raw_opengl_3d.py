# From: https://github.com/MyDuan/openGL-openCV-python-sample/blob/master/ARTest.py#L1
# Update for 2D with http://www.alecjacobson.com/weblog/?p=1875
# Improve with https://stackoverflow.com/questions/32210107/opencv-python-opengl-texture

import numpy as np
import cv2
from PIL import Image
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from threading import Thread

texture_id = 0
threadQuit = 0
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0
DIRECTION = 1
cap = cv2.VideoCapture(0)
newframe = cap.read()[1]

def Init(): 

    VideoThread = Thread(target=update, args=())
    VideoThread.start()
    #VideoThread.join()

def InitGL(Width, Height):
    global texture_id
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_TEXTURE_2D)
    texture_id = glGenTextures(1)

def update():
    global newframe
    while(True):
        newframe = cap.read()[1]
        if threadQuit == 1:
            break
    cap.release()
    cv2.destroyAllWindows()

def DrawGLScene():
    global cap
    global newframe
    global X_AXIS,Y_AXIS,Z_AXIS
    global DIRECTION
    global texture_id
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    frame = newframe
    # convert image to OpenGL texture format
    tx_image = cv2.flip(frame, 0)
    tx_image = Image.fromarray(tx_image)
    ix = tx_image.size[0]
    iy = tx_image.size[1]
    tx_image = tx_image.tobytes('raw', 'BGRX', 0, -1)
    # create texture
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, tx_image)

    glBindTexture(GL_TEXTURE_2D, texture_id)
    glPushMatrix()
    glTranslatef(0.0,0.0,-21.8)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0); glVertex3f(-16.0, -9.0, 0.0)
    glTexCoord2f(1.0, 1.0); glVertex3f( 16.0, -9.0, 0.0)
    glTexCoord2f(1.0, 0.0); glVertex3f( 16.0,  9.0, 0.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(-16.0,  9.0, 0.0)
    glEnd()
    glPopMatrix()
    
    glutSwapBuffers()

def keyPressed(key, x, y):
    global threadQuit
    print(key,x,y)
    if key == b'\x1b' or key == b'q':
        threadQuit = 1
        sys.exit()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(1280,720)
    glutInitWindowPosition(0,20)
    window = glutCreateWindow('Camera')
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(1280, 720)
    glutMainLoop()


Init()
main()
