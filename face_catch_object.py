import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

# 控制伺服馬達sg90
angle = 180  # 轉到180度的位置
CONTROL_PIN = 17  # bcm17腳位控制
PWM_FREQ = 50  # 頻率hz
GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)
pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)
# 控制伺服馬達sg90到初始位置
duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
print(duty_cycle)
pwm.ChangeDutyCycle(duty_cycle)  # 轉動到180度
time.sleep(2)

# 啟動Camera設定變數
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
rows, cols, _ = frame.shape
x_medium = int(cols/2)
center = int(cols/2)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    ret, imagename = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    faces = faceCascade.detectMultiScale(imagename, scaleFactor=1.1, minNeighbors=5, minSize=(30,30), flags = cv2.CASCADE_SCALE_IMAGE)
    cv2.rectangle(imagename, (10,imagename.shape[0]-20), (110,imagename.shape[0]), (0,0,0), -1)
    cv2.putText(imagename,"Find " + str(len(faces)) + " face!", (10,imagename.shape[0]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
    for (x,y,w,h) in faces:
        cv2.rectangle(imagename,(x,y),(x+w, y+h),(128,255,0),2)
    cv2.namedWindow("facedetect")
    cv2.imshow("facedetect", imagename)

    x_medium = int((imagename.shape[1]) / 2)
    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 0, 255), 2)

    k = cv2.waitKey(1)
    # 按下 z 鍵離開迴圈
    if k == ord("z") or k == ord("Z"):
        break

    if x_medium < center:
        angle += 1
    elif x_medium > center:
        angle -= 1

    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    print(duty_cycle)
    pwm.ChangeDutyCycle(duty_cycle)  # 跟著改變的angle轉動

# 釋放該攝影機裝置
cap.release()
cv2.destroyWindow("facedetect")

# 釋放GPIO
pwm.stop()
GPIO.cleanup()