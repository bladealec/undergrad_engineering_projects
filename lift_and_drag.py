# Constants
import math

# Function to calculate lift force
def calculate_lift(density, velocity, area, coefficient_of_lift):
    return 0.5 * density * velocity**2 * area * coefficient_of_lift

# Function to calculate drag force
def calculate_drag(density, velocity, area, coefficient_of_drag):
    return 0.5 * density * velocity**2 * area * coefficient_of_drag

def main():
    # Option to use sample values or input values
    use_sample_values = input("Use sample values? (yes/no): ").strip().lower()
    
    if use_sample_values == 'yes':
        # Sample values
        density = 1.225  # kg/m^3 (density of air at sea level)
        velocity = 30.0  # m/s (velocity of the object)
        area = 2.0       # m^2 (reference area)
        coefficient_of_lift = 1.0
        coefficient_of_drag = 0.5
    else:
        # User input
        density = float(input("Enter air density (kg/m^3): "))
        velocity = float(input("Enter velocity (m/s): "))
        area = float(input("Enter reference area (m^2): "))
        coefficient_of_lift = float(input("Enter coefficient of lift: "))
        coefficient_of_drag = float(input("Enter coefficient of drag: "))
    
    # Calculations
    lift = calculate_lift(density, velocity, area, coefficient_of_lift)
    drag = calculate_drag(density, velocity, area, coefficient_of_drag)
    
    # Output results
    print(f"Lift Force: {lift:.2f} N")
    print(f"Drag Force: {drag:.2f} N")

if __name__ == "__main__":
    main()
