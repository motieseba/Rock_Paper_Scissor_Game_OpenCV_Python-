import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import numpy.random as rd

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

detector = HandDetector(maxHands=1)
timer =0
stateResult = False
startGame = False
scores = [0, 0]
while True:
    imgBG = cv2.imread("resourses/BG.png")


    success, img = cap.read()

    imgScaled = cv2.resize(img,(0,0),None,0.875,0.875)
    imgScaled = imgScaled[:,80:480]

    hands, img = detector.findHands(imgScaled)
    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG,str(int(timer)),(605,435),cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255),4)

        if timer > 3 :
            stateResult = True
            timer = 0
            if hands:
                hand = hands[0]
                fingers = detector.fingersUp(hand)
                print(fingers)
                if fingers ==[0,0,0,0,0]:
                    playermove= 1
                if fingers == [1, 1, 1, 1, 1]:
                    playermove = 2
                if fingers == [0, 1, 1, 0, 0]:
                    playermove = 3

                RPS=[1,2,3]
                p=[0.5,0.25,0.25]
                randomNumber = rd.choice(RPS,1,p=p, replace=False)
                imgAI = cv2.imread(f'resourses/{randomNumber[0]}.png',cv2.IMREAD_UNCHANGED)
                imgBG = cvzone.overlayPNG(imgBG, imgAI ,(149,310))

                if (playermove ==1 and randomNumber[0]==3) or (playermove == 2 and randomNumber[0] == 1) or  (playermove == 3 and randomNumber[0] == 2):
                    scores[1] += 1
                if (playermove ==3 and randomNumber[0]==1) or (playermove == 1 and randomNumber[0] == 2) or  (playermove == 2 and randomNumber[0] == 3):
                    scores[0] += 1

    imgBG[234:654,795:1195]= imgScaled
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    cv2.imshow("BG",imgBG)


    key =cv2.waitKey(1)
    if key == ord('s'):
        startGame=True
        initialTime = time.time()
        stateResult = False
