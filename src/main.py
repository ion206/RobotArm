import cv2
import math
import time

from markerTracking import tagPositioner as tags
from robotControl import robotController as RC
from robotControl import getAngles as IK
from marker import Marker

#Getting values from the Config File
import configparser
parser = configparser.ConfigParser()
parser.read("src/config.cfg")
shoulder = parser['Arm'].getint('shoulderArm') #Shoulder Length
elbow = parser['Arm'].getint('elbowArm') #Elbow Arm Length
wrist = parser['Arm'].getint('wristArm') #Wrist+Claw(Closed) Length
armX = parser['Arm'].getint('armXpos') #Arm X-position in desk coords
armY = parser['Arm'].getint('armYpos') #Y Pos in desk coords


#Init Camera, init Robot
cap = cv2.VideoCapture(0)
RC.init()

#IK.init_plot()

#Finding, markers with IDs 4,5,6
marker4 = Marker(4, [0,0], [0,0,0])
marker5 = Marker(4, [0,0], [0,0,0])
marker6 = Marker(4, [0,0], [0,0,0])


RC.reset() #Zero Out robot a the start

z = 0
grab = 90
delay = 0

while True:
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            markers = tags.getpos(frame) #Get Marker Markers positions - stores in array of tuples
            marker4.updatePos(markers[0]) #Update Marker4 object
            marker5.updatePos(markers[1]) #Update Marker5 object
            marker6.updatePos(markers[2]) #Update Marker6 object

            #Calculate InverseKinematics of the position relative to the arm's X & Y
            #Divide by 1000 becuase IK requires input in Meters(m)
            armVals = IK.getAngs([(marker4.x-armX) / 1000, (marker4.y-armY) / 1000, z])
            armVals[4] = grab #Current Arm Grab poisition, Open:90, Closed:0

            RC.updateArm(armVals.copy())  #Send Servo Values to robot
    cv2.imshow('Aruco Pose Estimation', frame)
                

    #End Script on q-pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #Reset Robot, release servos, and close are serial/camera lines
        RC.reset() 
        time.sleep(1)
        RC.release()
        RC.close()
        cap.release()
        cv2.destroyAllWindows()
        break

    
