import pygame
import time
from robotControl.robotController import robotController
from robotControl import getAngles as IK

# Initialize controller
pygame.init()
pygame.joystick.init()
RC = robotController()

# Wait for controller to connect
if pygame.joystick.get_count() == 0:
    raise Exception("No controller connected.")
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Connected to: {joystick.get_name()}")

# Arm joint state: base, shoulder, elbow, wrist, gripper
xyz = [200, 100, 50]
angles = [150, 90, 0 , 90, 90]

# Angle change rate per joystick input
delta = 4



while True:
    pygame.event.pump()  # Process events

    # Axes are between -1 and 1; you can scale this for control
    base_input = joystick.get_axis(0) if abs(joystick.get_axis(0)) >= 0.25 else 0 # Left stick horizontal
    shoulder_input = joystick.get_axis(1) if abs(joystick.get_axis(1)) >= 0.25 else 0  # Left stick vertical
    elbow_input = joystick.get_axis(5) if joystick.get_axis(5) >= 0.25 else 0  # Right bumper
    elbow_input2 = joystick.get_axis(4) if joystick.get_axis(4) >= 0.25 else 0  # Left Bumper
    wrist_input = joystick.get_axis(2) if abs(joystick.get_axis(2)) >= 0.25 else 0  # Right stick horizontal

    # Buttons
    a_pressed = joystick.get_button(0)  # A
    b_pressed = joystick.get_button(1)  # B
    start_pressed = joystick.get_button(7)  # Start
    #print(base_input," " , shoulder_input, " ", elbow_input, " ", wrist_input)
    # Adjust angles
    xyz[0] += int(base_input * delta)
    xyz[1] += int(-shoulder_input * delta)
    xyz[2] += int((elbow_input-elbow_input2) * delta * 2)

   
    # Gripper control
    RC.goToPos([xyz[0], xyz[1], xyz[2]], False)
    print(xyz)
    if a_pressed:
        RC.closeClaw()
    elif b_pressed:
        RC.openClaw()
    # Send update to Arduino
    #print("Arduino:", response)

    time.sleep(0.02)
     



RC.release()
RC.close()
pygame.quit()
