import numpy as np
from scipy.special import erf
import matplotlib.pyplot as plt

def convert_units(value, from_unit, to_unit, conversion_factors):
    return value * conversion_factors[to_unit] / conversion_factors[from_unit]

def get_input(prompt, valid_units):
    value = float(input(f"{prompt}: "))
    unit = input(f"Available units: {', '.join(valid_units)}\nThe unit for {prompt}: ").strip().lower()
    if unit not in valid_units:
        raise ValueError(f"Invalid unit. Available units are: {', '.join(valid_units)}")
    return value, unit

def calculate_average_atomic_density(concentration, molar_volume):
    return concentration / molar_volume

def plot_concentration_gradient(D, C0, Cs, t, x_range, y_range):
    x = np.linspace(x_range[0], x_range[1], 100)
    y = np.linspace(y_range[0], y_range[1], 100)
    X, Y = np.meshgrid(x, y)
    Z = C0 + (Cs - C0) * erf(np.sqrt(X**2 + Y**2) / (2 * np.sqrt(D * t)))

    plt.contourf(X, Y, Z, levels=100, cmap='viridis')
    plt.colorbar(label='Concentration (mol/m^3)')
    plt.xlabel('X (meters)')
    plt.ylabel('Y (meters)')
    plt.title('Concentration Gradient')
    plt.show()

def fick_second_law_2d(D, C0, Cs, t, x, y):
    r = np.sqrt(x**2 + y**2)
    return C0 + (Cs - C0) * erf(r / (2 * np.sqrt(D * t)))

def solve_for_variable(variable, conversion_factors):
    if variable in ['d', 'c', 'c0', 'cs', 't', 'x', 'y']:
        if variable != 'd':
            C, C_unit = get_input("The concentration (C)", ['mol/m^3'])
        else:
            C, C_unit = 0, 'mol/m^3'  # Placeholder

        if variable != 'c0':
            C0, C0_unit = get_input("The initial concentration (C0)", ['mol/m^3'])
        else:
            C0, C0_unit = 0, 'mol/m^3'  # Placeholder

        if variable != 'cs':
            Cs, Cs_unit = get_input("The surface concentration (Cs)", ['mol/m^3'])
        else:
            Cs, Cs_unit = 0, 'mol/m^3'  # Placeholder

        if variable != 'd':
            D, D_unit = get_input("The diffusion coefficient (D)", ['m^2/s'])
        else:
            D, D_unit = 0, 'm^2/s'  # Placeholder

        if variable != 't':
            t, t_unit = get_input("The time (t)", ['seconds', 'minutes', 'hours'])
        else:
            t, t_unit = 0, 'seconds'  # Placeholder

        if variable != 'x':
            x, x_unit = get_input("The x-coordinate (x)", ['meters', 'centimeters', 'millimeters'])
        else:
            x, x_unit = 0, 'meters'  # Placeholder

        if variable != 'y':
            y, y_unit = get_input("The y-coordinate (y)", ['meters', 'centimeters', 'millimeters'])
        else:
            y, y_unit = 0, 'meters'  # Placeholder

        C = convert_units(C, C_unit, 'mol/m^3', conversion_factors)
        C0 = convert_units(C0, C0_unit, 'mol/m^3', conversion_factors)
        Cs = convert_units(Cs, Cs_unit, 'mol/m^3', conversion_factors)
        D = convert_units(D, D_unit, 'm^2/s', conversion_factors)
        t = convert_units(t, t_unit, 'seconds', conversion_factors)
        x = convert_units(x, x_unit, 'meters', conversion_factors)
        y = convert_units(y, y_unit, 'meters', conversion_factors)

        if variable == 'd':
            r = np.sqrt(x**2 + y**2)
            D = (r / (2 * np.sqrt(t * erf((C - Cs) / (C0 - Cs)))))**2
            return D, 'm^2/s'

        elif variable == 'c':
            C = fick_second_law_2d(D, C0, Cs, t, x, y)
            return C, 'mol/m^3'

        elif variable == 'c0':
            r = np.sqrt(x**2 + y**2)
            C0 = C - (C - Cs) / erf(r / (2 * np.sqrt(D * t)))
            return C0, 'mol/m^3'

        elif variable == 'cs':
            r = np.sqrt(x**2 + y**2)
            Cs = C - (C0 - Cs) * erf(r / (2 * np.sqrt(D * t)))
            return Cs, 'mol/m^3'

        elif variable == 't':
            r = np.sqrt(x**2 + y**2)
            t = (r / (2 * np.sqrt(D * erf((C - Cs) / (C0 - Cs)))))**2
            return t, 'seconds'

        elif variable == 'x' or variable == 'y':
            if variable == 'x':
                y = convert_units(y, y_unit, 'meters', conversion_factors)
                r = 2 * np.sqrt(D * t) * erf((C - Cs) / (C0 - Cs))
                x = np.sqrt(r**2 - y**2)
                return x, 'meters'
            else:
                x = convert_units(x, x_unit, 'meters', conversion_factors)
                r = 2 * np.sqrt(D * t) * erf((C - Cs) / (C0 - Cs))
                y = np.sqrt(r**2 - x**2)
                return y, 'meters'
    else:
        raise ValueError("Invalid variable to solve for.")

def main():
    conversion_factors = {
        'm^2/s': 1, 'mol/m^3': 1, 'seconds': 1, 'minutes': 60, 'hours': 3600,
        'meters': 1, 'centimeters': 0.01, 'millimeters': 0.001
    }

    variable = input("Which variable would you like to solve for (D, C, C0, Cs, t, x, y)? ").strip().lower()
    
    try:
        result, unit = solve_for_variable(variable, conversion_factors)
        print(f"The value of {variable.upper()} is: {result} {unit}")
        
        if variable in ['d', 'c']:
            x_range = [float(i) for i in input("Enter the x-range for plotting (e.g., 0 0.1): ").split()]
            y_range = [float(i) for i in input("Enter the y-range for plotting (e.g., 0 0.1): ").split()]
            plot_concentration_gradient(result, *get_input_params_for_plotting(), x_range, y_range)

    except ValueError as e:
        print(e)

def get_input_params_for_plotting():
    D, D_unit = get_input("Enter the diffusion coefficient (D)", ['m^2/s'])
    C0, C0_unit = get_input("Enter the initial concentration (C0)", ['mol/m^3'])
    Cs, Cs_unit = get_input("Enter the surface concentration (Cs)", ['mol/m^3'])
    t, t_unit = get_input("Enter the time (t)", ['seconds', 'minutes', 'hours'])
    return (
        convert_units(D, D_unit, 'm^2/s', conversion_factors),
        convert_units(C0, C0_unit, 'mol/m^3', conversion_factors),
        convert_units(Cs, Cs_unit, 'mol/m^3', conversion_factors),
        convert_units(t, t_unit, 'seconds', conversion_factors)
    )

if __name__ == "__main__":
    main()
