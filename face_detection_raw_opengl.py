#!/usr/bin/env python
# From https://stackoverflow.com/questions/32210107/opencv-python-opengl-texture
import cv2
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import sys

import timeit

#window dimensions
width = 1280
height = 720
nRange = 1.0

global capture
capture = None

face_cascade = cv2.CascadeClassifier('/Users/dcabecinhas/anaconda3/envs/image/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/Users/dcabecinhas/anaconda3/envs/image/share/OpenCV/haarcascades/haarcascade_eye.xml')

def idle():
  #capture next frame
  global capture
  _,frame = capture.read()

  # Timing
  t = timeit.default_timer()
  fps_camera = 1/(t-idle.t_prev)
  idle.t_prev = t
  
  frame=cv2.flip(frame,1)

  # Our operations on the frame come here
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  # HAAR
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)

  # LBP
  # faces = face_cascade.detectMultiScale(gray)
  for (x,y,w,h) in faces:
      cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),1)
      roi_gray = gray[y:y+h, x:x+w]
      roi_color = frame[y:y+h, x:x+w]
      # eyes = eye_cascade.detectMultiScale(roi_gray)
      # for (ex,ey,ew,eh) in eyes:
      #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

  t_stop = timeit.default_timer()
  fps_detection = 1/(t_stop-t)

  font = cv2.FONT_HERSHEY_SIMPLEX
  cv2.putText(frame, "fps camera:   {0:.1f}".format(fps_camera), (0, 13), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
  cv2.putText(frame, "fps detection: {0:.1f}".format(fps_detection), (0, 30), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

  ### OpenGL

  # Create Texture
  glTexImage2D(GL_TEXTURE_2D, 
    0, 
    GL_RGB, 
    1280,720,
    0,
    GL_BGR, 
    GL_UNSIGNED_BYTE, 
    frame)
  glutPostRedisplay()

idle.counter = 0
idle.t_prev = timeit.default_timer()


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
  # capture.set(cv2.CAP_PROP_FRAME_WIDTH,width)
  # capture.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
  glutInit(sys.argv)
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
  glutInitWindowSize(width, height)
  glutInitWindowPosition(100, 100)
  glutCreateWindow("OpenGL + OpenCV")

  init()
  glutMainLoop()

main()