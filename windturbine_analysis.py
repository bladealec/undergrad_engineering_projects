import numpy as np
import matplotlib.pyplot as plt

R = 40  # Rotor radius in meters
air_density = 1.225  # kg/m^3
efficiency = 0.4

wind_speeds = np.linspace(0, 25, 100)
swept_area = np.pi * R**2

power_output = 0.5 * air_density * swept_area * (wind_speeds**3) * efficiency
rotor_speed = (wind_speeds * 60) / (2 * np.pi * R)

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(wind_speeds, power_output / 1000, color='blue', label='Power Output (kW)')
plt.title('Wind Speed vs Power Output')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Power Output (kW)')
plt.grid()
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(wind_speeds, rotor_speed, color='green', label='Rotor Speed (RPM)')
plt.title('Wind Speed vs Rotor Speed')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Rotor Speed (RPM)')
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
