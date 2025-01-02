from geometry import Point
from math import e
from meteo_a import Measurement, MeteoA

class Environment:
    def __init__(self, temp0: float, pressure0: float, height0: float, meteo_a: MeteoA):
        self.temp0 = temp0
        self.pressure0 = pressure0
        self.height0 = height0
        self.meteo_a = meteo_a
        self.air_molar_mass = 0.02896968 # kg/mol
        self.gas_constant = 8.314462618 # J / (mol * K)
        self.gravity = 9.80665 # m / s^2

    def get_air_density(self, point: Point):
        pressure = self.derive_pressure(point)
        temperature = self.derive_temperature(point)
        return (100 * pressure) / (287.05 * temperature)

    def derive_temperature(self, point: Point):
        """
        Derives the temperature at the specified point in either the standard athmosphere (when no meteo_a given)
        or by performing linear interpolation between the two nearest measurements contained in the meteo_a.

        Parameters:
        point (Point): The point at whose height the temerature should be calculated

        Returns:
        float: The temperature in K
        """
        if self.is_meteo_a_given():
            return self.get_linear_interpolation_at(point.y).temperature + 273.15
        else:
            if point.y > 11000:
                return 216.65
            return (273.15 + self.temp0) - 0.0065 * (point.y - self.height0)

    def derive_pressure(self, point: Point):
        """
        Derives the air pressure at a given point.

        Parameters:
        point (Point): The point at whose height the pressure should be calculated

        Returns:
        float: The pressure in hPa
        """
        height_difference = point.y - self.height0

        if self.is_meteo_a_given():
            temperature = self.get_linear_interpolation_at(point.y).temperature
        else:
            temperature = self.temp0 - 0.0065 * height_difference

        return self.pressure0 * pow(e, - (self.gravity * self.air_molar_mass * height_difference / (self.gas_constant * (temperature + 273.15))))

        
    def get_wind(self, point: Point):
        """
        Derives the wind direction and velocity at a given point.

        Parameters:
        point (Point): The point at whose height the wind should be calculated

        Returns:
        float: The direction of the wind in Azimute
        velocity: The velocity of the wind in m/s
        """
        if self.is_meteo_a_given():
            measurement = self.get_linear_interpolation_at(point.y)
            return measurement.wind_direction * 100, measurement.wind_velocity
        else:
            return 0, 0

    def get_speed_of_sound(self, point: Point):
        return 331 + 0.6 * (self.derive_temperature(point) - 273.15)
    
    def is_meteo_a_given(self):
        return self.meteo_a != None and self.meteo_a.measurements != None
    
    def get_linear_interpolation_at(self, height: float):
        """
        Interpolates the fields of a set of vectors for a given target height.

        Parameters:
        height (float): The height at which to interpolate the fields.

        Returns:
        Measurement: Interpolated values for the fields at the given height.

        Raises:
        ValueError: If the height is outside the range of the given heights.
        """

        lower_idx = 0
        upper_idx = 0

        # Determine lower and upper indices
        if height < self.meteo_a.measurements[0].height:
            lower_idx = 0
            upper_idx = 1
        elif height > self.meteo_a.measurements[-1].height:
            lower_idx = len(self.meteo_a.measurements) - 2
            upper_idx = len(self.meteo_a.measurements) - 1
        else:
            for i in range(len(self.meteo_a.measurements) - 1):
                if self.meteo_a.measurements[i].height <= height < self.meteo_a.measurements[i + 1].height:
                    lower_idx = i
                    upper_idx = i + 1
                    break

        # Get the two closest objects
        lower_obj = self.meteo_a.measurements[lower_idx]
        upper_obj = self.meteo_a.measurements[upper_idx]

        # Heights for interpolation
        h1, h2 = lower_obj.height, upper_obj.height

        # Fields for interpolation
        interpolated_temperature = lower_obj.temperature + (
            (upper_obj.temperature - lower_obj.temperature) * (height - h1) / (h2 - h1)
        )
        interpolated_wind_direction = lower_obj.wind_direction + (
            (upper_obj.wind_direction - lower_obj.wind_direction) * (height - h1) / (h2 - h1)
        )
        interpolated_wind_velocity = lower_obj.wind_velocity + (
            (upper_obj.wind_velocity - lower_obj.wind_velocity) * (height - h1) / (h2 - h1)
        )

        # Return interpolated results
        return Measurement(height, interpolated_temperature, interpolated_wind_direction, interpolated_wind_velocity)