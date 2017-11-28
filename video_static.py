#!/usr/bin/env python
import cv2
import numpy as np

import timeit

font = cv2.FONT_HERSHEY_DUPLEX

# Image parameters
w = 1280
h = 720
# c = 1     # monochrome
c = 3       # color

# Timing
N = 10
k = 0
t = timeit.default_timer()
t_prev = 0
fps_imshow = 0
fps = 0
cv2.namedWindow('window',cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO)
while(True):
    k += 1

    static = np.random.randint(0,255,[h,w,c],np.uint8)

    # timing
    if(k % N == 0):
        t_prev = t
        t = timeit.default_timer()
        fps = N/(t-t_prev)

    cv2.putText(static, "fps display: {0:.1f}".format(fps), (0, 30), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(static, "fps imshow: {0:.1f}".format(fps_imshow), (0, 60), font, 1, (0, 255, 0), 1, cv2.LINE_AA)

    t_start = timeit.default_timer()
    cv2.imshow('window',static)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    t_stop = timeit.default_timer()
    fps_imshow = 1/(t_stop-t_start)

cv2.destroyAllWindows()

# Hack not to "hang" the window in *nix systems (Linux,Mac)
cv2.waitKey(1)