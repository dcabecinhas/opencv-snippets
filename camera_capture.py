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
cap.set(cv2.CAP_PROP_FRAME_WIDTH,424);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240);

font = cv2.FONT_HERSHEY_SIMPLEX

N = 10
k = 0
t = timeit.default_timer()
t_prev = 0
while(True):
    k += 1
    
    # Capture frame-by-frame
    ret, frame = cap.read()

    if(k % N == 0):
        t_prev = t
        t = timeit.default_timer()
        print("fps: ",N/(t-t_prev))

    # Our operations on the frame come here
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # fps = N/(t-t_prev)

    # cv2.putText(frame, "fps: {0:.1f}".format(fps), (0, 13), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

    # # Display the resulting frame
#    cv2.imshow('frame',frame)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break

# When everything done, release the capture
cap.release()

cv2.destroyAllWindows()

# Hack not to "hang" the window in *nix systems (Linux,Mac)
cv2.waitKey(1)

