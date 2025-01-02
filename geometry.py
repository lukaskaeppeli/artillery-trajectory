class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, factor: float) -> "Vector":
        return Vector(self.x * factor, self.y * factor, self.z * factor)
    
    def __truediv__(self, divisor: float) -> "Vector":
        return Vector(self.x / divisor, self.y / divisor, self.z / divisor)
    
    def dot(self, other: "Vector") -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"

class Point(Vector):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)

class Velocity(Vector):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)

class Acceleration(Vector):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)