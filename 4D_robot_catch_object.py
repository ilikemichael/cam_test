import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

# 控制伺服馬達sg90給予初始位置
angle = 180  # 轉到180度的位置
CONTROL_PIN = 17  # bcm17腳位控制
PWM_FREQ = 50  # 頻率hz
GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)
pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)
# 控制伺服馬達sg90到初始位置
def moving(angle):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    print(duty_cycle)
    time.sleep(2)
    return pwm.ChangeDutyCycle(duty_cycle)  # 轉動到180度


# 啟動Camera設定變數
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
rows, cols, _ = frame.shape
x_medium = int(cols/2)
center = int(cols/2)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # color to gray
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #yellow color
    low_yellow = np.array([26, 43, 46])
    high_yellow = np.array([34, 255, 255])
    yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)

    contours, _ = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contrours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

    for cnt in contrours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        x_medium = int((x + x + w)/2)
        cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 0, 255), 2)
        break

    # 顯示圖片
    cv2.imshow('frame', frame)
    cv2.imshow("Mask", yellow_mask)
    # 按下 q 鍵離開迴圈
    if cv2.waitKey(1) == ord('q'):
        break
    if x_medium < center:
        angle += 1
    elif x_medium > center:
        angle -= 1

    moving(angle)

# 釋放該攝影機裝置
cap.release()
cv2.destroyAllWindows()
# 釋放GPIO
pwm.stop()
GPIO.cleanup()