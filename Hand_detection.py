import cv2
import numpy as np
import pyautogui as mouse

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1980)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
hand_cascade = cv2.CascadeClassifier('hand.xml')
mouse.FAILSAFE = False
count = 0
prevx=0
prevy=0
import math

def getPoints(x1,y1,x2,y2):
    points=[]
    if(x1==x2 and y1==y2):
        return points
    dist=(y2-y1)*(y2-y1) + (x2-x1)*(x2-x1)
    dist=math.sqrt(dist)

    step=dist/3
    if(x1==x2):
        while(y1<y2):
            points.append((x1,y1))
            y1+=step
        return points

    slope=(y2-y1)/(x2-x1)
    theta=math.atan(slope)
    cos=math.cos(theta)
    sin=math.sin(theta)
    while dist>0:
        x1+=step*cos
        y1+=step*sin
        points.append((x1,y1))
        dist-=step
    return points

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hands = hand_cascade.detectMultiScale(gray, 1.5, 2)
    contour = hands
    contour = np.array(contour)

    if count == 0:

        if len(contour) == 2:
            cv2.putText(img=frame, text='Detection started', org=(int(100 / 2 - 20), int(100 / 2)),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1,
                        color=(0, 255, 0))
            for (x, y, w, h) in hands:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if count > 0:
        if len(contour) == 1:
            cv2.putText(img=frame, text='Detected', org=(int(100 / 2 - 20), int(100 / 2)),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1,
                        color=(0, 255, 0))

            for (x, y, w, h) in hands:
                l = getPoints(prevx,prevy,x,y)
                for i in l:
<<<<<<< Updated upstream
                    mouse.moveTo(i[0]*2, i[1]*2 )
=======
                    mouse.moveTo(i[0]*3, i[1]*2)
                    print(i[0]*3, i[1]*2)
>>>>>>> Stashed changes
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                prevx=x
                prevy=y
        elif len(contour) == 0:
            cv2.putText(img=frame, text='Where are you?', org=(int(100 / 2 - 20), int(100 / 2)),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1,
                        color=(0, 0, 255))

    count += 1

    cv2.imshow('lazyctr_frame', frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
