#识别形状

import cv2
import numpy as np
import serial
import time

cap = cv2.VideoCapture(0)
ser=serial.Serial("/dev/ttyUSB0",9600,timeout=0.1)

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print(area)
        if area>500:
            cv2.drawContours(imgContour, cnt, -1, (0, 0, 255), 3)
            peri = cv2.arcLength(cnt,True)
            #print(peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            #print(len(approx))
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            if objCor ==3:
                objectType ="Tri"
                ser.write('3'.encode())
                time.sleep(2)
                print('3')
            elif objCor == 4:
                objectType="Rectangle"
                ser.write('4'.encode())
                time.sleep(2)
                print('4')
            elif objCor>4:
                objectType= "Circles"
                ser.write('9'.encode())
                time.sleep(2)
                print('9')
            else:
                objectType="None"
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(imgContour,objectType,
                        (x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7,
                        (0,0,255),2)


while True:
    success, img = cap.read()

    imgContour = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    getContours(imgCanny)
    ser.write('0'.encode())
    print('0')
    cv2.imshow("Stacked Images", imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break