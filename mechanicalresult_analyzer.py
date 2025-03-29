import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit

# Load data (CSV format with columns: 'Displacement (mm)', 'Load (N)')
data = pd.read_csv('tensile_test_data.csv')

# Extracting displacement and load values
displacement = data['Displacement (mm)']
load = data['Load (N)']

# Assume a known cross-sectional area (for example: 10 mm^2)
A = 10  # mm^2
stress = load / A  # Stress = Load / Area (in N/mm^2)
strain = displacement / displacement.max()  # Strain = Displacement / Maximum Displacement

# Linear Elastic Region: Fit a linear model to the first portion of the data
def linear_model(x, m, b):
    return m * x + b

# Fit linear model (elastic region assumption: first 10% of strain)
fit_range = int(0.1 * len(strain))  # First 10% of strain data
popt, _ = curve_fit(linear_model, strain[:fit_range], stress[:fit_range])

# Modulus of elasticity (slope of the linear region)
modulus_of_elasticity = popt[0]  # Slope (N/mm²)
intercept = popt[1]  # Intercept

# Calculate Yield Point based on the linear fit
yield_strain = strain[0] + (yield_stress - intercept) / modulus_of_elasticity
yield_stress = modulus_of_elasticity * yield_strain + intercept

# Plastic Region (After Yield)
# Find maximum stress and strain values (UTS)
uts_stress = stress.max()
uts_strain = strain[stress.idxmax()]

# Power-law fit for plastic region (Strain hardening)
def power_law(x, a, b):
    return a * x ** b

# Fit power-law model to the plastic region (after yield)
plastic_range = (strain > yield_strain)
popt_plastic, _ = curve_fit(power_law, strain[plastic_range], stress[plastic_range])

# Strain Hardening Index
strain_hardening_index = popt_plastic[1]

# Determine fracture point (maximum strain) based on the curve shape
fracture_strain = strain[stress.idxmax()]
fracture_stress = stress.max()

# Print Results
print(f"Modulus of Elasticity (Elastic Region): {modulus_of_elasticity:.2f} N/mm²")
print(f"Yield Stress: {yield_stress:.2f} N/mm² at Yield Strain: {yield_strain:.4f}")
print(f"Ultimate Tensile Strength (UTS): {uts_stress:.2f} N/mm² at UTS Strain: {uts_strain:.4f}")
print(f"Strain Hardening Index: {strain_hardening_index:.4f}")
print(f"Fracture Stress: {fracture_stress:.2f} N/mm² at Fracture Strain: {fracture_strain:.4f}")

# Plot Stress-Strain Curve with Linear and Power-Law Fit
plt.figure(figsize=(10, 8))

# Plot original data
plt.plot(strain, stress, label="Stress-Strain Curve", color='b')

# Linear fit for the elastic region
plt.plot(strain[:fit_range], linear_model(strain[:fit_range], *popt), 'r--', label="Elastic Region Fit")

# Power-law fit for the plastic region
plt.plot(strain[plastic_range], power_law(strain[plastic_range], *popt_plastic), 'g--', label="Plastic Region Fit")

# Mark Yield Point
plt.axvline(x=yield_strain, color='r', linestyle='--', label=f"Yield Point ({yield_strain:.4f}, {yield_stress:.2f})")

# Mark UTS Point
plt.axvline(x=uts_strain, color='g', linestyle='--', label=f"UTS Point ({uts_strain:.4f}, {uts_stress:.2f})")

# Mark Fracture Point
plt.axvline(x=fracture_strain, color='purple', linestyle='--', label=f"Fracture Point ({fracture_strain:.4f}, {fracture_stress:.2f})")

# Labels and Legend
plt.xlabel("Strain")
plt.ylabel("Stress (N/mm²)")
plt.title("Stress-Strain Curve with Fitting Models")
plt.legend()
plt.grid(True)
plt.show()
