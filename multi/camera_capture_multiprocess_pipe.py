#!/usr/bin/env python
### Parallelism using Process() and Pipe()
from multiprocessing import Process, Pipe

import cv2
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

framerate = 1/30

def process_image(conn):

    N = 10
    t_prev = timeit.default_timer()
    counter = 0
    fps = 0
    
    # Remember framerate
    while True:
            
        image = conn.recv()

        counter += 1
        if(counter % N == 0):
            t = timeit.default_timer()
            fps = N/(t-t_prev)
            t_prev = t


        # Image processing
        
        image = cv2.flip(image, 1)

        image = cv2.medianBlur(image, 21)
        # image = cv2.GaussianBlur(image, (51,51),0)

        cv2.putText(image, "fps: {0:.1f}".format(fps), (0, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        conn.send(image)

    return


def main():

    cv2.namedWindow('Processed image',cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_OPENGL)
    
    # Setup image processing thread
    parent_conn, child_conn = Pipe()
    p = Process(target=process_image, args=(child_conn,))
    p.start()

    N = 10
    t_prev = timeit.default_timer()
    counter = 0
    fps = 0

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        parent_conn.send(frame)

        image = parent_conn.recv()

        counter += 1
        if(counter % N == 0):
            t = timeit.default_timer()
            fps = N/(t-t_prev)
            t_prev = t
            print('fps:',fps)

        # Display the resulting frame
        cv2.imshow('Processed image',image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    p.terminate()

    # When everything done, release the capture
    cap.release()

    cv2.destroyAllWindows()

    # Hack not to "hang" the window in *nix systems (Linux,Mac)
    cv2.waitKey(1)


if __name__ == "__main__":
    main()
