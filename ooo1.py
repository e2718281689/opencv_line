#!/usr/bin/env python3

# 识别的是中线为白色

import cv2
import numpy as np
import serial
import time



def getnumber12():
    while (1):
        fangxiang = str(ser.read(),"utf-8")
        ret, frame = cap.read()
        # 转化到HSV空间
        imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # mask不需要的部分
        mask = cv2.inRange(imgHSV, lower, upper)

        # 大津法二值化
        retval, dst = cv2.threshold(mask, 0, 255, cv2.THRESH_OTSU)
        # 膨胀，白区域变大
        dst = cv2.dilate(dst, None, iterations=2)
        # 腐蚀，白区域变小
        dst = cv2.erode(dst, None, iterations=6)
        cv2.imshow("dst3", dst)
        # 单看第400行的像素值v
        color1 = dst[300]
        try:
            # 找到白色的像素点个数
            white_count = np.sum(color1 == 255)
            # 防止white_count=0的报错
            if white_count == 0:
                white_count = 640

            # 找到白色的像素点索引
            white_index = np.where(color1 == 255)
            #########################################################################
            if white_count <= 200:
                # 找到白色像素的中心点位置 # 计算方法应该是边缘检测，计算白色边缘的位置和/2，即是白色的中央位置。
                center = (white_index[0][white_count - 1] + white_index[0][0]) / 2
                # 计算出center与标准中心点的偏移量，因为图像大小是640，因此标准中心是320，因此320不能改。
                direction = center - 320
                print(direction)
                if -20 < direction < 20:
                    com.write('F'.encode())
                elif direction <= -20:
                    if direction >-80:
                        com.write('e'.encode())
                    elif -140 < direction <= -80:
                        com.write('d'.encode())
                    elif -200 < direction <= -140:
                        com.write('c'.encode())
                    elif -260 < direction <= -200:
                        com.write('b'.encode())
                    elif -320 < direction <= -260:
                        com.write('a'.encode())
                elif direction >= 20:
                    if direction < 80:
                        com.write('f'.encode())
                    elif 80 <= direction < 140:
                        com.write('g'.encode())
                    elif 140 <= direction < 200:
                        com.write('h'.encode())
                    elif 200 <= direction < 260:
                        com.write('i'.encode())
                    elif 260 <= direction < 320:
                        com.write('j'.encode())
            elif white_count > 200:
                print('stop')
                com.write('S'.encode())
                if fangxiang == 'L':
                    print('left')
                    com.write('L'.encode())
                elif fangxiang == 'R':
                    print('Right')
                    com.write('R'.encode())
        ########################################################################
        except:
            continue
    #########################################################################3###
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
   
ser=serial.Serial("/dev/ttyUSB1",115200,timeout=0.1)
com=serial.Serial("/dev/ttyUSB0",9600,timeout=0.1)

lower = np.array([0, 60, 0])
upper = np.array([179, 255, 255])

# center定义
center = 320
# 打开摄像头，图像尺寸640*480（长*高），opencv存储值为480*640（行*列）
cap = cv2.VideoCapture(0)
while True:
    number = str(ser.read(),"utf-8")
    if number == '1' or number == '2':
        print('begin')
        time.sleep(1)
        getnumber12()
cap.release()  # 释放cap
cv2.destroyAllWindows()  # 销毁所有窗口
