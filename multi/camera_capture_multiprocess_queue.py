#!/usr/bin/env python
### Parallelism using Process() and Queue()
from multiprocessing import Process, Queue
import queue

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

framerate = 30
frame_time = 1/framerate

def process_image(q_in, q_out):

    N = 10
    t_prev = timeit.default_timer()
    counter = 0
    fps = 0
    
    while True:
        counter += 1

        if(counter % N == 0):
            t = timeit.default_timer()
            fps = N/(t-t_prev)
            t_prev = t
            print('fps:',fps)

        image = q_in.get()

        # Image processing
        
        image = cv2.flip(image, 1)

        image = cv2.medianBlur(image, 21)
        # image = cv2.GaussianBlur(image, (51,51),0)

        cv2.putText(image, "fps: {0:.1f}".format(fps), (0, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        q_out.put(image)

    return


def main():

    cv2.namedWindow('frame',cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_OPENGL)
    
    # Setup image processing thread
    qImage = Queue(maxsize=2)
    qImagePost = Queue(maxsize=2)
    p = Process(target=process_image, args=(qImage,qImagePost,))
    p.start()

    N = 10
    t_prev = timeit.default_timer()
    counter = 0
    fps = 0

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        try:
            qImage.put(frame, timeout=frame_time)
        except queue.Full:
            pass

        try:
            frame = qImagePost.get(block=False)

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

        except queue.Empty:
            pass

    # Clear the queue, wait for the thread to finish processing 
    # the current frame and return it to 
    qImagePost.get(block=2*frame_time)

    p.terminate()

    # When everything done, release the capture
    cap.release()

    cv2.destroyAllWindows()

    # Hack not to "hang" the window in *nix systems (Linux,Mac)
    cv2.waitKey(1)


if __name__ == "__main__":
    main()
