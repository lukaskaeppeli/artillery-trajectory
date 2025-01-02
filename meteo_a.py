class MeteoA:
    def __init__(self, data):
        self.measurements = self.parse_measurements(data)

    def parse_measurements(self, data):
        if len(data) == 0:
            self.error = "No data provided"
            return
        
        rows = []
        if data[0][0] == "HOEHE":
            rows = data[1:]
        else:
            rows = data
        
        rows[0] = [0 if cell == "//" else cell for cell in rows[0]]
        try:
            rows = [[float(cell) for cell in row] for row in rows]
        except:
            self.error = "Parsing error. Some data in meteo a cannot be parsed as float"
            return
        
        measurements = []
        for row in rows:
            if self.is_row_valid(row):
                measurements.append(Measurement(row[0], row[1], row[2], row[3]))
            else:
                self.error = "Checksum verification failed at height: " + row[0]

        return sorted(measurements, key=lambda item: item.height)

    def is_row_valid(self, row):
        numbers_to_process = row[:-1]
        digit_sum = 0

        for cell in numbers_to_process:
            if isinstance(cell, (int, float)) or cell.replace('.', '', 1).replace('-', '', 1).isdigit():
                # Convert the cell to a string, iterate over each character, and sum up its digits
                for digit in str(cell).replace('.', '').replace('-', ''):
                    digit_sum += int(digit)

        return digit_sum == int(row[-1])

class Measurement:

    def __init__(self, height: float, temperature: float, wind_direction: float, wind_velocity: MeteoA):
        self.height = height
        self.temperature = temperature
        self.wind_direction = wind_direction
        self.wind_velocity = wind_velocity
