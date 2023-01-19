import cv2 as cv
import numpy as np

class VisionBrain:
    def __init__(self    
                 ,mtx#mtx
                 ,dist#dist
                 ,arucoDict=cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_50)
                 ,arucoParams = cv.aruco.DetectorParameters_create()
                 ,arucoSize = 0.025
                 ):
        self.arucoDict = arucoDict
        self.arucoParams = arucoParams
        self.arucoSize = arucoSize
        self.mtx=mtx
        self.dist=dist
    def checkAruco(self,imgs,fileName=None):
        ret =[]
        ct=0
        for i in imgs:
            corners, ids, rejectedImgPoints = self.__detectAruco(np.array(i))
            if corners:
                rvecs,tvecs = self.__locateAruco(corners)
                ret.append([(a[0],b[0],c[0]) for a,b,c in zip(tvecs,rvecs,ids)])
                if fileName:
                    imaxis = cv.aruco.drawDetectedMarkers(i.copy(), corners, ids)
                    if len(tvecs)>0:
                        for i in range(len(tvecs)):
                            imaxis = cv.aruco.drawAxis(imaxis, self.mtx, self.dist, rvecs[i], tvecs[i], (self.arucoSize)/2)
                    cv.imwrite('picture/'+str(fileName)+str(ct)+'.png',imaxis)
                    ct+=1

        #partie du code qui boucle sur ret pour check si oui ou non on est bien calibre
        return ret
                    
    def __locateAruco(self,corners):
        return  cv.aruco.estimatePoseSingleMarkers(corners,self.arucoSize,self.mtx,self.dist)
    def __detectAruco(self,img):
        return cv.aruco.detectMarkers(img, self.arucoDict, parameters=self.arucoParams)






