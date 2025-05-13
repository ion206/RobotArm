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
ser = None
init = False

claw = 90 #Claw is open by default
currentPosition = [0,0,0]

def init(): 
    print("Initilizing Serial with Arduino...")
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
    except:
        print("Error initilizing Arduino .. is it plugged in?")
    time.sleep(2)  # Wait for Arduino to reset and establish connection
    init = True

def closeClaw():
    claw = 0
    return claw

def openClaw():
    claw = 90
    return claw

def updateArm(values):
    if not init:
        print("Controller not initialized")
        return
    values[0] = int((values[0] * 100/180)+80)
    values[1] = (180-(values[1]-25))
    values[2] = values[2] + 45
    values[3] = int(values[3] * (180/130))
    data = ' '.join(str(v) for v in values) + '\n' # Create a space-separated string ending with a newline
    ser.write(data.encode())
    print("Sent:", data.strip())
    # Read the response from Arduino
    response = ser.readline().decode().strip()
    return response # Returns the response from the Arduino


def goToPos(endPos):
    #Given an end goal position, generate and follows a trapezoidal path from current position
    #note, this function runs in coordinate plane LOCAL to the robot base
    motion = trap.trapXYZ(currentPosition, endPos)
    for pointarr in motion:
        angles = IK.getAngs([(pointarr[0]) / 1000, (pointarr[1]) / 1000, (pointarr[2])/1000])
        angles[4] = claw
        updateArm(angles.copy())
        delay(dt)
    currentPosition = endPos
    return 0

def reset():
    array = parser.get('Arm', 'ResetPos')
    arr = [value.strip() for value in array.split(',')]
    ints = list(map(int, arr))
    gotoPos(ints.copy(), ints.copy())

def release():
    values = [0,0,0,0,0]
    data = ' '.join(str(v) for v in values) + '\n' # Create a space-separated string ending with a newline
    ser.write(data.encode())
    response = ser.readline().decode().strip()
    print(response)
def close():
    print("Closing Serial")
    ser.close()
    



