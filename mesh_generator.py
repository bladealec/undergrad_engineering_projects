import numpy as np
import matplotlib.pyplot as plt

# Define the size of the beam
length = 10  # Length of the beam (in meters)
width = 1    # Width of the beam (in meters)

# Define how many nodes we want in each direction (along the length and width)
num_nodes_x = 11  # Number of nodes in the x-direction (along the length)
num_nodes_y = 2   # Number of nodes in the y-direction (along the width)

# Choose the type of elements for the mesh (we'll use quadrilateral elements here)
element_type = 'quad'  # 'quad' for quadrilateral, 'tri' for triangular elements

# Define material properties (using values for steel here)
E = 210e9  # Young's modulus (a measure of stiffness) in Pascals (Pa) for Steel
nu = 0.3   # Poisson's ratio (describes the ratio of lateral strain to axial strain)

# Generate the node coordinates (position of the nodes in the grid)
x = np.linspace(0, length, num_nodes_x)  # Nodes along the length of the beam
y = np.linspace(0, width, num_nodes_y)   # Nodes along the width of the beam

# Create a list of nodes by combining the x and y coordinates
nodes = np.array([[i, j] for i in x for j in y])

# Now, we create the elements (each element connects four nodes in a quadrilateral shape)
elements = []
for i in range(num_nodes_x - 1):  # Loop over each row of nodes
    for j in range(num_nodes_y - 1):  # Loop over each column of nodes
        # Define the four nodes that make up a quadrilateral element
        n1 = i * num_nodes_y + j
        n2 = (i + 1) * num_nodes_y + j
        n3 = (i + 1) * num_nodes_y + (j + 1)
        n4 = i * num_nodes_y + (j + 1)
        elements.append([n1, n2, n3, n4])  # Store each element's node indices

# Convert the lists of nodes and elements into numpy arrays for easier handling
nodes = np.array(nodes)
elements = np.array(elements)

# Function to plot the mesh and visualize the nodes and elements
def plot_mesh():
    plt.figure(figsize=(10, 5))  # Create a figure with a specific size
    for element in elements:  # Loop through each element
        # Get the coordinates of the nodes that make up the element
        node_coords = nodes[element, :]
        # Draw the element as a polygon (each element is a quadrilateral)
        polygon = plt.Polygon(node_coords, edgecolor='k', facecolor='none')
        plt.gca().add_patch(polygon)  # Add the polygon to the plot

    # Plot the nodes as red dots
    plt.scatter(nodes[:, 0], nodes[:, 1], color='red', marker='o')
    plt.xlim([0, length])  # Set the limits of the x-axis
    plt.ylim([0, width])  # Set the limits of the y-axis
    plt.xlabel('X (m)')  # Label for the x-axis
    plt.ylabel('Y (m)')  # Label for the y-axis
    plt.title('FEA Mesh')  # Title of the plot
    plt.show()  # Show the plot

# Call the function to plot the mesh
plot_mesh()

# Apply boundary conditions: Fix the left side of the beam (where x = 0)
# In this case, we apply fixed supports at all nodes where x = 0
fixed_nodes = nodes[nodes[:, 0] == 0]

# Define the boundary conditions (displacement is zero at the fixed nodes)
boundary_conditions = {}
for i, node in enumerate(fixed_nodes):
    boundary_conditions[node[0]] = {'ux': 0, 'uy': 0}  # No displacement in x and y directions

# Print out the boundary conditions for the fixed nodes
print(f"Boundary conditions (Fixed at x=0): {boundary_conditions}")

# Save the mesh data to a text file so it can be used in a solver later
def save_mesh_to_file(filename):
    with open(filename, 'w') as f:  # Open the file in write mode
        f.write("Nodes\n")  # Start by writing the header for the nodes section
        for node in nodes:
            # Write the x and y coordinates of each node
            f.write(f"{node[0]} {node[1]}\n")

        f.write("\nElements\n")  # Write the header for the elements section
        for element in elements:
            # Write the indices of the nodes for each element
            f.write(" ".join(map(str, element)) + "\n")

# Save the mesh data to a file called 'mesh.txt'
save_mesh_to_file('mesh.txt')
print("Mesh saved to 'mesh.txt'")
