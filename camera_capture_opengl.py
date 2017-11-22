import cv2
import timeit

cap = cv2.VideoCapture(0)

# HD 720p
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
print(cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720))

# # Full HD 1080p
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920);
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080);

w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("(w,h) = ({:.0f},{:.0f})".format(w,h))

font = cv2.FONT_HERSHEY_SIMPLEX

N = 10
k = 0
t = timeit.default_timer()
t_prev = 0
cv2.namedWindow('frame',cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_OPENGL)
# cv2.namedWindow('frame',cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.GUI_EXPANDED | cv2.WINDOW_OPENGL)
fps=30

while(True):
    k += 1
    
    # Capture frame-by-frame
    ret, frame = cap.read()
    if(k % N == 0):
        t_prev = t
        t = timeit.default_timer()
        fps = N/(t-t_prev)
        print(fps)

    # Our operations on the frame come here
    # frame = cv2.flip(frame,1)

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    # cv2.putText(frame, "fps: {0:.1f}".format(fps), (0, 13), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

    # Display the resulting frame
    # cv2.imshow('frame',frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# When everything done, release the capture
cap.release()

cv2.destroyAllWindows()

# Hack not to "hang" the window in *nix systems (Linux,Mac)
cv2.waitKey(1)

