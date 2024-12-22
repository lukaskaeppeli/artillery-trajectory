class MeteoA:
    def __init__(self, data):
        self.data = data
        self.remove_title_row()
        self.replace_double_slash_with_zero()
        self.parse_entries()
        self.validate()

    def remove_title_row(self):
        self.data = self.data[1:] if len(self.data) > 0 else self.data

    # Function to replace all occurrences of '//' with 0
    def replace_double_slash_with_zero(self):
        self.data = [[0 if cell == "//" else cell for cell in row] for row in self.data]

    def parse_entries(self):
        self.data = [[float(cell) for cell in row] for row in self.data]

    def validate(self):
        self.valid = True
        for row in self.data:
            numbers_to_process = row[:-1]
            digit_sum = 0

            for cell in numbers_to_process:
                if isinstance(cell, (int, float)) or cell.replace('.', '', 1).replace('-', '', 1).isdigit():
                    # Convert the cell to a string, iterate over each character, and sum up its digits
                    for digit in str(cell).replace('.', '').replace('-', ''):
                        digit_sum += int(digit)
            if digit_sum != int(row[-1]):
                self.valid = False