import cv2
from cvzone.HandTrackingModule import HandDetector

cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
else:
    cap.set(3, 640)
    cap.set(4, 480)

detector=HandDetector(detectionCon=0.8)
keys= [["Q","W","E","R","T","Y","U","I","O","P"],
       ["A","S","D","F","G","H","J","K","L",";"],
       ["Z","X","C","V","B","N","M",",",".","/"]]


def drawALL(img,buttonList):
    
    for button in buttonList:
        x,y=button.pos
        w,h=button.size
        cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
        cv2.putText(img,button.text,(x+8,y+40),
                cv2.FONT_HERSHEY_PLAIN,
                3,(0,0,0),3)
    return img

class Button():
    def __init__(self,pos,text,size=[45,45]):
        self.pos=pos
        self.size=size
        self.text=text
           

buttonList= []
for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([j*50+50,50*i+50],key))


while True:
    success, img =cap.read()
    hand,img=detector.findHands(img)
    img=drawALL(img,buttonList)
    
    if hand:
        for button in buttonList:
            x,y=button.pos
            w,h=button.size
            if x<hand[0][0]<x+w and y<hand[0][1]<y+h:
                cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                cv2.putText(img,button.text,(x+8,y+40),
                        cv2.FONT_HERSHEY_PLAIN,
                        3,(0,0,0),3)
                if button.text=="Q":
                    print("Q")
                if button.text=="W":
                    print("W")
                if button.text=="E":
                    print("E")
                if button.text=="R":
                    print("R")
                if button.text=="T":
                    print("T")
                if button.text=="Y":
                    print("Y")
                if button.text=="U":
                    print("U")
                if button.text=="I":
                    print("I")
                if button.text=="O":
                    print("O")
                if button.text=="P":
                    print("P")
                if button.text=="


    cv2.imshow('Image',img)
    cv2.waitKey(1)
