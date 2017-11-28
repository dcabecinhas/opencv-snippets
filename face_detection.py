#!/usr/bin/env python
# From https://docs.opencv.org/3.3.0/d7/d8b/tutorial_py_face_detection.html
import cv2
import timeit

face_cascade = cv2.CascadeClassifier('/Users/dcabecinhas/anaconda3/envs/image/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/Users/dcabecinhas/anaconda3/envs/image/share/OpenCV/haarcascades/haarcascade_eye.xml')

# face_cascade = cv2.CascadeClassifier('/Users/dcabecinhas/anaconda3/envs/opencv/share/OpenCV/lbpcascades/lbpcascade_frontalface_improved.xml')
cap = cv2.VideoCapture(0)

N = 5
list_fps_det = [30]*N
list_fps_cam = [30]*N
cam_stop = timeit.default_timer()

k = 0
cam_stop = timeit.default_timer()
while(True):
    k += 1
    
    # Capture frame-by-frame
    ret, frame = cap.read()

    cam_start = cam_stop
    cam_stop = timeit.default_timer()
    start = cam_stop

    frame=cv2.flip(frame,1)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # HAAR
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # # LBP
    # faces = face_cascade.detectMultiScale(gray)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    stop = timeit.default_timer()

    det_fps = 1/(stop-start)
    cam_fps = 1/(cam_stop-cam_start)

    list_fps_det[k % N] = det_fps
    list_fps_cam[k % N] = cam_fps

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "fps detection: {0:.1f}".format(sum(list_fps_det)/N), (0, 13), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, "fps camera:   {0:.1f}".format(sum(list_fps_cam)/N), (0, 30), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()

cv2.destroyAllWindows()

# Hack not to "hang" the window in *nix systems (Linux,Mac)
cv2.waitKey(1)

