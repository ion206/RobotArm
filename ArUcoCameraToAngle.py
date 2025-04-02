import tagPositioner as tags
import cv2
import math
import serial
import time
import struct

cap = cv2.VideoCapture(0)

 # Set your serial port and baud rate (match Arduino's Serial.begin(9600))
port = '/dev/cu.usbmodem1301'  # e.g., on Linux; change to 'COM3' on Windows if needed
baud_rate = 11500

armx = 0
army = -0.15
ser = serial.Serial(port, baud_rate, timeout=1)

    # Wait for the serial connection to initialize
time.sleep(2)

transforms = None

# Initialize servo angles for servos 1-4 with default values (e.g., 90°)
servo_angles = [150, 90, 90, 90]

while True:
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            transforms = tags.getpos(frame)

    arm = [100*abs(transforms[0][1]+army), 100*abs(transforms[0][0]+armx)-40, 100*(transforms[0][2])]
    marker = [(100*transforms[2][0])+170,100*(transforms[2][1])]
    if arm[0] != 0 or marker[0] != 0:
        angle = (math.atan((abs(marker[1])-arm[1])/(marker[0]-arm[0])))
    if(angle > 0):
        servo_angles[3] = int(math.degrees(angle))
    print(servo_angles)
    msg = "{},{},{},{}\n".format(*servo_angles)
    ser.write(msg.encode())
    print("Sent:", msg.strip())
    cv2.imshow('Aruco Pose Estimation', frame)
    time.sleep(0.05)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break