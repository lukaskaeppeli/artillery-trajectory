import numpy as np

from meteo_a import MeteoA

class Environment:
    def __init__(self, temp0: float, pressure0: float, height0: float, meteo_a: MeteoA):
        self.temp0 = temp0
        self.pressure0 = pressure0
        self.height0 = height0
        self.meteo_a = meteo_a

    def get_air_density(self, point: np.array):
        pressure = self.derive_pressure(point)
        temperature = self.derive_temperature(point)
        return (100 * pressure) / (287.05 * temperature)

    def derive_temperature(self, point: np.array):
        """
        Derives the temperature at the specified point in either the standard athmosphere (when no meteo_a given)
        or by performing linear interpolation between the two nearest measurements contained in the meteo_a.

        Parameters:
        point (np.array): The point at whose height the temerature should be calculated

        Returns:
        float: The temperature in K
        """
        height = point[1]

        if self.is_meteo_a_given():
            return self.get_linear_interpolation_at(height)[1] + 273.15
        else:
            if height > 11000:
                return 216.65
            return (273.15 + self.temp0) - 0.0065 * (height - self.height0)

    def derive_pressure(self, point: np.array):
        """
        Derives the air pressure at a given point.
        # TODO: Only valid up until 11'000
        # TODO: Given meteo_a: Take temperature at point into account
        # TODO: Given no meteo_a: Take pressure0 into account

        Parameters:
        point (np.array): The point at whose height the pressure should be calculated

        Returns:
        float: The pressure in hPa
        """
        if self.is_meteo_a_given():
            return self.pressure0 * pow(1 - (0.0065 * (point[1] - self.height0) / 288.15), 5.255)
        else:
            return 1013.25 * pow(1 - (0.0065 * point[1] / 288.15), 5.255)
        
    def get_wind(self, point: np.array):
        """
        Derives the wind direction and velocity at a given point.

        Parameters:
        point (np.arry): The point at whose height the wind should be calculated

        Returns:
        float: The direction of the wind in Azimute
        velocity: The velocity of the wind in m/s
        """
        if self.is_meteo_a_given():
            [_, _, direction, velocity, _] = self.get_linear_interpolation_at(point[1])
            return direction * 100, velocity
        else:
            return 0, 0

    def get_speed_of_sound(self, point: np.array):
        return 331 + 0.6 * (self.derive_temperature(point) - 273.15)
    
    def is_meteo_a_given(self):
        return self.meteo_a != None and self.meteo_a.data != None and self.meteo_a.valid
    
    def get_linear_interpolation_at(self, height: float):
        """
        Interpolates the fields of a set of vectors for a given target height.

        Parameters:
        height (float): The height at which to interpolate the fields.

        Returns:
        np.array: Interpolated values for the fields at the given height.

        Raises:
        ValueError: If the height is outside the range of the given heights.
        """
        # Sort the vectors by height (first entry)
        vectors = np.array(self.meteo_a.data)
        vectors = vectors[vectors[:, 0].argsort()]

        heights = vectors[:, 0]
        fields = vectors[:, 1:]

        lower_idx = 0
        upper_idx = 0
        if height < heights[0]:
            lower_idx = 0
            upper_idx = 1
        if height > heights[-1]:
            lower_idx = len(vectors) - 2
            lower_idx = len(vectors) - 1
        else:
            lower_idx = np.searchsorted(heights, height) - 1
            upper_idx = lower_idx + 1

        h1, h2 = heights[lower_idx], heights[upper_idx]
        f1, f2 = fields[lower_idx], fields[upper_idx]

        # Linear interpolation for each field
        interpolated_fields = f1 + (f2 - f1) * ((height - h1) / (h2 - h1))

        return [height] + interpolated_fields.tolist()
