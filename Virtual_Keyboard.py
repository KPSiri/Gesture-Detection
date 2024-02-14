import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8)
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]
finalText = ""
keyboard = Controller()

def drawAll(img , buttonList):

    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 12, y + 45), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    return img


class Button():
    def __init__(self,pos,text,size=[70,70]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


while True:
    success,img =cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList , bboxInfo = detector.findPosition(img)
    img = drawAll(img,buttonList)

    if lmList:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size

            if x<lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 150), cv2.FILLED)
                cv2.putText(img, button.text, (x + 12, y + 45), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

                l , _ , _ = detector.findDistance(8,12,img,draw=False)
                print(l)

                if l<40:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 200), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 12, y + 45), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

                    finalText += button.text
                    sleep(0.25)

    cv2.rectangle(img, (50,350), (700,450), (255,255,255), cv2.FILLED)
    cv2.putText(img, finalText, (60,425), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)


    cv2.imshow("Image",img)
    cv2.waitKey(1)
