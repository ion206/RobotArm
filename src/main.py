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


cap = cv2.VideoCapture(0)
RC.init()
IK.init_plot()

marker4 = Marker(4, [0,0], [0,0,0])

RC.reset()
while True:
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            markers = tags.getpos(frame)
            marker4.updatePos(markers)
            armVals = IK.getAngs([(marker4.x-210) / 1000, (marker4.y-50) / 1000, 0])
            RC.updateArm(armVals.copy())
                

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