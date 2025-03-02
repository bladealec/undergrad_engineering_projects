import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# data
data = {
    "AoA": [0, 5, 10, 15, 20],
    "Lift_40": [4.085, 4.138, 4.405, 4.306, 4.116],
    "Drag_40": [1.143, 1.269, 1.355, 1.192, 1.117],
    "Lift_50": [7.164, 7.358, 7.522, 7.063, 6.907],
    "Drag_50": [2.21, 2.265, 2.347, 1.85, 1.618],
    "Lift_60": [9.938, 10.55, 11.296, 10.502, 9.226],
    "Drag_60": [3.313, 3.544, 3.78, 3.604, 3.401],
    "Lift_70": [14.042, 14.59, 14.898, 14.903, 12.566],
    "Drag_70": [4.201, 4.247, 4.302, 4.845, 4.925],
}

df = pd.DataFrame(data)

# Lift-to-Drag ratio (L/D)
df["L/D_40"] = df["Lift_40"] / df["Drag_40"]
df["L/D_50"] = df["Lift_50"] / df["Drag_50"]
df["L/D_60"] = df["Lift_60"] / df["Drag_60"]
df["L/D_70"] = df["Lift_70"] / df["Drag_70"]

# Optimal AoA (max L/D ratio)
optimal_AoA = {}
for speed in ["40", "50", "60", "70"]:
    max_ld_index = df[f"L/D_{speed}"].idxmax()
    optimal_AoA[speed] = df.loc[max_ld_index, "AoA"]

# potential stall points (drop in L/D)
stall_points = {}
for speed in ["40", "50", "60", "70"]:
    stall_index = np.argmax(np.diff(df[f"L/D_{speed}"]) < 0)  # First drop
    stall_points[speed] = df.loc[stall_index, "AoA"] if stall_index > 0 else "No Stall Detected"

# Plot Lift-to-Drag ratio
plt.figure(figsize=(10, 6))
plt.plot(df["AoA"], df["L/D_40"], label="L/D (40 MPH)", marker="o")
plt.plot(df["AoA"], df["L/D_50"], label="L/D (50 MPH)", marker="o")
plt.plot(df["AoA"], df["L/D_60"], label="L/D (60 MPH)", marker="o")
plt.plot(df["AoA"], df["L/D_70"], label="L/D (70 MPH)", marker="o")

# Mark Optimal AoA
for speed, aoa in optimal_AoA.items():
    plt.scatter(aoa, df[f"L/D_{speed}"].max(), label=f"Opt AoA {speed} MPH", marker="x", s=100)

# Mark Stall Points
for speed, stall_aoa in stall_points.items():
    if stall_aoa != "No Stall Detected":
        plt.scatter(stall_aoa, df[df["AoA"] == stall_aoa][f"L/D_{speed}"].values[0], 
                    label=f"Stall {speed} MPH", marker="s", s=100, color="red")

plt.xlabel("Angle of Attack (AoA) [degrees]")
plt.ylabel("Lift-to-Drag Ratio (L/D)")
plt.title("Lift-to-Drag vs. Angle of Attack")
plt.legend()
plt.grid(True)
plt.show()

# Plot Lift
plt.figure(figsize=(10, 6))
plt.plot(df["AoA"], df["Lift_40"], label="Lift(40 MPH)", marker="o")
plt.plot(df["AoA"], df["Lift_50"], label="Lift (50 MPH)", marker="o")
plt.plot(df["AoA"], df["Lift_60"], label="Lift (60 MPH)", marker="o")
plt.plot(df["AoA"], df["Lift_70"], label="Lift (70 MPH)", marker="o")

plt.xlabel("Angle of Attack (AoA) [degrees]")
plt.ylabel("Lift (L)")
plt.title("Lift vs. Angle of Attack")
plt.legend()
plt.grid(True)
plt.show()

# Plot Drag
plt.figure(figsize=(10, 6))
plt.plot(df["AoA"], df["Drag_40"], label="Lift(40 MPH)", marker="o")
plt.plot(df["AoA"], df["Drag_50"], label="Lift (50 MPH)", marker="o")
plt.plot(df["AoA"], df["Drag_60"], label="Lift (60 MPH)", marker="o")
plt.plot(df["AoA"], df["Drag_70"], label="Lift (70 MPH)", marker="o")

plt.xlabel("Angle of Attack (AoA) [degrees]")
plt.ylabel("Drag (D)")
plt.title("Drag vs. Angle of Attack")
plt.legend()
plt.grid(True)
plt.show()



# Print results
print("Optimal AoA for Maximum L/D:")
print(optimal_AoA)
print("\nPotential Stall AoA:")
print(stall_points)
