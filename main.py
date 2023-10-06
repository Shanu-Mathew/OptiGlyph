import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np


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
finalText=""



def drawALL(img,buttonList):
    imgNew=np.zeros_like(img,np.uint8)
    for button in buttonList:
        x,y=button.pos
        cvzone.cornerRect(imgNew,(button.pos[0],button.pos[1],button.size[0],button.size[1]),
                          50,rt=0,colorC=(10,10,10))
        w,h=button.size
        cv2.rectangle(imgNew,button.pos,(x+w,y+h),(50,50,50),cv2.FILLED)
        cv2.putText(imgNew,button.text,(x+8,y+40),
                cv2.FONT_HERSHEY_PLAIN,
                3,(255,255,255),3)
    out=img.copy()
    alpha=0.2
    mask=imgNew.astype(bool)
    out[mask]=cv2.addWeighted(img,alpha,imgNew,1-alpha,0)[mask]
    return out

class Button():
    def __init__(self,pos,text,size=[45,45], button_id=None, action=None):
        self.pos=pos
        self.size=size
        self.text=text
        self.button_id = button_id  
        self.action = action
           

buttonList= []
for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([j*50+50,50*i+50],key))

#Adding Clear Button
buttonList.append(Button([350, 300], "CLEAR", size=[170, 50], button_id="CLEAR", action="CLEAR"))

# Add Space Button
buttonList.append(Button([100, 300], "SPACE", size=[170, 50], button_id="SPACE", action="SPACE"))

while True:
    success, img =cap.read()
    img=cv2.flip(img,1)
    hand,img=detector.findHands(img)
    img=drawALL(img,buttonList)
    
    if hand:
        hand1=hand[0]
        lmList=hand1["lmList"]
        if lmList:
            for button in buttonList:
                x,y=button.pos
                w,h=button.size
                if x<lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                    cv2.rectangle(img,button.pos,(x+w,y+h),(0,0,0),cv2.FILLED)
                    cv2.putText(img,button.text,(x+8,y+40),
                            cv2.FONT_HERSHEY_PLAIN,
                            3,(255,255,255),3)
                    l,_,_=detector.findDistance(lmList[8][0:2],lmList[12][0:2],img)
                
                    #Button Press Code
                    if l<30:
                        cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                        cv2.putText(img,button.text,(x+8,y+40),
                                cv2.FONT_HERSHEY_PLAIN,
                                3,(0,0,0),3)
                        if button.action == "CLEAR":
                            finalText = finalText[:-1]
                        elif button.action == "SPACE":
                            finalText += " "
                        else:
                            finalText += button.text
                        sleep(0.3)
                
    cv2.rectangle(img,(50,200),(545,250),(0,0,0),cv2.FILLED)
    cv2.putText(img,finalText,(55,240),
                cv2.FONT_HERSHEY_PLAIN,
                3,(255,255,255),3)            
                

    cv2.imshow('Image',img)
    cv2.waitKey(1)
