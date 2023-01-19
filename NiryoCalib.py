#!/usr/bin/venv python3
#import rospy
def p(s):
    print(s)
from Calib_RosWrapper import RosWrapperCalib
from VisionBrain import VisionBrain
import numpy as np
import os
import simplejson as json
import time as t
class NiryoCalib:
    def __init__(self): 
        self.__filepath = os.path.realpath(__file__)
        self.wrap=RosWrapperCalib()
        mtx,dist = self.wrap.cameraCalibrationDefault()
        mtx=np.array(mtx).reshape(3,3)
        self.view = VisionBrain(mtx=mtx,dist=dist)
    def setCalibration(self):
        for i in range(2):
            if self.wrap.forceCalibration():
                pass
        
        #normalement y'a une fonction de recherche
        self.__selfViewDefaultPosition()
        img = self.wrap.Vision.getImage('test')
        ret = self.view.checkAruco([img], fileName='testAxis')

        self.__ConfigToJson(ret[0], list(self.wrap.niryo.get_joints()))
        self.__defaultPosition()

    def Calibration(self):
        for i  in range(5):
            if self.wrap.forceCalibration():
                if self.CheckPosition():
                    return True
        return False


    def CheckPosition(self):
        if not os.path.exists(os.path.dirname(self.__filepath)+'/config.json'):
            self.setCalibration()
        data = self.JsonToConfig()
        data = [data[a] for a in data if 'Aruco' in a]
        self.__selfViewDefaultPosition()
        img = self.wrap.Vision.getImage()
        ret = self.view.checkAruco([img], fileName='checkAxis')
        
        self.__defaultPosition()
        if len(data)!=len(ret):
            print("pas le meme nombre d aruco entre les deux comparaisons")
            return False
        ret=ret[0]
        err=[]
        for d in data:
            print(d['id'])
            paired = [(d,r)for r in ret if str(r[2])==d['id']][0]
            old_tvecs= paired[0]['tvecs']
            old_rvecs= paired[0]['rvecs']
            for a, b in zip(old_tvecs,r[0]):
                err.append( abs(a-b) )
                #print(abs(a-b))
            mean =sum(err)/len(err)
            print(mean)
            self.__defaultPosition()
            if mean<0.005:#(en gros quand on se trompe d'un demi centimetre en moyenne)
                return True
            else : 
                return False
    def __selfViewDefaultPosition(self):
        self.wrap.move(0, -0.8, -0.4, -0.1, -1.7, 0)
    def __defaultPosition(self):
        self.wrap.move_to_sleep_pose()

    def __ConfigToJson(self, ret, joints):
        data={}
        for r in ret:
            data['Aruco'+str(r[2])]={"tvecs":list(r[0]),'rvecs':list(r[1]),'id':str(r[2])}
        with open(os.path.dirname(self.__filepath)+"/config.json","w") as f:
            json.dump(data,f, indent=4)
    def JsonToConfig(self):
        with open(os.path.dirname(self.__filepath)+'/config.json') as f:
            return json.load(f)
#n=NiryoCalib()
#n.setCalibration()
#print(n.Calibration())
#print(n.CheckPosition())
