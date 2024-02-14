import cv2
from cvzone.HandTrackingModule import HandDetector
import time

class Button:
    def __init__(self, pos, width, height, value):

        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):

        cv2.rectangle(img, self.pos, (self.pos[0] + self.width,self.pos[1] + self.height), (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width,self.pos[1] + self.height), (50,50,50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 55, self.pos[1] + 100), cv2.FONT_HERSHEY_PLAIN, 4, (50, 50, 50), 2)

    def checkclick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and\
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255),
                          cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
            cv2.putText(img, self.value, (self.pos[0] + 45, self.pos[1] + 110), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0),
                        4)
            return True
        else:
            return False



cap = cv2.VideoCapture(0)
cap.set(5,1980)
cap.set(6,1080)

detector = HandDetector(detectionCon=0.8)

buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]

buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x * 150 + 800
        ypos = y * 150 + 150
        buttonList.append(Button((xpos,ypos),150,150,buttonListValues[y][x]))

myEqn = ''
delayCounter = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)

    hands, img = detector.findHands(img, flipType=False)

    cv2.rectangle(img, (800,40), (800 + 600 , 150 + 150), (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (800,40), (800 + 600, 150 + 150), (50, 50, 50), 3)

    for button in buttonList:
        button.draw(img)

    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        x,y = lmList[8][:2]
        if length < 50:
            for i,button in enumerate(buttonList):
                if button.checkclick(x,y) and delayCounter == 0:
                    myValue = buttonListValues[int(i%4)][int(i/4)]
                    if myValue == "=":
                        myEqn = str(eval(myEqn))
                    else:
                        myEqn += myValue
                    delayCounter = 1

    if delayCounter != 0 :
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0


    cv2.putText(img, myEqn, (810,115), cv2.FONT_HERSHEY_PLAIN, 4, (50, 50, 50), 2)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('c'):
        myEqn = ''

