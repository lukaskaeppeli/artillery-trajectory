import numpy as np
from environment import Environment
from projectile import Projectile

class Simulator:

    def __init__(self, environment: Environment, projectile: Projectile):
        self.environment = environment
        self.projectile = projectile
        self.g = 9.80665

    def iterate(self, point: np.array, velocity: np.array, delta_t: float):
        velocity = self.projectile.update_velocity(point, velocity, self.environment, delta_t)
        # Apply gravity
        velocity = np.subtract(velocity, np.array([0, self.g * delta_t, 0]))
        # Update position
        point = np.add(point, velocity * delta_t)
        
        return point, velocity


    def calculate(self, v0, phi0, delta_t):
        points = []
        vectors = []
        point_i = np.array([0, self.environment.height0,0])
        vector_i = np.array([v0 * np.cos((np.pi / 180) * phi0), v0 * np.sin((np.pi / 180) * phi0), 0])

        while point_i[0] >= 0:
            point_i, vector_i = self.iterate(point_i, vector_i, delta_t)
            points.append(point_i)
            vectors.append(vector_i)

            if (point_i[1] < 0):
                break

        return points
