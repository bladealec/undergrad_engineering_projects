import numpy as np
import matplotlib.pyplot as plt

# Sample data for the pump curve
# Replace these arrays with actual data from the pump manufacturer or experiment
flow_rate = np.array([0, 10, 20, 30, 40, 50, 60, 70])  # Flow rate in cubic meters per hour (m^3/h)
head = np.array([50, 48, 45, 40, 35, 28, 18, 5])         # Head in meters (m)

# Optional: Efficiency data
# efficiency = np.array([0, 50, 65, 75, 80, 78, 70, 60])  # Efficiency in percentage (%)

# Create the plot
plt.figure(figsize=(8, 6))

# Plot Head vs Flow Rate
plt.plot(flow_rate, head, label="Pump Head Curve", marker='o', linestyle='-')

# Uncomment this section if you want to include efficiency in the plot
# plt.plot(flow_rate, efficiency, label="Pump Efficiency Curve", marker='s', linestyle='--')

# Add labels and title
plt.title("Pump Performance Curve")
plt.xlabel("Flow Rate (m^3/h)")
plt.ylabel("Head (m)")
plt.grid(True)
plt.legend()

# Show the plot
plt.show()

# Optional: Find flow rate for a specific head using interpolation
def interpolate_head_for_flow(target_head, flow_rate, head):
    return np.interp(target_head, head[::-1], flow_rate[::-1])  # Reverse arrays for descending order

# Example: Find the flow rate when the head is 30 meters
target_head = 30
corresponding_flow = interpolate_head_for_flow(target_head, flow_rate, head)
print(f"The flow rate corresponding to a head of {target_head} m is approximately {corresponding_flow:.2f} m^3/h.")

# Calculate head given flow rate and cross-sectional area
def calculate_head(flow_rate, area, gravity=9.81):
    # Flow rate is assumed in m^3/s and area in m^2
    velocity = flow_rate / area  # Velocity in m/s
    head = (velocity**2) / (2 * gravity)  # Head in meters
    return head

# Example: Calculate head for a flow rate of 0.02 m^3/s and area of 0.005 m^2
flow_rate_example = 0.02  # Flow rate in m^3/s
area_example = 0.005      # Cross-sectional area in m^2
calculated_head = calculate_head(flow_rate_example, area_example)
print(f"The head for a flow rate of {flow_rate_example} m^3/s and an area of {area_example} m^2 is {calculated_head:.2f} m.")
