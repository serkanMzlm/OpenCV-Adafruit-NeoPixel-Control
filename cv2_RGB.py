import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os
import serial

sericom = serial.Serial("COM10",9600)
sericom.timeout = 1
cap = cv2.VideoCapture(0)
cap.set(3, 1280) 
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8,maxHands=1)




class DragImg():
    def __init__(self, path, posOrigin, imgType):

        self.posOrigin = posOrigin
        self.imgType = imgType
        self.path = path

        if self.imgType == 'png': 
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)


        self.size = self.img.shape[:2] 




path = "png"
myList = os.listdir(path) 


listImg = []
for x, pathImg in enumerate(myList):
    if 'png' in pathImg:
        imgType = 'png'
    else:
        imgType = 'jpg'
    listImg.append(DragImg(f'{path}/{pathImg}', [400 + x * 150, 100], imgType))
    length1,length2,length3=0,0,0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']



        cursor = lmList[8]

        w,h = listImg[0].size
        
      
        xr,yr=listImg[0].posOrigin
        xg,yg=listImg[1].posOrigin
        xb,yb=listImg[2].posOrigin
        xrs, yrs = listImg[3].posOrigin

        if xr < cursor[0] < xr+w and yr < cursor[1] < yr+h :
            length, info, img = detector.findDistance(lmList[8], lmList[4], img,5,(0,0,255))
            length1=int((length/1000)*500)-15


        if xg < cursor[0] < xg + w and yg < cursor[1] < yg + h:
            length, info, img = detector.findDistance(lmList[8], lmList[4], img,5,(0,255,0))
            length2 = int((length/1000)*500)-15
            
        if xb < cursor[0] < xb + w and yb < cursor[1] < yb + h:
            length, info, img = detector.findDistance(lmList[8], lmList[4], img,5,(255,0,0))
            length3 = int((length/1000)*500)-15

        if xrs < cursor[0] < xrs + w and yrs < cursor[1] < yrs + h:
            length1 = 0
            length2 = 0
            length3 = 0
        

        e = '\n'


        if length1 > 99 :
            length1 = 100

        if length2 > 99:
           length2 = 100

        if length3 > 99 :
            length3= 100


        if length1 < 0:
            length1 = 0

        if length2 < 0:
            length2 = 0

        if length3 < 0:
            length3 = 0
        
        
        cv2.putText(img, str(int(length1)), (20, 30), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), 2)
        cv2.putText(img, str(int(length2)), (20, 60), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 0), 2)
        cv2.putText(img, str(int(length3)), (20, 90), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 0, 0), 2)
        d = (int(length1),int(length2),int(length3))

        a1 = str(d)
        
        sericom.write(a1.encode())
        sericom.write(e.encode())



    try:  

        for imgObject in listImg:

          
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            if imgObject.imgType == "png":
                
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
            else:
                img[oy:oy + h, ox:ox + w] = imgObject.img

    except:
        pass

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
