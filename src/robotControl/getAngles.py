import ikpy.chain
import ikpy.utils.plot as plot_utils

import numpy as np
import time
import math 

import matplotlib.pyplot as plt

checkPlot = False

chain = ikpy.chain.Chain.from_urdf_file(
    "src/robotControl/robotArm.urdf",base_elements=["base_stand"], 
    active_links_mask=[False, True, True, True, True, False],
    last_link_vector = [0, 0, -0.11]  # adjust based on claw length
    )

# Global figure and axis
fig, ax = None, None

def init_plot(): #Initialize Matplotlib Visualization
    global fig, ax
    if fig is None or ax is None:
        fig, ax = plot_utils.init_3d_figure()
        fig.set_figheight(9)
        fig.set_figwidth(13)
        plt.ion()
        plt.show()

def getAngs(target_position):
    flipBase = False #When x becomes negative IKPy was having errors, so flipBase fixes it
    if (target_position[0] <= 0):
        target_position[0] *= -1
        flipBase = True

    
    ik = chain.inverse_kinematics(target_position, target_orientation = [0, 0, 1], orientation_mode="Z")
    angs = list(map(lambda r:math.degrees(r),ik.tolist()))
    #print("Angles: ", angs )
    if(checkPlot):
        forwardKinematics(target_position, ik)
    if(flipBase):
        angs[1] = abs(180-angs[1])
    return [135-int(angs[2]), 180-int(angs[3]), 180+int(angs[4]), int(angs[1]), 90]

def forwardKinematics(target_position, ik):
    #Allows for double checking of Arm Values and matplot visualization
    global ax
    computed_position = chain.forward_kinematics(ik)
    #print("Computed position: %s, original position : %s" % (computed_position[:3, 3], target_position))
    #print("Joint angles (deg):", [round(math.degrees(a), 2) for a in ik])
    ax.clear()  # Clear previous frame
    chain.plot(ik, ax, target=target_position)
    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(-0.5, 0.5)
    ax.set_zlim(0, 0.6)
    plt.draw()
    plt.pause(0.001)  # Allow GUI event loop to update







    