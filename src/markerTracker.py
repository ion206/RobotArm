from makerTracking import tagPositioner as tags
from robotControl import robotController as RC
from robotControl import inverseKinematics as IK
from marker import Marker
import cv2
import math

cap = cv2.VideoCapture(0)
RC.init()

marker4 = Marker(4, [0,0], [0,0,0])

armVals = [160,40,90,60,0]
zbias = -30

while True:
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            markers = tags.getpos(frame)
            marker4.updatePos(markers)
            armVals[3] = IK.baseAngle(marker4.x,marker4.y, zbias)
            RC.updateArm(armVals.copy())

    print(marker4)
    cv2.imshow('Aruco Pose Estimation', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        RC.close()
        cap.release()
        cv2.destroyAllWindows()
        break