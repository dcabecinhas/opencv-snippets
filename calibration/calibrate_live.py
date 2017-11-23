#!/usr/bin/env python

import cv2
import numpy as np
import yaml

import json
from datetime import datetime

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,640);
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480);

# Needed for fast display
cv2.namedWindow('grid',cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_OPENGL)

# Number of inner corners per a chessboard row and column
pattern_size = (7,5)
square_size = 45.0 # mm (can be other or just 1.0)
pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
pattern_points *= square_size

obj_points = []
img_points = []

while (True):
    # Capture frame-by-frame
    ret, image = cap.read()

    found, corners = cv2.findChessboardCorners(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), pattern_size, cv2.CALIB_CB_FAST_CHECK)

    if found == True:
        # Refine square detection
        term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
        cv2.cornerSubPix(image, corners, (5, 5), (-1, -1), term)

        img_points.append(corners.reshape(-1, 2))
        obj_points.append(pattern_points)

        # Save image to disc
        filename = datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg'
        cv2.imwrite(filename, image)

        # Draw grid overlay
        cv2.drawChessboardCorners(image, pattern_size, corners, found)

    # display image (with grid overlay, if cound corners)
    cv2.imshow('grid', cv2.flip(image,1))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Calculating camera distortion...")

# calculate camera distortion
rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)

print("\nRMS:", rms)
print("camera matrix:\n", camera_matrix)
print("distortion coefficients: ", dist_coefs.ravel())

# From https://longervision.github.io/2017/03/19/opencv-internal-calibration-chessboard/
#
# Write to yaml configuration file
# 
# It's very important to transform the matrix to list.
data = {'camera_matrix': np.asarray(camera_matrix).tolist(),
        'dist_coeff': np.asarray(dist_coefs).tolist()}
        
with open("calibration.yaml", "w") as f:
    yaml.dump(data, f)
with open("calibration.yaml", "w") as f:
    yaml.dump(data, f)

# To read back the yaml file:
# 
# with open('calibration.yaml') as f:
#     loadeddict = yaml.load(f)
#     camera_matrix_loaded = loadeddict.get('camera_matrix')
#     dist_coefs_loaded = loadeddict.get('dist_coeff')


# When everything done, release the capture
cap.release()

cv2.destroyAllWindows()

# Hack not to "hang" the window in *nix systems (Linux,Mac)
cv2.waitKey(1)

