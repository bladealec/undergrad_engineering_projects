import math
from scipy.optimize import fsolve

def calculate_velocity(flow_rate, diameter):
    """
    Calculate the fluid velocity.
    :param flow_rate: Flow rate in m^3/s
    :param diameter: Diameter of the pipe in meters
    :return: Velocity in m/s
    """
    area = math.pi * (diameter / 2) ** 2
    return flow_rate / area

def calculate_reynolds_number(density, velocity, diameter, viscosity):
    """
    Calculate the Reynolds number.
    :param density: Density of the fluid in kg/m^3
    :param velocity: Velocity of the fluid in m/s
    :param diameter: Diameter of the pipe in meters
    :param viscosity: Dynamic viscosity of the fluid in Pa.s
    :return: Reynolds number
    """
    return (density * velocity * diameter) / viscosity

def colebrook_white(f, Re, epsilon, diameter):
    """
    Colebrook-White equation to find the friction factor.
    :param f: Initial guess for the friction factor
    :param Re: Reynolds number
    :param epsilon: Roughness of the pipe in meters
    :param diameter: Diameter of the pipe in meters
    :return: Zero for function solver
    """
    return 1 / math.sqrt(f) + 2.0 * math.log10((epsilon / diameter) / 3.7 + 2.51 / (Re * math.sqrt(f)))

def calculate_friction_factor(Re, epsilon, diameter):
    """
    Calculate the friction factor using the Colebrook-White equation.
    :param Re: Reynolds number
    :param epsilon: Roughness of the pipe in meters
    :param diameter: Diameter of the pipe in meters
    :return: Friction factor
    """
    initial_guess = 0.02
    return fsolve(colebrook_white, initial_guess, args=(Re, epsilon, diameter))[0]

def calculate_pressure_drop(length, diameter, friction_factor, density, velocity):
    """
    Calculate the pressure drop using the Darcy-Weisbach equation.
    :param length: Length of the pipe in meters
    :param diameter: Diameter of the pipe in meters
    :param friction_factor: Friction factor
    :param density: Density of the fluid in kg/m^3
    :param velocity: Velocity of the fluid in m/s
    :return: Pressure drop in Pascals
    """
    return friction_factor * (length / diameter) * (density * velocity ** 2) / 2

# Example usage
flow_rate = 0.05  # m^3/s
length = 100  # m
diameter = 0.1  # m
density = 1000  # kg/m^3
viscosity = 1e-3  # Pa.s
roughness = 0.00015  # m

velocity = calculate_velocity(flow_rate, diameter)
Re = calculate_reynolds_number(density, velocity, diameter, viscosity)
friction_factor = calculate_friction_factor(Re, roughness, diameter)
pressure_drop = calculate_pressure_drop(length, diameter, friction_factor, density, velocity)

print(f"Velocity: {velocity:.2f} m/s")
print(f"Reynolds number: {Re:.0f}")
print(f"Friction factor: {friction_factor:.4f}")
print(f"Pressure drop: {pressure_drop:.2f} Pa")
