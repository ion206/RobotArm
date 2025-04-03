import serial
import time

#This code handles setting robot joint angles and serial communication with the Arduino Uno in the Robot Arm

port = '/dev/cu.usbmodem1301'  #Running on USB Moden USB3 Port 1
baud_rate = 11500
ser = serial.Serial(port, baud_rate, timeout=1)
init = False
def init(): 
    print("Initilizing Serial with Arduino...")
    time.sleep(2)  # Wait for Arduino to reset and establish connection
    init = True

def updateArm(values):
    if not init:
        print("Controller not initialized")
        return
    data = ' '.join(str(v) for v in values) + '\n' # Create a space-separated string ending with a newline
    ser.write(data.encode())
    #print("Sent:", data.strip())
    # Read the response from Arduino
    response = ser.readline().decode().strip()
    return response # Returns the response from the Arduino


def close():
    print("Closing Serial")
    ser.close()


