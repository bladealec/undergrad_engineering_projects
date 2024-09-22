import time
import RPi.GPIO as GPIO
import numpy as np
import decimal
import os, sys
import math

#clears any previous gpio configurations
GPIO.cleanup()

#setup based on board pin numbers and noat GPIO name
GPIO.setmode(GPIO.BOARD)

#set up the input pins
GPIO.setup(3, GPIO.IN)
GPIO.setup(5, GPIO.IN)

#set up the output pins (to drive the motor)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

#set up Pulse Width Modulation for output pins
#(this allows for the digital pins to emulate analog)

#max frequency is 8000, but causes issues w/ motor driver.
frequency = 100

PWM1 = GPIO.PWM(19,frequency) ;#right wheel
PWM2 = GPIO.PWM(21,frequency) ;#left wheel

#the activation of proportional voltage to
#the pins. In this case it is 60% power
pwm1_percent = 60
pwm2_percent = 60
PWM1.start(pwm1_percent)
PWM2.start(pwm2_percent)
power_l = pwm1_percent
power_r = pwm2_percent

#initiate variables
l_count = 0
r_count = 0
l_count_prev = 0
r_count_prev = 0
l_prev = 0
r_prev = 0
l_RPM = 0
r_RPM = 0
t = 0; #time
t_prev = 0

#additional variables
ARRAY_SIZE_ENCODER = 20  #data points for edge detection
ARRAY_SIZE_RPM = 20       #data points for average RPM
SAMPLE_TIME = 0.1  #time before RPM funct. calculastes speed; 10 samples per second


#starting array
l_array = np.full(ARRAY_SIZE_ENCODER, l_prev)
r_array = np.full(ARRAY_SIZE_ENCODER, r_prev)

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



#RPM array
l_RPM_array = np.full(ARRAY_SIZE_RPM, 0, dtype=decimal.Decimal)
r_RPM_array = np.full(ARRAY_SIZE_RPM, 0, dtype=decimal.Decimal)

#Initializing distance data collection
wheel_diameter_inches = 2 #place holder value
wheel_diameter_meters = wheel_diameter_inches * 0.0254
circumference = math.pi * wheel_diameter_meters

r_distance = 0
l_distance = 0



def RPM_function():
    global l_count, r_count, l_count_prev, r_count_prev, l_RPM, r_RPM
    global l_RPM_array, r_RPM_array, t, t_prev, l_distance, r_distance
	
    #calculatin gow many counts have happened between the last implementation
    l_RPM_now = (l_count - l_count_prev)/40*60/(t - t_prev)
    r_RPM_now = (r_count - r_count_prev)/40*60/(t - t_prev)

    #filter for RPM using arrays
    l_RPM_array = np.insert(l_RPM_array, 0, l_RPM_now)
    l_RPM_array = np.delete(l_RPM_array, -1)
    r_RPM_array = np.insert(r_RPM_array, 0, r_RPM_now)
    r_RPM_array = np.delete(r_RPM_array, -1)

    #averaging the results of the arrays for a single value
    l_RPM = np.mean(l_RPM_array)
    r_RPM = np.mean(r_RPM_array)

    #replacing the previous values
    l_count_prev = l_count
    r_count_prev = r_count
    t_prev = t

    #distance
    time_elapsed = t - t_prev  # in seconds
    speed_right = (r_RPM / 60) * circumference  # meters per second
    speed_left = (l_RPM / 60) * circumference  # meters per second
    
    r_distance += speed_right * time_elapsed
    l_distance += speed_left * time_elapsed

t_start = time.time()
t_sample = SAMPLE_TIME
duration = 10

with open("/home/pi/Documents/encoder_data.csv", 'w') as f:
    f.write('Encoder Data,,\n')
    f.write('time,power_l,l_RPM,power_r,r_RPM\n')

    # Loop through PWM power values
    for pwm_percent in range(0, 101, 10):
        PWM1.start(pwm_percent)
        PWM2.start(pwm_percent)
        
        t_start = time.time()
        t_sample = SAMPLE_TIME
        t = 0
        
        # Reset counts and arrays
        l_count = r_count = 0
        l_count_prev = r_count_prev = 0
        
        # Run the duration for this PWM setting
        while t < duration:
            t = time.time() - t_start
            CounterFunction()

            if t >= t_sample:
                t_sample += SAMPLE_TIME
                RPM_function()
                print(f'time: {t:.02f} L power: {pwm_percent:.02f} L RPM: {l_RPM:.02f} R power: {pwm_percent:.02f} R RPM: {r_RPM:.02f}')
                f.write(f'{t},{pwm_percent},{l_RPM},{pwm_percent},{r_RPM}\n')
