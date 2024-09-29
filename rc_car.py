import time
import RPi.GPIO as GPIO
import numpy as np
import decimal
import os
import matplotlib.pyplot as plt

# Clear any unintended GPIO configurations
GPIO.cleanup()

# Setup based on board pin numbers and not GPIO name
GPIO.setmode(GPIO.BOARD)

# Set up the input pins
GPIO.setup(3, GPIO.IN)
GPIO.setup(5, GPIO.IN)

# Set up the output pins (to drive the motor)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

# Set up Pulse Width Modulation for output pins
frequency = 100
PWM1 = GPIO.PWM(19, frequency)  # Right wheel
PWM2 = GPIO.PWM(21, frequency)  # Left wheel

# Initiate variables
l_count = 0
r_count = 0
l_count_prev = 0
r_count_prev = 0
l_prev = 0
r_prev = 0
l_RPM = 0
r_RPM = 0
t = 0  # Time
t_prev = 0

ARRAY_SIZE_ENCODER = 20
ARRAY_SIZE_RPM = 20
SAMPLE_TIME = 0.1

# Starting array
l_array = np.full(ARRAY_SIZE_ENCODER, l_prev)
r_array = np.full(ARRAY_SIZE_ENCODER, l_prev)

# Edge comparison array
edge_size = round(ARRAY_SIZE_ENCODER / 2)
array_edge_high = np.full(ARRAY_SIZE_ENCODER, 1)
array_edge_high[:-edge_size] = 0
array_edge_low = np.full(ARRAY_SIZE_ENCODER, 0)
array_edge_low[:-edge_size] = 1

def CounterFunction():
    global l, r, l_count, r_count, l_array, r_array, array_edge_high, array_edge_low

    l = GPIO.input(5)
    r = GPIO.input(3)

    # Refresh the array
    l_array = np.insert(l_array, 0, l)
    l_array = np.delete(l_array, -1)
    r_array = np.insert(r_array, 0, r)
    r_array = np.delete(r_array, -1)

    # Edge detection
    if (r_array == array_edge_high).all() or (r_array == array_edge_low).all():
        r_count += 1
    if (l_array == array_edge_high).all() or (l_array == array_edge_low).all():
        l_count += 1

# RPM calculation
l_RPM_array = np.full(ARRAY_SIZE_RPM, 0, dtype=decimal.Decimal)
r_RPM_array = np.full(ARRAY_SIZE_RPM, 0, dtype=decimal.Decimal)

def RPM_function():
    global l_count, r_count, l_count_prev, r_count_prev, l_RPM, r_RPM
    global l_RPM_array, r_RPM_array, t, t_prev
    
    l_RPM_now = (l_count - l_count_prev) / 40 * 60 / (t - t_prev)
    r_RPM_now = (r_count - r_count_prev) / 40 * 60 / (t - t_prev)

    # Filter for RPM using arrays
    l_RPM_array = np.insert(l_RPM_array, 0, l_RPM_now)
    l_RPM_array = np.delete(l_RPM_array, -1)
    r_RPM_array = np.insert(r_RPM_array, 0, r_RPM_now)
    r_RPM_array = np.delete(r_RPM_array, -1)

    # Averaging the results
    l_RPM = np.mean(l_RPM_array)
    r_RPM = np.mean(r_RPM_array)

    # Replace previous values
    l_count_prev = l_count
    r_count_prev = r_count
    t_prev = t

# Main loop for testing power levels
power_levels = np.arange(10, 110, 10)  # Power levels from 10% to 100%
num_trials = 3  # Number of trials per power level
duration = 10  # Duration for each trial

with open("/home/pi/Desktop/encoder_data/encoder_data.csv", 'w') as f:
    f.write(f'Encoder Data\n')
    f.write(f'time,l_power,l_RPM,r_pwr,r_RPM,trial,power_level\n')

    for power in power_levels:
        for trial in range(1, num_trials + 1):
            # Start PWM with the current power level
            PWM1.start(power)
            PWM2.start(power)

            t_start = time.time()
            t_sample = SAMPLE_TIME

            # Reset counts and time
            l_count = r_count = 0
            t = 0
            t_prev = 0

            # Run for the duration
            while t < duration:
                t = time.time() - t_start
                CounterFunction()

                if t >= t_sample:
                    t_sample += SAMPLE_TIME
                    RPM_function()

                    # Log data with trial number and power level
                    f.write(f'{t},{power},{l_RPM},{power},{r_RPM},{trial},{power}\n')
                    print(f'Trial {trial}, Power: {power}%, Time: {t:.02f}, L RPM: {l_RPM:.02f}, R RPM: {r_RPM:.02f}')

            # Stop the motors before next trial
            PWM1.stop()
            PWM2.stop()

# Clean up
GPIO.cleanup()

# Plotting
# Collecting data for plotting
time_data = []
l_rpm_data = []
r_rpm_data = []
trial_data = []

with open("/home/pi/Desktop/encoder_data/encoder_data.csv", 'r') as f:
    next(f)  # Skip the header
    for line in f:
        parts = line.strip().split(',')
        time_data.append(float(parts[0]))
        l_rpm_data.append(float(parts[2]))
        r_rpm_data.append(float(parts[4]))
        trial_data.append(int(parts[5]))
        power_level = int(parts[6])  # Collecting power level

# Convert data lists to numpy arrays for easier manipulation
time_data = np.array(time_data)
l_rpm_data = np.array(l_rpm_data)
r_rpm_data = np.array(r_rpm_data)
trial_data = np.array(trial_data)

# Plotting
for power in power_levels:
    for trial in range(1, num_trials + 1):
        plt.figure(figsize=(12, 6))
        
        # Filter indices for the current power level and trial
        indices = np.where((trial_data == trial) & (np.array([int(line.split(',')[6]) for line in open("/home/pi/Desktop/encoder_data/encoder_data.csv", 'r').readlines()[1:]]) == power))[0]

        # Plotting RPM for left wheel
        plt.plot(time_data[indices], l_rpm_data[indices], label='Left Wheel RPM', color='blue', alpha=0.6)
        
        # Plotting RPM for right wheel
        plt.plot(time_data[indices], r_rpm_data[indices], label='Right Wheel RPM', color='red', alpha=0.6)

        # Adding titles and labels
        plt.title(f'RPM vs. Time for Both Wheels - Power Level: {power}%, Trial: {trial}')
        plt.xlabel('Time (seconds)')
        plt.ylabel('RPM')
        plt.legend()
        plt.grid()
        plt.show()

PWM1.stop()
PWM2.stop()
