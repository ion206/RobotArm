import numpy as np
import matplotlib.pyplot as plt
import configparser

parser = configparser.ConfigParser()
parser.read("src/config.cfg")

vmax = int(parser['Motion'].getint('vmax'))
amax = int(parser['Motion'].getint('amax'))
dt = float(parser['Motion'].get('dt'))


def trapezoidal_profile(x0, xf):
    """Generate a trapezoidal motion profile between two points"""
    d = xf - x0
    direction = np.sign(d)
    d = abs(d)

    # Calculate acceleration time and distance
    t_a = vmax / amax  
    d_a = 0.5 * amax * t_a ** 2

    if 2 * d_a >= d:
        # Use triangular profile for short distances
        v_peak = np.sqrt(d * amax)
        t_a = v_peak / amax
        t_total = 2 * t_a
        t_c = 0
    else:
        # Use trapezoidal profile for longer distances
        v_peak = vmax
        d_c = d - 2 * d_a
        t_c = d_c / vmax
        t_total = 2 * t_a + t_c

    # Generate time points
    time = np.arange(0, t_total + dt, dt)
    pos = np.zeros(len(time))
    vel = np.zeros(len(time))

    # Calculate position and velocity at each time point
    for i, t in enumerate(time):
        if t < t_a:
            # Acceleration phase
            vel[i] = amax * t
            pos[i] = 0.5 * amax * t**2
        elif t < t_a + t_c:
            # Constant velocity phase
            vel[i] = v_peak
            pos[i] = d_a + v_peak * (t - t_a)
        else:
            # Deceleration phase
            t_d = t - (t_a + t_c)
            vel[i] = v_peak - amax * t_d
            pos[i] = d_a + v_peak * t_c + v_peak * t_d - 0.5 * amax * t_d**2

    # Apply direction and offset
    pos = x0 + direction * pos
    vel = direction * vel

    return time, pos, vel


def trapXYZ(start, end):
    """Generate synchronized 3D trapezoidal motion profile"""
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    delta = end - start
    
    # Return if no movement needed
    if np.allclose(delta, 0):
        return [start]

    # Find the axis that requires the longest time
    times = []
    profiles = []
    for i in range(3):
        t, p, _ = trapezoidal_profile(start[i], end[i])
        times.append(len(t))
        profiles.append(p)
    
    # Synchronize all axes to the longest profile
    max_length = max(times)
    synchronized_positions = []
    
    for t in range(max_length):
        # Interpolate position for each axis
        pos = np.zeros(3)
        for i in range(3):
            # Scale the profile index to match the longest profile
            idx = int(t * (times[i] - 1) / (max_length - 1))
            pos[i] = profiles[i][idx]
        synchronized_positions.append(pos)

    return synchronized_positions
