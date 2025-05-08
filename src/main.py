import cv2
import math
import time

from markerTracking import tagPositioner as tags
from robotControl import robotController as RC
from robotControl import getAngles as IK
from marker import Marker

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
#IK.init_plot()

marker4 = Marker(4, [0,0], [0,0,0])

RC.reset()
z = 0
grab = 90
delay = 0
while True:
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            markers = tags.getpos(frame) #Get Marker 4 world xy position
            marker4.updatePos(markers) #Update Marker4 object
            #Calculate InverseKinematics of the position relative to the arm's X & Y
            armVals = IK.getAngs([(marker4.x-armX) / 1000, (marker4.y-armY) / 1000, z])
            armVals[4] = grab
            RC.updateArm(armVals.copy())  #Send Servo Values to robot
    print(marker4)
    cv2.imshow('Aruco Pose Estimation', frame)
                
    if cv2.waitKey(1) & 0xFF == ord('q'):
        RC.reset()
        time.sleep(1)
        RC.release()
        RC.close()
        cap.release()
        cv2.destroyAllWindows()
        break

    
