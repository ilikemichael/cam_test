import cv2

cv2.VideoCapture(0)
cap = cv2.VideoCapture(0)                           # a USB videocam
waitframe = 100                                       # frames per second
while True:                                         # an infinite while loop til Esc key pressed
    success, img = cap.read()
    if not success:
        break
    cv2.imshow("Video", img)
    ch = cv2.waitKey(waitframe)
    if ch == 27 or ch == ord('q') or ch == ord('Q'):
        cv2.waitKey(300)
        print('Quitting')
        break
cap.release()
cv2.destroyAllWindows()