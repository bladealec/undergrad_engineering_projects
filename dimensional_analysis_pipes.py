import numpy as np

def calculate_reynolds_number(flow_rate, diameter, fluid_density, fluid_viscosity):
    velocity = (4 * flow_rate) / (np.pi * diameter**2)  # velocity in m/s
    Re = (fluid_density * velocity * diameter) / fluid_viscosity
    return Re, velocity

def calculate_friction_factor(Re, diameter, roughness):
    if Re < 2000:  # Laminar flow
        return 64 / Re
    else:  # Turbulent flow
        f_initial_guess = 0.02  # initial guess for friction factor
        for _ in range(10):  # iterative solution
            f_initial_guess = (1 / (-2 * np.log10(roughness / (3.7 * diameter) + 5.74 / Re**0.9)))**2
        return f_initial_guess

def calculate_head_loss(friction_factor, length, diameter, velocity):
    return friction_factor * (length / diameter) * (velocity**2 / (2 * 9.81))

def main():
    print("Dimensional Analysis for Pipe Design")
    print("Choose the parameter to solve for:")
    print("1. Reynolds Number")
    print("2. Velocity")
    print("3. Friction Factor")
    print("4. Head Loss")
    choice = input("Enter the number of your choice: ")

    # Common parameters
    fluid_density = 1000  # kg/m^3 (default for water)
    fluid_viscosity = 0.001  # Pa·s (default for water)
    pipe_length = 50  # m (default pipe length)
    pipe_roughness = 0.0002  # m (default roughness)

    if choice == '1':  # Solve for Reynolds Number
        flow_rate = float(input("Enter flow rate (m^3/s): "))
        diameter = float(input("Enter pipe diameter (m): "))
        Re, velocity = calculate_reynolds_number(flow_rate, diameter, fluid_density, fluid_viscosity)
        print(f"Reynolds Number: {Re:.2f} (Flow Regime: {'Laminar' if Re < 2000 else 'Turbulent'})")
        print(f"Velocity: {velocity:.2f} m/s")

    elif choice == '2':  # Solve for Velocity
        flow_rate = float(input("Enter flow rate (m^3/s): "))
        diameter = float(input("Enter pipe diameter (m): "))
        velocity = (4 * flow_rate) / (np.pi * diameter**2)  # velocity in m/s
        print(f"Velocity: {velocity:.2f} m/s")

    elif choice == '3':  # Solve for Friction Factor
        Re = float(input("Enter Reynolds number (dimensionless): "))
        diameter = float(input("Enter pipe diameter (m): "))
        roughness = float(input("Enter pipe roughness height (m): "))
        friction_factor = calculate_friction_factor(Re, diameter, roughness)
        print(f"Friction Factor: {friction_factor:.4f}")

    elif choice == '4':  # Solve for Head Loss
        flow_rate = float(input("Enter flow rate (m^3/s): "))
        diameter = float(input("Enter pipe diameter (m): "))
        length = float(input("Enter pipe length (m): "))
        roughness = float(input("Enter pipe roughness height (m): "))

        Re, velocity = calculate_reynolds_number(flow_rate, diameter, fluid_density, fluid_viscosity)
        friction_factor = calculate_friction_factor(Re, diameter, roughness)
        head_loss = calculate_head_loss(friction_factor, length, diameter, velocity)

        print(f"Head Loss: {head_loss:.2f} m")

    else:
        print("Invalid choice. Please run the program again.")

if __name__ == "__main__":
    main()
