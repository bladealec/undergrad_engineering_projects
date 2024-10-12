import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rated_power = 1000  # Rated power in watts
constant_speed = 300  # RPM for power vs load plot
blade_angle_tbd = 10  # Blade angle for power vs load plot
load_resistance = 10  # Load resistance in ohms for power vs load plot
blade_angles = [5, 10, 15, 20, 25]  # Blade angles for power vs wind speed
single_load = 10  # Single load resistance in ohms for wind speed plot

data = pd.read_csv('wind_turbine.csv')

voltage = data['RMS Voltage A (Volts)']
current = data['Current A (Amps)']
power = voltage * current

load = np.linspace(1, 100, 100)
power_vs_load = voltage**2 / load

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(load, power_vs_load, label=f'Angle: {blade_angle_tbd}° @ {constant_speed} RPM')
plt.title('Power vs Load Resistance')
plt.xlabel('Load Resistance (Ohms)')
plt.ylabel('Power (Watts)')
plt.grid()
plt.legend()

plt.subplot(1, 2, 2)
for angle in blade_angles:
    wind_speed = data[data['Blade Angle (degrees)'] == angle]['Wind Speed (m/s)']
    power = data[data['Blade Angle (degrees)'] == angle]['Power (Watts)']
    plt.plot(wind_speed, power, label=f'Angle: {angle}°')

plt.title('Power vs Wind Speed for Different Blade Angles')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Power (Watts)')
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()

plt.figure(figsize=(7, 6))
for angle in blade_angles:
    wind_speed = data[data['Blade Angle (degrees)'] == angle]['Wind Speed (m/s)']
    power = data[data['Blade Angle (degrees)'] == angle]['Power (Watts)']
    wind_speeds_for_rated_power = wind_speed[power >= rated_power]
    plt.plot(wind_speeds_for_rated_power, np.full_like(wind_speeds_for_rated_power, angle), label=f'Power: {rated_power}W')

plt.title('Blade Angle vs Wind Speed for Rated Power')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Blade Angle (degrees)')
plt.grid()
plt.legend()
plt.show()

data['Power Factor'] = voltage * current / rated_power
data['Advance Ratio'] = data['Rotor RPM'] / (data['Wind Speed (m/s)'] * 60 / (2 * np.pi * R))

print(data[['Blade Angle (degrees)', 'Wind Speed (m/s)', 'Power Factor', 'Advance Ratio']])
