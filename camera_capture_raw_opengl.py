# From https://stackoverflow.com/questions/32210107/opencv-python-opengl-texture

import cv2
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import sys


#window dimensions
width = 1280
height = 720
nRange = 1.0

global capture
capture = None

def idle():
  #capture next frame
  global capture
  _,image = capture.read()

  # Create Texture
  glTexImage2D(GL_TEXTURE_2D, 
    0, 
    GL_RGB, 
    1280,720,
    0,
    GL_BGR, 
    GL_UNSIGNED_BYTE, 
    image)
  glutPostRedisplay()


def init():
  #glclearcolor (r, g, b, alpha)
  glClearColor(0.0, 0.0, 0.0, 1.0)

  glutDisplayFunc(display)
  glutReshapeFunc(reshape)
  glutKeyboardFunc(keyboard)
  glutIdleFunc(idle)


def display():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  glEnable(GL_TEXTURE_2D)
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

  # Set Projection Matrix
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluOrtho2D(0, width, height, 0)

  # Switch to Model View Matrix
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()

  # Draw textured Quads
  glBegin(GL_QUADS)
  glTexCoord2f(0.0, 0.0)
  glVertex2f(0.0, 0.0)
  glTexCoord2f(1.0, 0.0)
  glVertex2f(width, 0.0)
  glTexCoord2f(1.0, 1.0)
  glVertex2f(width, height)
  glTexCoord2f(0.0, 1.0)
  glVertex2f(0.0, height)
  glEnd()

  glFlush()
  glutSwapBuffers()


def reshape(w, h):
  # if h == 0:
  #   h = 1

  glViewport(0, 0, w, h)
  # glMatrixMode(GL_PROJECTION)

  # glLoadIdentity()
  # # allows for reshaping the window without distoring shape

  # if w <= h:
  #   glOrtho(-nRange, nRange, -nRange*h/w, nRange*h/w, -nRange, nRange)
  # else:
  #   glOrtho(-nRange*w/h, nRange*w/h, -nRange, nRange, -nRange, nRange)

  # glMatrixMode(GL_MODELVIEW)
  # glLoadIdentity()


def keyboard(key, x, y):
  if key == b'\x1b' or key == b'q':
    sys.exit()


def main():
  global capture
  #start openCV capturefromCAM
  capture = cv2.VideoCapture(0)
  print(capture)
  capture.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
  capture.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
  glutInit(sys.argv)
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
  glutInitWindowSize(width, height)
  glutInitWindowPosition(100, 100)
  glutCreateWindow("OpenGL + OpenCV")

  init()
  glutMainLoop()

main()