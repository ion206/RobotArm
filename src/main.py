import tagPositioner as tags
import robotController as RC
import inverseKinematics as IK
from marker import Marker
import cv2
import math
import time

cap = cv2.VideoCapture(0)
RC.init()

marker4 = Marker(4, [0,0], [0,0,0])

armVals = [160,20,90,60,0]

while True:
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            markers = tags.getpos(frame)
            marker4.updatePos(markers)
            armVals = IK.getAngs(marker4.x,marker4.y, 7, 80, 100)
            RC.updateArm(armVals)

    print(marker4)
    cv2.imshow('Aruco Pose Estimation', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        RC.close()
        cap.release()
        cv2.destroyAllWindows()
        break

