import cv2
import math
import time

from apis import geminiAPI as api

from markerTracking import tagPositioner as tags
from robotControl import robotController as RC
from robotControl import getAngles as IK
from marker import Marker
import numpy as np

import configparser
parser = configparser.ConfigParser()
parser.read("src/config.cfg")

shoulder = parser['Arm'].getint('shoulderArm')
elbow = parser['Arm'].getint('elbowArm')
wrist = parser['Arm'].getint('wristArm')
armX = parser['Arm'].getint('armXpos')
armY = parser['Arm'].getint('armYpos')


cap = cv2.VideoCapture(0)
RC.init()


RC.reset()



marker4 = Marker(4, [0,0], [0,0,0])
grab = 90
delay = 0
findObject = True
num = 0
while findObject:
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            markers = tags.getpos(frame) #Get Marker 4 world xy position
            marker4.updatePos(markers) #Update Marker4 object
    cv2.imshow('Aruco Pose Estimation', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        findObject = False
        cv2.imwrite('src/GeminiImage.jpg', frame)

IK.init_plot()


#objectpos = [marker4.x, marker4.y, 0]
objectpos = [410, 100, 0]
object2pos = [130, 200, 0]
command = input("Enter Command: ")
row = api.sendCommand(command, objectpos, object2pos, num)
print(row)
for i in range(len(row)):
    print(str(row[i]['x']) + " " + str(row[i]['y']) + " " + str(row[i]['z']) + " " + str(row[i]['delay']))
    x=int(row[i]['x'])
    y=int(row[i]['y'])
    z=int(row[i]['z'])
    if(x==0 and y==0 and z==0):
        print("RESET")
        RC.reset()
    delay=int(row[i]['delay'])
    claw = int(row[i]['claw'])
    print("x: ", x, " y: ", y, "z: ", z, "delay: ", delay, "claw: ", claw)
    armVals = IK.getAngs([(x-armX) / 1000, (y-armY) / 1000, z/1000])
    if claw == 1:
        armVals[4] = 0
    else:
        armVals[4] = 90
    RC.updateArm(armVals.copy())
    time.sleep(row[i]['delay'])
RC.release()
RC.close()
print("End")


def pick(key):
    armVals = IK.getAngs([(marker4.x-armX) / 1000, (marker4.y-armY) / 1000, z/1000])
    RC.updateArm(armVals.copy())  #Send Servo Values to robot
    time.sleep(0.5)
    armVals[4] = 0
    grab = 0
    RC.updateArm(armVals.copy())  #Send Servo Values to robot

def release(key):
    grab = 90
