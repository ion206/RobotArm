import math

def getAngs(x, y, z, l1, l2):
    print("XYZ: " + str(x) + ", " + str(y) + ", " +  str(z))
    xbias = 250.1
    ybias = 0.1

    """
    Computes inverse kinematics for a 3-DOF robotic arm.s
    
    :param x: Target x position
    :param y: Target y position
    :param z: Target z position
    :param l1: Length of the upper arm
    :param l2: Length of the lower arm
    :return: (base_angle, shoulder_angle, elbow_angle)
    """
    angle = (math.atan((abs(y-ybias)/abs(x-xbias))))
    if(x < 200):
        base_angle = multiple(math.degrees(angle), 1)
    else:
        base_angle = 180 - multiple(math.degrees(abs(angle)), 1)
    
    r = math.sqrt(math.pow(x,2)+ math.pow(y,2))
    d = math.sqrt(math.pow(r,2) + math.pow(z,2))
    print("r: " + str(r))
    
    theta2 = 3.14/2 ##math.acos((d**2 - l1**2 - l2**2)/(2*l1*l2)) #Law of Cosines
    theta1 = 3.14/2 #math.asin((l2*math.sin(theta2))/d) # Law of Sines
    theta1 = theta1 + math.asin(z/d)
    print(base_angle)
    return[int(math.degrees(theta1)), int(math.degrees(theta2)),0, (base_angle),0]


def multiple(val, nearest):
        return round(val / nearest) * nearest