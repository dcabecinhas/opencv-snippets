#!/usr/bin/env python
from multiprocessing import Process
import cv2
    
def process_image():

    print(cv2.__loader__)

    return


def main():

    p = Process(target=process_image)
    p.start()

    print(cv2.__loader__)

    p.join()


if __name__ == "__main__":
    main()
