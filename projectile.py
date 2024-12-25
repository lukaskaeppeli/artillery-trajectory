import numpy as np
from environment import Environment

class Projectile:
    def __init__(self, radius: float, mass: float, direction: float):
        self.radius = radius
        self.mass = mass
        self.lateral_cross_sectional_area = np.pi * radius**2
        self.axial_cross_sectional_area = 0.125 # TODO: Just an estimate
        self.direction = direction

    def update_velocity(self, point: np.array, velocity: np.array, environment: Environment, delta_t: float):
        """
        Calculates the resulting velocity vector based on air resistance and wind

        Parameters:
        point (np.array): Current position of the projectile
        velocity (np.array): Current velocity of the projectile
        environment (Environment): The environment
        delta_t (float): Number of seconds to iterate

        Returns:
        np.array: The resulting velocity vector
        """

        air_density = environment.get_air_density(point)
        wind_direction, wind_velocity = environment.get_wind(point)

        angle_relative = (wind_direction - self.direction) * (2 * np.pi / 6400)
        wind_relative = np.array([wind_velocity * np.cos(angle_relative), 0, wind_velocity * np.sin(angle_relative)])

        velocity_absolute = velocity - wind_relative

        speed = np.linalg.norm(np.array(velocity_absolute[0], velocity_absolute[1])) # Ignore z axis for now
        
        # If the speed is zero, the object isn't moving, and there's no drag force
        if speed == 0:
            return velocity
        
        # Lateral part        
        lateral_drag_coefficient = self.derive_lateral_cw(speed, environment, point)
        lateral_acceleration_magnitude = self.derive_drag_force_magnitude(air_density, speed, lateral_drag_coefficient, self.lateral_cross_sectional_area) / self.mass
        lateral_drag_direction = -velocity / speed  # Negative sign to indicate the opposite direction

        # Axial part
        axial_drag_coefficient = 1.2
        axial_acceleration_magnitude = self.derive_drag_force_magnitude(air_density, velocity_absolute[2], axial_drag_coefficient, self.axial_cross_sectional_area) / self.mass
        axial_drag_direction = np.array([0, 0, 1]) if velocity_absolute[2] < 0 else np.array([0, 0, -1])
        
        acceleration = (lateral_acceleration_magnitude * lateral_drag_direction) + (axial_acceleration_magnitude * axial_drag_direction)

        # Update the velocity using: v_new = v_old + a * delta_t
        new_velocity = velocity + acceleration * delta_t

        return new_velocity

    def derive_lateral_cw(self, speed: float, environment: Environment, point: np.array):
        """
        Derives the drag coefficient cw as described in Regl. 55.210 1.3.1

        Parameters:
        velocity (np.array): Current velocity of the projectile
        environment (Environment): Meteorogical environment
        point (np.array): The point at which the cw should be derived for

        Returns:
        float: the drag coefficient cw
        """
        speed_of_sound = environment.get_speed_of_sound(point)
        mach = speed / speed_of_sound
        if mach < 0.8:
            return 0.14
        elif mach > 1.2:
            return -0.15 * mach + 0.57
        return -0.36 + mach * 0.625
    
    def derive_drag_force_magnitude(self, air_density: float, speed: float, drag_coefficient: float, area: float):
        """
        Calculates the drag force magnitude

        Parameters:
        air_density (float): The air density at the point, where the projectile is currently
        speed (float): Current projectile speed
        drag_coefficient (float): The drag coefficient of the projectile
        area (float): The area that results in the drag force

        Returns:
        float: The resulting drag force magnitude
        """
        return 0.5 * air_density * speed**2 * drag_coefficient * area
