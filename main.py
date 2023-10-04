import cv2
from cvzone.HandTrackingModule import HandDetector

cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
else:
    cap.set(3, 640)
    cap.set(4, 480)

detector=HandDetector(detectionCon=0.8)

class Button():
    def __init__(self,pos,text,size=[50,50]):
        self.pos=pos
        self.size=size
        self.text=text
    def draw(self,img):
        x,y=self.pos
        w,h=self.size
        cv2.rectangle(img,self.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
        cv2.putText(img,self.text,(x+8,y+40),
                cv2.FONT_HERSHEY_PLAIN,
                3,(255,255,255),5)   
        return img 
    
myButton=Button([50,50],'Q')
while True:
    success, img =cap.read()
    hand,img=detector.findHands(img)
    
    img= myButton.draw(img)

    cv2.imshow('Image',img)
    cv2.waitKey(1)
