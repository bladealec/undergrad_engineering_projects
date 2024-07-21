import numpy as np
from scipy.special import erf

def fick_second_law_2d(D, C0, Cs, t, x, y):
    """
    Calculate the concentration profile in 2D using Fick's second law.
    
    Parameters:
    D (float): Diffusion coefficient in m^2/s.
    C0 (float): Initial concentration in mol/m^3.
    Cs (float): Surface concentration in mol/m^3.
    t (float): Time in seconds.
    x (float): X-coordinate in meters.
    y (float): Y-coordinate in meters.
    
    Returns:
    float: Concentration at coordinates (x, y) after time t in mol/m^3.
    """
    r = np.sqrt(x**2 + y**2)
    return Cs + (C0 - Cs) * erf(r / (2 * np.sqrt(D * t)))

def convert_units(value, from_unit, to_unit, conversion_factors):
    return value * conversion_factors[from_unit] / conversion_factors[to_unit]

def get_input(prompt, units):
    print(f"Available units: {', '.join(units)}")
    value = float(input(f"{prompt}: "))
    unit = input(f"Enter the unit you used for {prompt}: ").strip()
    return value, unit

def solve_for_variable(variable, conversion_factors):
    if variable == 'D':
        C, C_unit = get_input("Enter the concentration (C)", ['mol/m^3'])
        C0, C0_unit = get_input("Enter the initial concentration (C0)", ['mol/m^3'])
        Cs, Cs_unit = get_input("Enter the surface concentration (Cs)", ['mol/m^3'])
        t, t_unit = get_input("Enter the time (t)", ['seconds', 'minutes', 'hours'])
        x, x_unit = get_input("Enter the x-coordinate (x)", ['meters', 'centimeters', 'millimeters'])
        y, y_unit = get_input("Enter the y-coordinate (y)", ['meters', 'centimeters', 'millimeters'])

        C = convert_units(C, C_unit, 'mol/m^3', conversion_factors)
        C0 = convert_units(C0, C0_unit, 'mol/m^3', conversion_factors)
        Cs = convert_units(Cs, Cs_unit, 'mol/m^3', conversion_factors)
        t = convert_units(t, t_unit, 'seconds', conversion_factors)
        x = convert_units(x, x_unit, 'meters', conversion_factors)
        y = convert_units(y, y_unit, 'meters', conversion_factors)

        r = np.sqrt(x**2 + y**2)
        D = (r / (2 * np.sqrt(t * (erf((C - Cs) / (C0 - Cs))))))**2
        return D, 'm^2/s'

    elif variable == 'C':
        D, D_unit = get_input("Enter the diffusion coefficient (D)", ['m^2/s'])
        C0, C0_unit = get_input("Enter the initial concentration (C0)", ['mol/m^3'])
        Cs, Cs_unit = get_input("Enter the surface concentration (Cs)", ['mol/m^3'])
        t, t_unit = get_input("Enter the time (t)", ['seconds', 'minutes', 'hours'])
        x, x_unit = get_input("Enter the x-coordinate (x)", ['meters', 'centimeters', 'millimeters'])
        y, y_unit = get_input("Enter the y-coordinate (y)", ['meters', 'centimeters', 'millimeters'])

        D = convert_units(D, D_unit, 'm^2/s', conversion_factors)
        C0 = convert_units(C0, C0_unit, 'mol/m^3', conversion_factors)
        Cs = convert_units(Cs, Cs_unit, 'mol/m^3', conversion_factors)
        t = convert_units(t, t_unit, 'seconds', conversion_factors)
        x = convert_units(x, x_unit, 'meters', conversion_factors)
        y = convert_units(y, y_unit, 'meters', conversion_factors)

        C = fick_second_law_2d(D, C0, Cs, t, x, y)
        return C, 'mol/m^3'

    elif variable == 'C0':
        C, C_unit = get_input("Enter the concentration (C)", ['mol/m^3'])
        D, D_unit = get_input("Enter the diffusion coefficient (D)", ['m^2/s'])
        Cs, Cs_unit = get_input("Enter the surface concentration (Cs)", ['mol/m^3'])
        t, t_unit = get_input("Enter the time (t)", ['seconds', 'minutes', 'hours'])
        x, x_unit = get_input("Enter the x-coordinate (x)", ['meters', 'centimeters', 'millimeters'])
        y, y_unit = get_input("Enter the y-coordinate (y)", ['meters', 'centimeters', 'millimeters'])

        C = convert_units(C, C_unit, 'mol/m^3', conversion_factors)
        D = convert_units(D, D_unit, 'm^2/s', conversion_factors)
        Cs = convert_units(Cs, Cs_unit, 'mol/m^3', conversion_factors)
        t = convert_units(t, t_unit, 'seconds', conversion_factors)
        x = convert_units(x, x_unit, 'meters', conversion_factors)
        y = convert_units(y, y_unit, 'meters', conversion_factors)

        r = np.sqrt(x**2 + y**2)
        C0 = (C - Cs) / erf(r / (2 * np.sqrt(D * t))) + Cs
        return C0, 'mol/m^3'

    elif variable == 'Cs':
        C, C_unit = get_input("Enter the concentration (C)", ['mol/m^3'])
        D, D_unit = get_input("Enter the diffusion coefficient (D)", ['m^2/s'])
        C0, C0_unit = get_input("Enter the initial concentration (C0)", ['mol/m^3'])
        t, t_unit = get_input("Enter the time (t)", ['seconds', 'minutes', 'hours'])
        x, x_unit = get_input("Enter the x-coordinate (x)", ['meters', 'centimeters', 'millimeters'])
        y, y_unit = get_input("Enter the y-coordinate (y)", ['meters', 'centimeters', 'millimeters'])

        C = convert_units(C, C_unit, 'mol/m^3', conversion_factors)
        D = convert_units(D, D_unit, 'm^2/s', conversion_factors)
        C0 = convert_units(C0, C0_unit, 'mol/m^3', conversion_factors)
        t = convert_units(t, t_unit, 'seconds', conversion_factors)
        x = convert_units(x, x_unit, 'meters', conversion_factors)
        y = convert_units(y, y_unit, 'meters', conversion_factors)

        r = np.sqrt(x**2 + y**2)
        Cs = C - (C0 - Cs) * erf(r / (2 * np.sqrt(D * t)))
        return Cs, 'mol/m^3'

    elif variable == 't':
        C, C_unit = get_input("Enter the concentration (C)", ['mol/m^3'])
        D, D_unit = get_input("Enter the diffusion coefficient (D)", ['m^2/s'])
        C0, C0_unit = get_input("Enter the initial concentration (C0)", ['mol/m^3'])
        Cs, Cs_unit = get_input("Enter the surface concentration (Cs)", ['mol/m^3'])
        x, x_unit = get_input("Enter the x-coordinate (x)", ['meters', 'centimeters', 'millimeters'])
        y, y_unit = get_input("Enter the y-coordinate (y)", ['meters', 'centimeters', 'millimeters'])

        C = convert_units(C, C_unit, 'mol/m^3', conversion_factors)
        D = convert_units(D, D_unit, 'm^2/s', conversion_factors)
        C0 = convert_units(C0, C0_unit, 'mol/m^3', conversion_factors)
        Cs = convert_units(Cs, Cs_unit, 'mol/m^3', conversion_factors)
        x = convert_units(x, x_unit, 'meters', conversion_factors)
        y = convert_units(y, y_unit, 'meters', conversion_factors)

        r = np.sqrt(x**2 + y**2)
        t = (r / (2 * np.sqrt(D * erf((C - Cs) / (C0 - Cs)))))**2
        return t, 'seconds'

    elif variable == 'x' or variable == 'y':
        C, C_unit = get_input("Enter the concentration (C)", ['mol/m^3'])
        D, D_unit = get_input("Enter the diffusion coefficient (D)", ['m^2/s'])
        C0, C0_unit = get_input("Enter the initial concentration (C0)", ['mol/m^3'])
        Cs, Cs_unit = get_input("Enter the surface concentration (Cs)", ['mol/m^3'])
        t, t_unit = get_input("Enter the time (t)", ['seconds', 'minutes', 'hours'])

        C = convert_units(C, C_unit, 'mol/m^3', conversion_factors)
        D = convert_units(D, D_unit, 'm^2/s', conversion_factors)
        C0 = convert_units(C0, C0_unit, 'mol/m^3', conversion_factors)
        Cs = convert_units(Cs, Cs_unit, 'mol/m^3', conversion_factors)
        t = convert_units(t, t_unit, 'seconds', conversion_factors)

        r = 2 * np.sqrt(D * t) * erf((C - Cs) / (C0 - Cs))
        if variable == 'x':
            x = np.sqrt(r**2 - y**2)
            return x, 'meters'
        else:
            y = np.sqrt(r**2 - x**2)
            return y, 'meters'

def main():
    conversion_factors = {
        'm^2/s': 1, 'mol/m^3': 1, 'seconds': 1, 'minutes': 60, 'hours': 3600,
        'meters': 1, 'centimeters': 0.01, 'millimeters': 0.001
    }

    variable = input("Which variable would you like to solve for (D, C, C0, Cs, t, x, y)? ").strip()
    result, unit = solve_for_variable(variable, conversion_factors)
    print(f"The value of {variable} is: {result} {unit}")

if __name__ == "__main__":
    main()
