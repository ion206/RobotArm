import tagPositioner as tags
import robotController as RC
from marker import Marker
import cv2
import math
import time

cap = cv2.VideoCapture(0)
RC.init()

marker4 = Marker(4, [0,0], [0,0,0])

armVals = [135,90,90,90,0]

while True:
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            markers = tags.getpos(frame)
            marker4.updatePos(markers)

    print(marker4)
    cv2.imshow('Aruco Pose Estimation', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        RC.close()
        cap.release()
        cv2.destroyAllWindows()
        break

