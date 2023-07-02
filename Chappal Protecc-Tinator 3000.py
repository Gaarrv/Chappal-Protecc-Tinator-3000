
#MAIN PROJECT
#Chappal Protecc-Tinator 3000

import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import os
import pyautogui




wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
browserExe = "chrome.exe"

detector = htm.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volPer = 0
volBar = 400
browserExe = "chrome.exe"
a = 0

is_paused = False



while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        x3, y3 = lmList[20][1], lmList[20][2]
        x4, y4 = (100, 200)
        x5, y5 = lmList[0][1], lmList[0][2]
        x6, y6 = lmList[16][1], lmList[16][2]


        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 10, (255, 127, 0), cv2.FILLED)
        # cv2.circle(img, (x4, y4), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x5, y5), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x6, y6), 10, (0, 0, 255), cv2.FILLED)
        #cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        #cv2.line(img, (x3, y3), (x4, y4), (255, 0, 0), 3)
        cv2.line(img, (x5, y5), (x6, y6), (0, 0, 255), 3)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)


        lenght = math.hypot(x2-x1, y2-y1)
        len2 = (((x4 - x3)**2 + (y4 - y3)**2)**0.5)
        len3 = (((x6 - x5)**2 + (y6 - y5)**2)**0.5)



        vol = np.interp(lenght, [40, 300], [minVol, maxVol])
        volBar = np.interp(lenght, [100, 300], [400, 150])
        volPer = np.interp(lenght, [100, 300], [0, 100])
        print("Length between Ring finger and Palm: ", int(len3))
        print("Length between Hand and Fixed Point: ", int(len2))
        print("Length between Pointer and Thumb: ", int(lenght))


        volume.SetMasterVolumeLevel(vol, None)


        if len3 < 100 and is_paused is False:
            pyautogui.press("space")
            print('PAUSED')
            is_paused = not is_paused

        if is_paused is True:
            cv2.putText(img, f'VIDEO PAUSED', (40, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

        if is_paused is True and len3 > 100:
            pyautogui.press("space")
            print('PLAYED')
            is_paused = False


        if len2 > 360:
            os.system("taskkill /f /im " + browserExe)
            print("Chrome Tab has been Successfully Compromised")


    cv2.rectangle(img, (50, 150), (85, 400), (0, 252, 124), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 252, 124), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}%', (45, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 252, 124), 2)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    #cv2.putText(img, f'FPS:{int(fps)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

    cv2.imshow("Chappal Protecc-Tinator 3000", img)
    cv2.waitKey(1)
