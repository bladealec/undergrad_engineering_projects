import matplotlib.pyplot as plt
import pandas as pd

# Data from Solidworks Flow Simulations
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

# Plot Lift Forces
plt.figure(figsize=(10, 6))
plt.plot(df["AoA"], df["Lift_40"], label="Lift (40 MPH)", marker="o")
plt.plot(df["AoA"], df["Lift_50"], label="Lift (50 MPH)", marker="o")
plt.plot(df["AoA"], df["Lift_60"], label="Lift (60 MPH)", marker="o")
plt.plot(df["AoA"], df["Lift_70"], label="Lift (70 MPH)", marker="o")

plt.xlabel("Angle of Attack (AoA) [degrees]")
plt.ylabel("Lift Force [lbf]")
plt.title("Lift Forces vs. Angle of Attack")
plt.legend()
plt.grid(True)
plt.show()

# Plot Drag Forces
plt.figure(figsize=(10, 6))
plt.plot(df["AoA"], df["Drag_40"], label="Drag (40 MPH)", marker="s")
plt.plot(df["AoA"], df["Drag_50"], label="Drag (50 MPH)", marker="s")
plt.plot(df["AoA"], df["Drag_60"], label="Drag (60 MPH)", marker="s")
plt.plot(df["AoA"], df["Drag_70"], label="Drag (70 MPH)", marker="s")

plt.xlabel("Angle of Attack (AoA) [degrees]")
plt.ylabel("Drag Force [lbf]")
plt.title("Drag Forces vs. Angle of Attack")
plt.legend()
plt.grid(True)
plt.show()
