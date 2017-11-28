#!/usr/bin/env python
from multiprocessing import Process

def process_image():

    import cv2
    print(cv2.__loader__)

    return


def main():

    p = Process(target=process_image)
    p.start()

    import cv2
    print(cv2.__loader__)

    p.join()


if __name__ == "__main__":
    main()
