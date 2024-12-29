import csv
import tkinter as tk
from tkinter import filedialog
from environment import Environment
from meteo_a import MeteoA
from projectile import Projectile
from simulator import Simulator
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import sys
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        ico = Image.open(self.resource('schneeflocke.ico'))
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, photo)

        self.title("Meteo A - Auswertung")
        self.geometry("1000x500")
        self.configure(bg="#2e2e2e")

        # Initialize widgets
        self.create_widgets()

        # Initial validation
        self.validate_inputs()

    def resource(self, relative_path):
        base_path = getattr(
            sys,
            '_MEIPASS',
            os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def validate_inputs(self):
        """Validate input fields, update button states, and provide feedback."""
        # Initialize feedback messages
        calculate_feedback = ""

        # Validate calculate_button: Base data must meet specific conditions
        try:
            v0 = float(self.base_data_entry1.get())
            elevation = float(self.base_data_entry2.get())
            temp0 = float(self.base_data_entry3.get())  # Placeholder validation
            pressure0 = float(self.base_data_entry4.get())  # Placeholder validation
            height = float(self.base_data_entry5.get())
            valid_base_data = (
                v0 > 0 and
                0 <= elevation <= 90 and
                height > 0
            )
        except ValueError:
            valid_base_data = False
            calculate_feedback = "Base data fields must be valid numbers."

        # Specific feedback for each condition
        if valid_base_data:
            if v0 <= 0:
                calculate_feedback = "v0 must be greater than 0."
            elif not (0 <= elevation <= 90):
                calculate_feedback = "Elevation must be between 0 and 90 degrees."
            elif height <= 0:
                calculate_feedback = "Height must be greater than 0."

        self.calculate_button.config(state=tk.NORMAL if valid_base_data else tk.DISABLED)
        self.calculate_with_csv_button.config(state=tk.NORMAL if valid_base_data else tk.DISABLED)

        # Update feedback label
        if not valid_base_data:
            self.base_data_label.config(text=calculate_feedback, fg="red")
        else:
            self.base_data_label.config(text="", fg="green")

    def calculate_and_update_plot_with_standard(self):
        self.calculate_and_update_plot(None)

    def calculate_and_update_plot(self, meteo_a: MeteoA):
        """Generate and display the plot based on current datasets."""
       
        v0 = float(self.base_data_entry1.get())
        phi0 = float(self.base_data_entry2.get())
        temp0 = float(self.base_data_entry3.get())
        pressure0 = float(self.base_data_entry4.get())
        height0 = float(self.base_data_entry5.get())
        direction = float(self.trajectory_direction_entry.get())

        environment = Environment(temp0, pressure0, height0, meteo_a)
        projectile = Projectile(radius= 0.077, mass=42, direction=direction)
        simulator = Simulator(environment, projectile)
        points = simulator.calculate(v0, phi0, 0.1)

        # Extract data for plotting
        x_values = [item[0] for item in points]
        y_values = [item[1] for item in points]
        z_values = [item[2] for item in points]

        label = "v0={},phi0={},temp0={},pressure0={},direction={}".format(v0, phi0, temp0, pressure0, direction)

        x_y_figure = plt.figure("x_y")
        plt.plot(x_values, y_values, label=label)
        plt.title('X / Y ')
        plt.xlabel('x /m')
        plt.ylabel('y /m')
        plt.legend()
        x_y_figure.show()

        x_z_figure = plt.figure("x_z")
        plt.plot(x_values, z_values, label=label)
        plt.title('X / Z ')
        plt.xlabel('x /m')
        plt.ylabel('z /m')
        plt.legend()
        x_z_figure.show()

    def update_display(self):
        """Display all datasets in the editable format."""
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        for i, dataset in enumerate(self.datasets):
            for j, value in enumerate(dataset):
                entry = tk.Entry(self.display_frame, width=10, font=("Helvetica", 12))
                entry.insert(0, value)
                entry.grid(row=i, column=j, padx=5, pady=2)
                entry.config(bg="#333333", fg="white", insertbackground="white")
                entry.bind("<FocusOut>", lambda e, i=i, j=j: self.update_dataset(i, j, e))

    def update_dataset(self, row, col, event):
        """Update the dataset list with new values from the Entry fields."""
        try:
            new_value = float(event.widget.get())
            self.datasets[row][col] = new_value
            self.label.config(text="Dataset updated successfully!")
        except ValueError:
            self.label.config(text="Invalid input. Please enter a valid number.")

    def create_widgets(self):
        """Create and layout all widgets."""
        self.instructions = tk.Label(self, text="Geben Sie folgende Daten an", font=("Helvetica", 12), fg="#f5f5f5", bg="#2e2e2e")
        self.instructions.pack(pady=10)

        # Base data frame
        self.create_base_data_section()

        # Meteo A data frame
        self.create_meteo_section()

        # Frame to display datasets
        self.display_frame = tk.Frame(self, bg="#2e2e2e")
        self.display_frame.pack(pady=10)

        # Revalidate inputs on changes
        for entry in [self.base_data_entry1, self.base_data_entry2, self.base_data_entry3, self.base_data_entry4, self.base_data_entry5]:
            entry.bind("<KeyRelease>", lambda e: self.validate_inputs())

    def create_base_data_section(self):
        """Create the base data input section."""
        self.base_data_entry_frame = tk.Frame(self, bg="#2e2e2e")
        self.base_data_entry_frame.pack(pady=10)

        labels = ["Anfangsgeschwindigkeit [m/s]", "Elevation Geschütz [0°-90°]", "Temperatur am Boden [°C]",
                  "Luftdruck am Boden [hPa]", "Höhe [m]"]
        self.base_data_entries = []

        for i, label_text in enumerate(labels):
            tk.Label(self.base_data_entry_frame, text=label_text, font=("Helvetica", 10), fg="#f5f5f5", bg="#2e2e2e").grid(row=0, column=i, padx=5)
            entry = tk.Entry(self.base_data_entry_frame, width=20, font=("Helvetica", 12))
            entry.grid(row=1, column=i, padx=5)
            self.base_data_entries.append(entry)

        self.base_data_entry1, self.base_data_entry2, self.base_data_entry3, self.base_data_entry4, self.base_data_entry5 = self.base_data_entries
        self.base_data_entry1.insert(0, "816")
        self.base_data_entry2.insert(0, "45")
        self.base_data_entry3.insert(0, "21.5")
        self.base_data_entry4.insert(0, "944")
        self.base_data_entry5.insert(0, "691")

        self.calculate_button = tk.Button(self, text="Berechne via Standardathmosphäre", command=self.calculate_and_update_plot_with_standard,
                                          font=("Helvetica", 12), bg="#555555", fg="white",
                                          activebackground="#777777", activeforeground="white",
                                          padx=10, pady=5, borderwidth=0, state=tk.DISABLED)
        self.calculate_button.pack(pady=10)

        self.base_data_label = tk.Label(self, text="", font=("Helvetica", 12), fg="#f5f5f5", bg="#2e2e2e", wraplength=400)
        self.base_data_label.pack(pady=10)

    def create_meteo_section(self):
        """Create the Meteo A input section."""
        self.trajectory_direction_label = tk.Label(self, text="Schussrichtung [Azimut]", font=("Helvetica", 12), fg="#f5f5f5", bg="#2e2e2e", wraplength=400)
        self.trajectory_direction_label.pack(pady=10)
        self.trajectory_direction_entry = tk.Entry(width=20, font=("Helvetica", 12))
        self.trajectory_direction_entry.pack()
        self.trajectory_direction_entry.insert(0, "0")

        self.calculate_with_csv_button = tk.Button(self, text="Berechne mit Meteo A", command=self.select_and_read_csv,
                                          font=("Helvetica", 12), bg="#555555", fg="white",
                                          activebackground="#777777", activeforeground="white",
                                          padx=10, pady=5, borderwidth=0, state=tk.DISABLED)
        self.calculate_with_csv_button.pack(pady=10)

        self.meteo_a_entry_frame = tk.Frame(self, bg="#2e2e2e")
        self.meteo_a_entry_frame.pack(pady=10)

    def select_and_read_csv(self):
        # Open a file dialog to select the CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        
        if not file_path:
            return None
        
        # Read the CSV file and store it as an array of arrays
        data = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)

        meteo_a = MeteoA(data)
        return self.calculate_and_update_plot(meteo_a)


if __name__ == '__main__':
    app = App()
    app.mainloop()
