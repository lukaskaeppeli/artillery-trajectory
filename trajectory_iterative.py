import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

#################
# Initial State #
#################

# Speed
v0 = 816

# launch angle (from the horizontal).
phi0 = np.radians(45)

# Temperature and pressure on ground
temp0 = 20
pressure0 = 926

height0 = 800

# Drag coefficient, projectile radius (m), area (m2) and mass (kg).
r = 0.077 #(1/2 caliber size)
A = np.pi * r**2
m = 42

# Air density (kg.m-3)
rho_air = 1.2

# Gravity
g = 9.81

def get_initial_point():
    return np.array([0,0,0])

def get_initial_vector():
    return np.array([v0 * np.cos(phi0), v0 * np.sin(phi0), 0])

def get_air_density(point: np.array):
    pression = derive_pression(point)
    temperature = get_temp(point)
    return pression / (287.05 * temperature)

def get_temp(point: np.array):
    if (point[1]) > 11000:
        return 216.65 #(-56.5 °C)
    return 273.15 + temp0 - point[1] / 1000 * 6.5 # (-6.5 K pro 1000m)

def get_speed_of_sound(point: np.array):
    return 331 + 0.6 * get_temp(point)

def derive_cw(point: np.array, vector: np.array):
    v = np.linalg.norm(vector)
    c = get_speed_of_sound(point)
    m = v / c
    if m < .8:
        return .14
    if m > 1.2:
        return -.15 * m + .57
    return -.36 + m * 0.625

# TODO: Only valid up until 11'000
def derive_pression(point: np.array):
    return 1013.25 * pow(1- (0.0065 * point[1] / 288.15), 5.255)

def iterate(point: np.array, vector: np.array):
    # Gravitation
    vector = np.subtract(vector, np.array([0, g, 0]))

    # Air density

    # cw
    
    point_new = np.add(point, vector)
    return point_new, vector


points = []
vectors = []

def calculate():
    point_i = get_initial_point()
    vector_i = get_initial_vector()

    for i in range(120):
        point_i, vector_i = iterate(point_i, vector_i)
        points.append(point_i)
        vectors.append(vector_i)




calculate()

x = [item[0] for item in points]
y = [item[1] for item in points]
z = [item[2] for item in points]

print(x)
print(y)
print(z)



#for i in range(0, 15000, 1000):
#    print(get_temp(np.array([0, i, 0])))
#    print(get_air_density(np.array([0, i, 0])))
#    print(derive_rho_air(np.array([0, i, 0])))
#    print(derive_pression(np.array([0,i,0])))

plt.plot(x, y)
plt.xlabel('x /m')
plt.ylabel('z /m')
plt.show()
plt.savefig("test.svg")