import pygame
import time
from robotControl import robotController as RC
from robotControl import getAngles as IK

# Initialize controller
pygame.init()
pygame.joystick.init()
RC.init()

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


try:
    running = True
    while running:
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

        angles = IK.getAngs([xyz[0] / 1000, xyz[1] / 1000, xyz[2] / 1000])
        print(xyz)
        if a_pressed:
            angles[4] = 0
        elif b_pressed:
            angles[4] = 90
        # Send update to Arduino
        response = RC.updateArm(angles.copy())
        #print("Arduino:", response)

        # Exit safely
        if start_pressed:
            running = False

        time.sleep(0.02)

except KeyboardInterrupt:
    print("Interrupted.")

finally:
    RC.release()
    RC.close()
    pygame.quit()
