# From http://zulko.github.io/blog/2013/10/04/read-and-write-audio-files-in-python-using-ffmpeg/

import cv2
import timeit

FFMPEG_BIN = "ffmpeg" # on Linux

# LINUX
# v4l2-ctl --list-formats
# v4l2-ctl --list-formats-ext
# ffmpeg -f video4linux2 -list_formats all -i /dev/video0
# ffmpeg -f video4linux2 -input_format mjpeg -i /dev/video0 -c:v copy output.mkv
# 
# MAC
# ffmpeg -f avfoundation -list_devices true -i ""
# ffmpeg -f avfoundation -pix_fmt yuyv422 -framerate 30 -s 1280x720 -i "0" -f rawvideo - > /dev/null
# ffmpeg -f avfoundation -pix_fmt nv12 -framerate 30 -s 1280x720 -i "0" -f rawvideo - > /dev/null

import subprocess as sp
import numpy

w = 1280
h = 720
c = 3
command = [ FFMPEG_BIN,
            '-hide_banner',
            '-loglevel', 'warning',
            '-f', 'avfoundation',
            '-pix_fmt', 'yuyv422',
            '-framerate', '30',
            '-s', '{}x{}'.format(w,h),
            '-i', '0',
            '-f', 'image2pipe',
            '-pix_fmt', 'bgr24',
            '-vcodec', 'rawvideo', '-']
pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)

font = cv2.FONT_HERSHEY_SIMPLEX


cv2.namedWindow('frame',cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_OPENGL)


N = 10
k = 0
t = timeit.default_timer()
t_prev = 0
while(True):
    k += 1
    
    # read w*h*c bytes (= 1 frame)
    raw_image = pipe.stdout.read(w*h*c)
    # transform the byte read into a numpy array
    frame =  numpy.fromstring(raw_image, dtype='uint8')
    frame = frame.reshape((h,w,c))
    # throw away the data in the pipe's buffer.
    # pipe.stdout.flush()


    if(k % N == 0):
        t_prev = t
        t = timeit.default_timer()
    
    fps = N/(t-t_prev)

    cv2.putText(frame, "fps: {0:.1f}".format(fps), (0, 13), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

    # # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

# Hack not to "hang" the window in *nix systems (Linux,Mac)
cv2.waitKey(1)

