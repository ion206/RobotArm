import numpy as np
import matplotlib.pyplot as plt
import configparser

parser = configparser.ConfigParser()
parser.read("src/config.cfg")

vmax = int(parser['Motion'].getint('vmax'))
amax = int(parser['Motion'].getint('amax'))
dt = float(parser['Motion'].get('dt'))


def trapezoidal_profile(x0, xf):
    d = xf - x0
    direction = np.sign(d)
    d = abs(d)

    t_a = v_max / a_max
    d_a = 0.5 * a_max * t_a ** 2

    if 2 * d_a >= d:
        # Triangular profile
        v_peak = np.sqrt(d * a_max)
        t_a = v_peak / a_max
        t_total = 2 * t_a
        t_c = 0
    else:
        # Trapezoidal profile
        v_peak = v_max
        d_c = d - 2 * d_a
        t_c = d_c / v_max
        t_total = 2 * t_a + t_c

    time = np.arange(0, t_total + dt, dt)
    pos = []
    vel = []

    for t in time:
        if t < t_a:
            # Acceleration phase
            v = a_max * t
            p = 0.5 * a_max * t**2
        elif t < t_a + t_c:
            # Constant velocity
            v = v_peak
            p = d_a + v_peak * (t - t_a)
        else:
            # Deceleration phase
            t_d = t - (t_a + t_c)
            v = v_peak - a_max * t_d
            p = d_a + v_peak * t_c + v_peak * t_d - 0.5 * a_max * t_d**2

        pos.append(x0 + direction * p)
        vel.append(direction * v)

    return time, pos, vel


def trapXYZ(start, end):
    start = np.array(start)
    end = np.array(end)
    delta = end - start
    distance = np.linalg.norm(delta)
    direction = delta / distance

    time, scalar_pos, _ = trapezoidal_profile(0, distance)

    positions = [start + direction * s for s in scalar_pos]
    return positions

