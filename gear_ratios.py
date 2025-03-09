import numpy as np
import matplotlib.pyplot as plt

# Function to calculate gear ratio
def calculate_gear_ratio(teeth_input, teeth_output):
    return teeth_output / teeth_input

# Function to calculate output torque based on input torque and gear ratio
def calculate_output_torque(input_torque, gear_ratio):
    return input_torque * gear_ratio

# Function to calculate output speed based on input speed and gear ratio
def calculate_output_speed(input_speed, gear_ratio):
    return input_speed / gear_ratio

# Function to plot the relationship between gear ratio and output torque
def plot_gear_system(input_torque, input_speed, max_gear_teeth):
    gear_ratios = np.linspace(1, 5, 10)  # Varying gear ratios from 1 to 5
    output_torques = [calculate_output_torque(input_torque, ratio) for ratio in gear_ratios]
    output_speeds = [calculate_output_speed(input_speed, ratio) for ratio in gear_ratios]
    
    plt.figure(figsize=(10, 6))

    # Plotting output torque
    plt.subplot(2, 1, 1)
    plt.plot(gear_ratios, output_torques, label='Output Torque', color='blue')
    plt.title('Output Torque vs Gear Ratio')
    plt.xlabel('Gear Ratio')
    plt.ylabel('Output Torque (Nm)')
    plt.grid(True)
    plt.legend()

    # Plotting output speed
    plt.subplot(2, 1, 2)
    plt.plot(gear_ratios, output_speeds, label='Output Speed', color='red')
    plt.title('Output Speed vs Gear Ratio')
    plt.xlabel('Gear Ratio')
    plt.ylabel('Output Speed (RPM)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

# Main input values
input_teeth = 20  # Number of teeth on the input gear
output_teeth = 100  # Number of teeth on the output gear
input_torque = 10  # Torque applied to the input gear (Nm)
input_speed = 3000  # Speed of the input gear (RPM)

# Calculate gear ratio
gear_ratio = calculate_gear_ratio(input_teeth, output_teeth)
print(f"Gear Ratio: {gear_ratio:.2f}")

# Calculate output torque
output_torque = calculate_output_torque(input_torque, gear_ratio)
print(f"Output Torque: {output_torque:.2f} Nm")

# Calculate output speed
output_speed = calculate_output_speed(input_speed, gear_ratio)
print(f"Output Speed: {output_speed:.2f} RPM")

# Visualize the gear system performance
plot_gear_system(input_torque, input_speed, output_teeth)
