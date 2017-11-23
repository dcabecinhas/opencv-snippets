import cv2
from datetime import datetime

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,640);
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480);

# Needed for fast display
cv2.namedWindow('grid',cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_OPENGL)

# Number of inner corners per a chessboard row and column
pattern_size = (7,5)

while (True):
    # Capture frame-by-frame
    ret, image = cap.read()

    # display image
    cv2.imshow('grid', cv2.flip(image,1))
    cv2.waitKey(1)

    # save image to file, if pattern found
    found, corners = cv2.findChessboardCorners(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), pattern_size, None)

    if found == True:
        # Save image to disc
        filename = datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg'
        cv2.imwrite(filename, image)

        # Draw grid overlay
        cv2.drawChessboardCorners(image, pattern_size, corners, found)

    # display image (with grid overlay, if cound corners)
    cv2.imshow('grid', cv2.flip(image,1))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()

cv2.destroyAllWindows()

# Hack not to "hang" the window in *nix systems (Linux,Mac)
cv2.waitKey(1)

