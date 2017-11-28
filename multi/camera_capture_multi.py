#!/usr/bin/env python
# Baseline file without concurrency nor parallelism
import cv2
import numpy as np
import timeit

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,1900);
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080);
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280);
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720);
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,848);
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480);
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,640);
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,360);
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,424);
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240);

font = cv2.FONT_HERSHEY_SIMPLEX

def process_image(image):

    # Remember framerate

    N = 10
    if not hasattr(process_image, "t_prev"):
        process_image.t_prev = timeit.default_timer()  # it doesn't exist yet, so initialize it
    if not hasattr(process_image, "counter"):
        process_image.counter = 0  # it doesn't exist yet, so initialize it
    if not hasattr(process_image, "fps"):
        process_image.fps = 0  # it doesn't exist yet, so initialize it
    process_image.counter += 1

    if(process_image.counter % N == 0):
        t = timeit.default_timer()
        process_image.fps = N/(t-process_image.t_prev)
        process_image.t_prev = t
    
    # Image processing

    image = cv2.flip(image, 1)

    image = cv2.medianBlur(image, 21)
    # image = cv2.GaussianBlur(image, (51,51),0)

    cv2.putText(image, "fps: {0:.1f}".format(process_image.fps), (0, 30), font, 1, 255, 2, cv2.LINE_AA)

    return image


def main():
    cv2.namedWindow('frame',cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_OPENGL)
    
    N = 10
    t_prev = timeit.default_timer()
    counter = 0
    fps = 0

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        frame = process_image(frame)

        counter += 1
        if(counter % N == 0):
            t = timeit.default_timer()
            fps = N/(t-t_prev)
            t_prev = t
            print('fps:',fps)

        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()

    cv2.destroyAllWindows()

    # Hack not to "hang" the window in *nix systems (Linux,Mac)
    cv2.waitKey(1)


if __name__ == "__main__":
    main()
