import time
import RPi.GPIO as GPIO
import numpy as np
import decimal
import os, sys
import math


# Clears any previous GPIO configurations
GPIO.cleanup()

# Set up GPIO mode based on board pin numbers
GPIO.setmode(GPIO.BOARD)

# Set up input pins
GPIO.setup(3, GPIO.IN)
GPIO.setup(5, GPIO.IN)

# Set up output pins to drive the motor
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

# Set up Pulse Width Modulation for output pins
frequency = 100
PWM1 = GPIO.PWM(19, frequency)  # Right wheel
PWM2 = GPIO.PWM(21, frequency)  # Left wheel

#FOPDT Parameters (left)
t0_l = 0.346
Tau_l = 0.982
K_l = 1.16

#FOPDT Parameters (left)
t0_r = 0.171
Tau_r = 1.07
K_r = 1.094

# PID Controller Constants (Tuning parameters)
Kc_r = (0.965/K_r) *( t0_r/Tau_r ) ** (-0.85)       # Proportional gain
TI_r = Tau_r / (0.796-0.1465*(t0_r/Tau_r))      # Integral time constant
TD_r = 0.308*Tau_r*(t0_r/Tau_r)**0.929       # Derivative time constant
Kc_l = (0.965/K_l) *( t0_l/Tau_l ) ** (-0.85)       # Proportional gain
TI_l = Tau_l / (0.796-0.1465*(t0_l/Tau_l))      # Integral time constant
TD_l = 0.308*Tau_l*(t0_l/Tau_l)**0.929       # Derivative time constant
bias = 40       # Bias to avoid power being zero
setpoint = 80   # Desired RPM setpoint
SAMPLE_TIME = 0.1  # Sampling time (seconds)
duration = 40   # Duration for the run

# Initialize PID variables
l_I = 0                  # Integral sum for left wheel
r_I = 0                  # Integral sum for right wheel
e_prev_l = 0             # Previous error for left wheel
e_prev_r = 0             # Previous error for right wheel
t_prev_PID_l = time.time()  # Previous time for left wheel
t_prev_PID_r = time.time()  # Previous time for right wheel
t_start = time.time()     # Start time for the run

# Initialize variables for RPM and distance calculation
l_RPM = 0
r_RPM = 0
l_count = 0
r_count = 0
l_count_prev = 0
r_count_prev = 0
t_prev = 0

#Array variables
ARRAY_SIZE_ENCODER = 4  #data points for edge detection
ARRAY_SIZE_RPM = 5     #data points for average RPM

#starting array
l_array = np.full(ARRAY_SIZE_ENCODER, e_prev_l)
r_array = np.full(ARRAY_SIZE_ENCODER, e_prev_r)

#edge comparison array
edge_size = round(ARRAY_SIZE_ENCODER/2)
array_edge_high = np.full(ARRAY_SIZE_ENCODER, 1)
array_edge_high[:-edge_size] = 0
array_edge_low = np.full(ARRAY_SIZE_ENCODER, 0)
array_edge_low[:-edge_size] = 1

def CounterFunction():
    global l, r, l_count, r_count, l_array, r_array, array_edge_high, array_edge_low

    l = GPIO.input(5)
    r = GPIO.input(3)

    # refresh the array - add the newest value to the front
    # and subtract the oldest value from the end
    l_array = np.insert(l_array, 0, l)
    l_array = np.delete(l_array, -1)
    r_array = np.insert(r_array, 0, r)
    r_array = np.delete(r_array, -1)

    # if there is an edge according to the edge array...
    if (r_array == array_edge_high).all() or (r_array == array_edge_low).all():
        r_count += 1
    if (l_array == array_edge_high).all() or (l_array == array_edge_low).all():
        l_count += 1

# Arrays for RPM calculations
l_RPM_array = np.full(20, 0, dtype=decimal.Decimal)
r_RPM_array = np.full(20, 0, dtype=decimal.Decimal)

# Function to calculate RPM based on encoder counts
def RPM_function():
    global l_count, r_count, l_count_prev, r_count_prev, l_RPM, r_RPM
    global l_RPM_array, r_RPM_array, t, t_prev, l_distance, r_distance

    # Calculate RPM
    l_RPM_now = (l_count - l_count_prev) / 40 * 60 / (t - t_prev)
    r_RPM_now = (r_count - r_count_prev) / 40 * 60 / (t - t_prev)

    # Filter RPM using arrays
    l_RPM_array = np.insert(l_RPM_array, 0, l_RPM_now)
    l_RPM_array = np.delete(l_RPM_array, -1)
    r_RPM_array = np.insert(r_RPM_array, 0, r_RPM_now)
    r_RPM_array = np.delete(r_RPM_array, -1)

    # Averaging RPM
    l_RPM = np.mean(l_RPM_array)
    r_RPM = np.mean(r_RPM_array)

    # Update previous values
    l_count_prev = l_count
    r_count_prev = r_count
    t_prev = t


# PID function for left wheel
def PID_function_l():
    global setpoint, l_RPM, Kc, TI, TD, bias, l_I, t_start, t_prev_PID_l, e_prev_l

    # Calculate error
    t = time.time()
    dt = t - t_prev_PID_l
    t_prev_PID_l = t
    e_l = setpoint - l_RPM

    # Proportional, Integral, Derivative terms
    l_P = Kc_l * e_l
    l_I += Kc_l * e_l * dt / TI_l
    l_D = Kc_l * TD_l * (e_l - e_prev_l) / dt

    # Update previous error
    e_prev_l = e_l
    # Calculate power output
    if TI_l == 0:
        power_l = l_P + l_D + bias
    else:
        power_l = l_P + l_I + l_D + bias

    if power_l > 100:
        power_l = 100
    elif power_l < 0:
        power_l = 0

    return power_l

# PID function for right wheel
def PID_function_r():
    global setpoint, r_RPM, Kc, TI, TD, bias, r_I, t_start, t_prev_PID_r, e_prev_r

    # Calculate error
    t = time.time()
    dt = t - t_prev_PID_r
    t_prev_PID_r = t
    e_r = setpoint - r_RPM

    # Proportional, Integral, Derivative terms
    r_P = Kc_r * e_r
    r_I += Kc_r * e_r * dt / TI_r
    r_D = Kc_r * TD_r * (e_r - e_prev_r) / dt

    # Update previous error
    e_prev_r = e_r

    # Calculate power output
    if TI_r == 0:
        power_r = r_P + r_D + bias
    else:
        power_r = r_P + r_I + r_D + bias
        
    if power_r > 100:
        power_r = 100
    elif power_r < 0:
        power_r = 0
        
    return power_r

# Main loop
t_start = time.time()
t_sample = SAMPLE_TIME

with open("/home/pi/Documents/tuning_data_1.csv", 'w') as f:
    f.write('Tuning Data\n')
    f.write('time,input_power_l,l_RPM,input_power_r,r_RPM,setpoint\n')
    
    t = 0  # Reset time
    while t < duration:
        t = time.time() - t_start
        CounterFunction()

        if t >= t_sample:
            t_sample += SAMPLE_TIME
            RPM_function()
            power_l = PID_function_l()  # Get power for left wheel
            power_r = PID_function_r()  # Get power for right wheel
            PWM1.start(power_r)
            PWM2.start(power_l)

            # Write data to file
            f.write(f'{t:.02f},{power_l:.02f},{l_RPM:.02f},{power_r:.02f},{r_RPM:.02f}, {setpoint}\n')

            print(f'{t:.02f} {power_l:.02f} {l_RPM:.02f} {power_r:.02f} {r_RPM:.02f} {setpoint}')

PWM1.stop()
PWM2.stop()
