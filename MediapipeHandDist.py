import cv2
import mediapipe as mp
import serial
import time

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

def write(x):
     arduino.write(bytes(x, 'utf-8'))

def mapping(v, in_min, in_max, out_min, out_max):
    if v < in_min:
        v = in_min
    if v > in_max:
        v = in_max
    return int((v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0) 

while True:
    success, image = cap.read()
    if not success:
        continue
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
   

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            handLandmarks = []
            for landmarks in hand_landmarks.landmark:
                handLandmarks.append([landmarks.x, landmarks.y])
        thumbx=int(handLandmarks[4][0]*640)
        thumby=int(handLandmarks[4][1]*480)
        indexx=int(handLandmarks[8][0]*640)
        indexy=int(handLandmarks[8][1]*480)
        dist=((thumbx-indexx)**2+(thumby-indexy)**2)**0.5
        
        

        pwm=mapping(dist,17,240,0,255)
        print(pwm)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        # textoffset = cv2.getTextSize(str(pwm), font, 1, 2)[0]
        # textx=int((thumbx+indexx-textoffset[0])/2)
        # texty=int((thumby+indexy-textoffset[1])/2)
        cv2.putText(image,str(pwm), (10,50), font, 1, (255, 0, 0), 2)
        image =cv2.line(image,(thumbx,thumby),(indexx,indexy),(255,0,0), 5)
        write(str(pwm))
    cv2.imshow('MediaPipe Hands', image)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break