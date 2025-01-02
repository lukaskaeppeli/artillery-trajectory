from geometry import Point, Velocity, Acceleration
from environment import Environment
from projectile import Projectile
from math import sin, cos, pi

class Simulator:

    def __init__(self, environment: Environment, projectile: Projectile):
        self.environment = environment
        self.projectile = projectile
        self.g = Acceleration(0, 9.80665, 0)

    def iterate(self, point: Point, velocity: Velocity, delta_t: float):
        velocity = self.projectile.update_velocity(point, velocity, self.environment, delta_t)
        # Apply gravity
        velocity -= self.g * delta_t
        # Update position
        point += velocity * delta_t
        
        return point, velocity


    def calculate(self, v0, phi0, delta_t):
        points = []
        vectors = []
        point_i = Point(0, self.environment.height0, 0)
        vector_i = Velocity(v0 * cos(phi0 * pi / 180), v0 * sin(phi0 * pi / 180), 0)

        while point_i.x >= 0:
            point_i, vector_i = self.iterate(point_i, vector_i, delta_t)
            points.append(point_i)
            vectors.append(vector_i)

            if (point_i.y < 0):
                break

        return points
