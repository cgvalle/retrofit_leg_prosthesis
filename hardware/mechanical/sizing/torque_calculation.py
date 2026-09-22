"""Motor-torque sizing for the ball-screw knee actuator.

Python port of torque_calculation.nb (Mathematica). Reproduces Table 1 of the
paper: the motor-shaft torque needed for the ball screw to deliver the peak
level-walking knee extension moment at a given knee flexion angle.

Geometry (knee centre K at the origin, mm):
    A = (-a2, a1)                       thigh attachment of the screw
    B = (-k2 cos a - k1 sin a,          shank attachment of the screw,
          k2 sin a - k1 cos a)          rotated by the flexion angle a
    screw length  = |AB|
    moment arm    = |KA x KB| / |AB|
    screw force   F = M / r
    motor torque  T = F L / (2 pi eta)

Run:  python torque_calculation.py
"""
import numpy as np

# Linkage dimensions (mm), measured on the prototype
A1 = 90.0    # thigh attachment, vertical offset from knee centre
A2 = 50.0    # thigh attachment, horizontal offset
K1 = 295.0   # shank attachment, vertical offset (280 + 15)
K2 = 50.0    # shank attachment, horizontal offset

# Load case
MOMENT_PER_KG = 0.49   # Nm/kg, peak knee extension moment, level walking
MASS = 90.36           # kg, worst case supported mass (user + prosthesis)

# Ball screw SFU1610
LEAD = 0.010           # m/rev
ETA_SCREW = 0.90

# Installed motor (5840-31ZY, 31:1 worm gear, 200 rpm variant)
MOTOR_NOMINAL_TORQUE = 0.49  # Nm


def linkage(alpha_deg):
    """Return (screw length [mm], moment arm [m]) at knee flexion alpha."""
    a = np.radians(alpha_deg)
    A = np.array([-A2, A1])
    B = np.array([-K2 * np.cos(a) - K1 * np.sin(a),
                  K2 * np.sin(a) - K1 * np.cos(a)])
    AB = B - A
    cross = abs(A[0] * B[1] - A[1] * B[0])
    length = np.linalg.norm(AB)
    return length, cross / length / 1000.0


def required_motor_torque(alpha_deg, moment=MOMENT_PER_KG * MASS):
    _, r = linkage(alpha_deg)
    force = moment / r
    return force * LEAD / (2 * np.pi * ETA_SCREW)


if __name__ == '__main__':
    moment = MOMENT_PER_KG * MASS
    print(f'Target knee moment: {moment:.2f} Nm')
    print(f'{"angle (deg)":>12} {"screw (mm)":>11} {"arm (mm)":>9} {"force (N)":>10} {"motor (Nm)":>11} {"x nominal":>10}')
    for alpha in [1, 5, 37.4, 64.1]:
        length, r = linkage(alpha)
        t = required_motor_torque(alpha)
        print(f'{alpha:>12} {length:>11.0f} {r * 1000:>9.1f} {moment / r:>10.0f} {t:>11.2f} '
              f'{t / MOTOR_NOMINAL_TORQUE:>10.1f}')
