import serial
import time
import configparser # Config Info

from robotControl import trapezoidalMotion as trap
from robotControl import getAngles as IK


parser = configparser.ConfigParser()
parser.read("src/config.cfg")

#This code handles setting robot joint angles and serial communication with the Arduino Uno in the Robot Arm

#Arduino USB Port and baudrate
port = parser['Serial'].get('port')
baud_rate = parser['Serial'].getint('baudrate')
dt = float(parser['Motion'].get('dt'))


class robotController:
    ser = None
    init = False

    claw = 0 #Claw is open by default
    currPos = [0, 150, 79]
    values = [0,0,0,0,0]

    def __init__(self): 
        print("Initilizing Serial with Arduino...")
        try:
            self.ser = serial.Serial(port, baud_rate, timeout=1)
        except:
            print("Error initilizing Arduino .. is it plugged in?")
        time.sleep(2)  # Wait for Arduino to reset and establish connection
        IK.init_plot()
        self.init = True
        self.reset()
        

    def closeClaw(self):
        self.claw = 0
        return self.claw

    def openClaw(self):
        self.claw = 90
        return self.claw

    def updateArm(self):
        if not self.init:
            print("Controller not initialized")
            return
        angle = [0,0,0,0,0]
        angle[0] = int((self.values[0] * 100/180)+80)
        angle[1] = (180-(self.values[1]-25))
        angle[2] = self.values[2] + 45
        angle[3] = int(self.values[3] * (180/130))
        angle[4] = int(self.claw)
        data = ' '.join(str(a) for a in angle) + '\n' # Create a space-separated string ending with a newline
        self.ser.write(data.encode())
        #print("Sent:", data.strip())
        # Read the response from Arduino
        response = self.ser.readline().decode().strip()
        return response # Returns the response from the Arduino


    def goToPos(self,endPos, smoothing):
        #Given an end goal position, generate and follows a trapezoidal path from current position
        #note, this function runs in coordinate plane LOCAL to the robot base
        if smoothing == True:
            motion = trap.trapXYZ(self.currPos, endPos.copy())
            if motion != 0:
                for pointarr in motion:
                    self.values = IK.getAngs([pointarr[0] / 1000, pointarr[1] / 1000, pointarr[2] / 1000])
                    self.updateArm()
                    time.sleep(dt)
        else:
            self.values = IK.getAngs([(endPos[0]) / 1000, (endPos[1]) / 1000, (endPos[2])/1000])
        self.updateArm()
        self.currPos = endPos
        #print(self.currPos)
        return 0

    def reset(self):
        array = parser.get('Arm', 'ResetPos')
        arr = [value.strip() for value in array.split(',')]
        ints = list(map(int, arr))
        self.goToPos(ints.copy(), False)

    def release(self):
        vals = [0,0,0,0,0]
        data = ' '.join(str(v) for v in vals) + '\n' # Create a space-separated string ending with a newline
        self.ser.write(data.encode())
        response = self.ser.readline().decode().strip()
        print(response)

    def close(self):
        print("Closing Serial")
        self.ser.close()
        
        



