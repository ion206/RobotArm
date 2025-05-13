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

armX = parser['Arm'].getint('armXpos')
armY = parser['Arm'].getint('armYpos')


cap = cv2.VideoCapture(0)

#Initilize and reset the robot
RC.init()
RC.reset()

marker4 = Marker(4, [0,0], [0,0,0])
marker5 = Marker(5, [0,0], [0,0,0])
marker6 = Marker(6, [0,0], [0,0,0])
delay = 0
findObject = True
num = 0
while findObject:
    if cap.isOpened():
        ret, frame = cap.read()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            findObject = False
            cv2.imwrite('src/GeminiImage.jpg', frame)
        if ret:
            markers = tags.getpos(frame) #Get Marker 4 world xy position
            print(markers)
            marker4.updatePos(markers[0]) #Update Marker4 object
            marker5.updatePos(markers[1]) #Update Marker4 object
            marker6.updatePos(markers[2]) #Update Marker4 object
            print(marker5)
            print(marker6)
    cv2.imshow('Aruco Pose Estimation', frame)
    

#IK.init_plot()


#objectpos = [marker4.x, marker4.y, 0]
object5pos = [marker5.x, marker5.y, 0]
#object2pos = [130, 200, 0]h
object6pos = [marker6.x, marker6.y, 0]
command = input("Enter Command: ")
row = api.sendCommand(command, object5pos, object6pos, num)
print(row)
for i in range(len(row)):
    x=int(row[i]['x'])
    y=int(row[i]['y'])
    z=int(row[i]['z'])
    if(x==0 and y==0 and z==0):
        print("RESET")
        RC.reset()
    delay=int(row[i]['delay'])
    claw = int(row[i]['claw'])
    print("x: ", x, " y: ", y, "z: ", z, "delay: ", delay, "claw: ", claw)
    RC.goToPos([(x-armX), (y-armY), (z-60)])
    if claw == 1:
        RC.closeClaw()
    else:
        RC.openClaw()
    time.sleep(row[i]['delay'])
RC.release()
RC.close()
print("End")


