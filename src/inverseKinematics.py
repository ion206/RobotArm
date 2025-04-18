import math

def getAngs(x, y, z, l1, l2):
    print("XYZ: " + str(x) + ", " + str(y) + ", " +  str(z))
    xbias = 210.1
    ybias = -20

    """
    Computes inverse kinematics for a 3-DOF robotic arm.s
    
    :param x: Target x position
    :param y: Target y position
    :param z: Target z position
    :param l1: Length of the upper arm
    :param l2: Length of the lower arm
    :return: (base_angle, shoulder_angle, elbow_angle)
    """
    base_angle = baseAngle(x,y, xbias, ybias)
    
    r = math.sqrt((x - xbias)**2 + (y - ybias)**2)
    d = math.sqrt(r**2 + z**2)
    print("r: " + str(r))
    print("d: " + str(d))
    
    cos_theta2 = ((r**2 + z**2 - l2**2 - l1**2) / (2 * l1 * l2))
    if abs(cos_theta2) > 1:
        print("Target position is out of reach")
        return [160,30,90,60,0]
    theta2 = math.acos(cos_theta2)
    theta1 = math.asin((l1 * math.sin(theta2)) / d) + math.asin(z / d)
    theta2 = 3.14 - theta2
    print("Computed Angles: " + "\nShoulder: " + str(math.degrees(theta1)-40) + "\nArm: " + str(math.degrees(theta2)+25) + "\nBase: " + str(base_angle))
    return[int(math.degrees(theta1)+40), int(math.degrees(theta2)-25),0, (base_angle),0]

def baseAngle(x,y, zBias, xbias = 210.1, ybias = -20):
    angle = (math.atan((abs(y-ybias)/abs(x-xbias))))
    if(x < 200):
        base_angle = multiple(math.degrees(angle), 1)
    else:
        base_angle = 180 - multiple(math.degrees(abs(angle)), 1)
    
    return base_angle + zBias


def multiple(val, nearest):
        return round(val / nearest) * nearest