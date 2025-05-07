import serial
import time
import configparser
parser = configparser.ConfigParser()
parser.read("src/config.cfg")

#This code handles setting robot joint angles and serial communication with the Arduino Uno in the Robot Arm


port = parser['Serial'].get('port')
baud_rate = parser['Serial'].getint('baudrate')
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
def reset():
    array = parser.get('Arm', 'servoResets')
    arr = [value.strip() for value in array.split(',')]
    ints = list(map(int, arr))
    updateArm(ints.copy())
def release():
    values = [0,0,0,0,0]
    data = ' '.join(str(v) for v in values) + '\n' # Create a space-separated string ending with a newline
    ser.write(data.encode())
    response = ser.readline().decode().strip()
    print(response)
def close():
    print("Closing Serial")
    ser.close()
    



