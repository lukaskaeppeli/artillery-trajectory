import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Initial speed and launch angle (from the horizontal).
v0 = 816
phi0 = np.radians(45)

# Temperature on ground
temp0 = 20

height0 = 800
height = height0

pressure0 = 926

def derive_cw(v):
    m = v / 343
    if m < .8:
        return .14
    if m > 1.2:
        return -.15 * m + .57
    return -.36 + m * 0.625

def derive_rho_air():
    global height
    temperature = 20 - 0.65 * (height / 100)
    temperature = temperature + 273.15
    r_s = 287.058
    pressure = pressure0 - (height / 8)
    pressure = pressure * 100000
    rho = pressure / (r_s * temperature)
    print(str(height) + " - " + str(rho))
    return rho / 1000

def update_height(delta):
    global height
    height += delta
    return height

# Drag coefficient, projectile radius (m), area (m2) and mass (kg).
r = 0.077
A = np.pi * r**2
m = 42
# Air density (kg.m-3), acceleration due to gravity (m.s-2).
rho_air = 1.2
g = 9.81

def deriv(t, u):
    x, xdot, z, zdot = u
    speed = np.hypot(xdot, zdot)
    xdotdot = -(0.5 * derive_cw(speed) * rho_air * A)/m * speed * xdot
    zdotdot = -(0.5 * derive_cw(speed) * rho_air * A)/m * speed * zdot - g
    print()
    print(xdot)
    print(xdotdot)
    print(zdot)
    print(zdotdot)
    print(speed)
    print(update_height(zdot))
    return xdot, xdotdot, zdot, zdotdot

# Initial conditions: x0, v0_x, z0, v0_z.
u0 = 0, v0 * np.cos(phi0), 0., v0 * np.sin(phi0)
# Integrate up to tf unless we hit the target sooner.
t0, tf = 0, 300

def hit_target(t, u):
    # We've hit the target if the z-coordinate is 0.
    return u[2]
# Stop the integration when we hit the target.
hit_target.terminal = True
# We must be moving downwards (don't stop before we begin moving upwards!)
hit_target.direction = -1

def max_height(t, u):
    # The maximum height is obtained when the z-velocity is zero.
    return u[3]

soln = solve_ivp(deriv, (t0, tf), u0, method="RK23", dense_output=True,
                 events=(hit_target, max_height))
print(soln)
print('Time to target = {:.2f} s'.format(soln.t_events[0][0]))
print('Time to highest point = {:.2f} s'.format(soln.t_events[1][0]))

# A fine grid of time points from 0 until impact time.
t = np.linspace(0, soln.t_events[0][0], 100)

# Retrieve the solution for the time grid and plot the trajectory.
sol = soln.sol(t)
x, z = sol[0], sol[2]
print('Range to target, xmax = {:.2f} m'.format(x[-1]))
print('Maximum height, zmax = {:.2f} m'.format(max(z)))
plt.plot(x, z)
plt.xlabel('x /m')
plt.ylabel('z /m')
plt.show()
plt.savefig("test.svg")