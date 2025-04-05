import numpy as np
import random
import matplotlib.pyplot as plt

# Constants for the material and loading conditions
material_density = 7.85  # g/cm^3 for steel
yield_stress = 250  # MPa for steel
E = 210000  # Young's Modulus in MPa (for steel)
applied_load = 1000  # Applied load in Newtons
max_deflection = 1  # Maximum allowed deflection in cm

# Beam properties
def beam_weight(length, width, height):
    """ Calculate weight of the beam (volume * material_density) """
    volume = length * width * height  # cm^3
    weight = volume * material_density  # g
    return weight

def beam_bending_stress(length, width, height):
    """ Calculate bending stress using formula: sigma = M / S
        M = Applied load * length / 4 (simply supported beam, center load)
        S = Section Modulus (width * height^2 / 6)
    """
    M = applied_load * length / 4  # Moment in Nm (converted from cm)
    S = (width * height**2) / 6  # Section modulus in cm^3
    bending_stress = M / S  # in MPa (Stress = Moment / Section Modulus)
    return bending_stress

def beam_deflection(length, width, height):
    """ Calculate deflection using the formula: delta = 5 * P * L^3 / (384 * E * I)
        I = (width * height^3) / 12  (Moment of inertia)
    """
    I = (width * height**3) / 12  # Moment of inertia in cm^4
    deflection = (5 * applied_load * length**3) / (384 * E * I)  # Deflection in cm
    return deflection

def fitness_function(individual):
    """ Fitness function for genetic algorithm: Minimize weight, subject to constraints on stress and deflection """
    length, width, height = individual
    weight = beam_weight(length, width, height)
    stress = beam_bending_stress(length, width, height)
    deflection = beam_deflection(length, width, height)

    # Penalty for stress exceeding yield stress
    stress_penalty = max(0, stress - yield_stress) * 1000  # High penalty for excessive stress

    # Penalty for deflection exceeding the maximum allowed deflection
    deflection_penalty = max(0, deflection - max_deflection) * 1000  # High penalty for excessive deflection

    # Total fitness: Minimize weight and add penalties for violations
    fitness = weight + stress_penalty + deflection_penalty
    return fitness

# Genetic Algorithm Functions
def create_individual():
    """ Create a random individual [length, width, height] within reasonable bounds """
    length = random.uniform(50, 300)  # length in cm
    width = random.uniform(5, 20)  # width in cm
    height = random.uniform(5, 20)  # height in cm
    return [length, width, height]

def crossover(parent1, parent2):
    """ One-point crossover between two parents """
    crossover_point = random.randint(1, 2)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutate(individual):
    """ Mutate an individual by changing one of the design variables """
    mutation_index = random.randint(0, 2)
    if mutation_index == 0:
        individual[mutation_index] = random.uniform(50, 300)  # length mutation
    elif mutation_index == 1:
        individual[mutation_index] = random.uniform(5, 20)  # width mutation
    else:
        individual[mutation_index] = random.uniform(5, 20)  # height mutation
    return individual

def selection(population, fitness_values):
    """ Tournament selection: Pick the best two individuals """
    tournament_size = 3
    selected_parents = []
    for _ in range(2):
        tournament = random.sample(list(zip(population, fitness_values)), tournament_size)
        tournament.sort(key=lambda x: x[1])  # Sort by fitness value
        selected_parents.append(tournament[0][0])
    return selected_parents

# Genetic Algorithm
def genetic_algorithm(pop_size=100, generations=200, mutation_rate=0.1):
    # Initialize population
    population = [create_individual() for _ in range(pop_size)]
    
    # Evolve over generations
    best_fitness = float('inf')
    best_individual = None
    fitness_history = []

    for generation in range(generations):
        fitness_values = [fitness_function(ind) for ind in population]
        
        # Track best individual
        current_best_fitness = min(fitness_values)
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_individual = population[fitness_values.index(current_best_fitness)]
        
        fitness_history.append(best_fitness)

        # Select the best individuals to reproduce
        new_population = []
        for _ in range(pop_size // 2):
            parent1, parent2 = selection(population, fitness_values)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)

            # Mutate children
            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)
            
            new_population.extend([child1, child2])
        
        population = new_population

    return best_individual, best_fitness, fitness_history

# Run the genetic algorithm
best_individual, best_fitness, fitness_history = genetic_algorithm()

# Results
print(f"Optimal Design (Length, Width, Height): {best_individual}")
print(f"Optimal Weight: {best_fitness:.2f} g")

# Plotting Fitness History (Convergence)
plt.plot(fitness_history)
plt.xlabel('Generation')
plt.ylabel('Best Fitness (Weight + Penalties)')
plt.title('Genetic Algorithm Convergence')
plt.grid(True)
plt.show()
