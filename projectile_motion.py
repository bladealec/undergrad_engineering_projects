import numpy as np
import matplotlib.pyplot as plt

def calculate_lift_drag(density, velocity, area, lift_coefficient, drag_coefficient):
    """
    Calculate lift and drag forces.

    Parameters:
    - density: Density of the fluid (kg/m^3)
    - velocity: Velocity of the object (m/s)
    - area: Reference area of the object (m^2)
    - lift_coefficient: Coefficient of lift (dimensionless)
    - drag_coefficient: Coefficient of drag (dimensionless)

    Returns:
    - lift: Lift force (N)
    - drag: Drag force (N)
    """
    lift = 0.5 * density * velocity**2 * area * lift_coefficient
    drag = 0.5 * density * velocity**2 * area * drag_coefficient
    return lift, drag

def projectile_motion(initial_velocity, launch_angle, mass, area, lift_coefficient, drag_coefficient, time_step=0.01, total_time=10):
    """
    Simulate the projectile motion under the influence of lift and drag forces.

    Parameters:
    - initial_velocity: Initial velocity of the projectile (m/s)
    - launch_angle: Launch angle (degrees)
    - mass: Mass of the projectile (kg)
    - area: Reference area of the projectile (m^2)
    - lift_coefficient: Coefficient of lift (dimensionless)
    - drag_coefficient: Coefficient of drag (dimensionless)
    - time_step: Time step for simulation (s)
    - total_time: Total simulation time (s)
    
    Returns:
    - times: Array of time values (s)
    - positions: Array of (x, y) positions (m)
    """
    g = 9.81  # gravitational acceleration (m/s^2)
    launch_angle_rad = np.radians(launch_angle)  # convert angle to radians
    vx = initial_velocity * np.cos(launch_angle_rad)  # initial velocity in x
    vy = initial_velocity * np.sin(launch_angle_rad)  # initial velocity in y

    # Lists to store time and position values
    times = [0]
    positions = [(0, 0)]  # initial position

    density = 1.225  # kg/m^3 (air at sea level)
    
    for t in np.arange(time_step, total_time, time_step):
        velocity = np.sqrt(vx**2 + vy**2)  # resultant velocity
        lift, drag = calculate_lift_drag(density, velocity, area, lift_coefficient, drag_coefficient)

        # Update forces
        drag_force_x = drag * (vx / velocity)  # drag force in x direction
        drag_force_y = drag * (vy / velocity)  # drag force in y direction
        net_force_x = -drag_force_x
        net_force_y = -mass * g - drag_force_y + lift  # net force in y direction

        # Update velocities
        vx += (net_force_x / mass) * time_step
        vy += (net_force_y / mass) * time_step

        # Update positions
        new_x = positions[-1][0] + vx * time_step
        new_y = positions[-1][1] + vy * time_step

        positions.append((new_x, new_y))
        times.append(t)

        # Stop simulation if the projectile hits the ground
        if new_y < 0:
            break

    return times, positions

# Simulation parameters
initial_velocity = 50.0  # m/s
launch_angle = 45.0      # degrees
mass = 2.0               # kg
area = 0.1               # m^2
lift_coefficient = 0.5   # dimensionless
drag_coefficient = 0.05  # dimensionless

# Run the simulation
times, positions = projectile_motion(initial_velocity, launch_angle, mass, area, lift_coefficient, drag_coefficient)

# Extract x and y positions
x_positions, y_positions = zip(*positions)

# Plot the trajectory
plt.figure(figsize=(12, 6))
plt.plot(x_positions, y_positions)
plt.title('Projectile Motion with Lift and Drag')
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.grid()
plt.xlim(0, max(x_positions) * 1.1)
plt.ylim(0, max(y_positions) * 1.1)
plt.axhline(0, color='black', lw=0.8)  # ground line
plt.show()
