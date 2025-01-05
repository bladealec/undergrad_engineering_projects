from mp_api.client import MPRester

# Replace 'your_api_key_here' with your actual Materials Project API key
API_KEY = "your_api_key_here"

def fetch_materials(criteria=None):
    """
    Fetch material data from the Materials Project API.
    :param criteria: Dictionary of filter criteria for materials
    :return: List of material documents
    """
    with MPRester(API_KEY) as mpr:
        # Fetch materials summary data
        if criteria:
            materials = mpr.summary.search(**criteria)
        else:
            materials = mpr.summary.search()
        return materials

def rank_materials(materials, weight_density=1, weight_band_gap=1, weight_formation_energy=1):
    """
    Rank materials based on user-defined weights for properties.
    :param materials: List of material documents
    :param weight_density: Weight for density (higher is better)
    :param weight_band_gap: Weight for band gap (higher is better)
    :param weight_formation_energy: Weight for formation energy (lower is better)
    :return: Sorted list of materials
    """
    def calculate_score(material):
        density = material.density or 0
        band_gap = material.band_gap or 0
        formation_energy = material.energy_above_hull or 0
        
        # Weighted scoring: density and band gap are positive; formation energy is negative
        score = (
            weight_density * density +
            weight_band_gap * band_gap -
            weight_formation_energy * formation_energy
        )
        return score

    # Calculate scores and sort materials
    for material in materials:
        material["score"] = calculate_score(material)
    return sorted(materials, key=lambda x: x["score"], reverse=True)

def main():
    print("Materials Selector Using the Materials Project API")
    print("-" * 50)

    try:
        # Define search criteria (e.g., filter by band gap range)
        criteria = {"band_gap_min": 0.5, "band_gap_max": 3.0}
        
        print("Fetching materials...")
        materials = fetch_materials(criteria)

        if not materials:
            print("No materials found with the specified criteria.")
            return

        # Define property weights
        print("\nSpecify weights for ranking properties (default is 1):")
        weight_density = float(input("Weight for density (higher is better): ") or 1)
        weight_band_gap = float(input("Weight for band gap (higher is better): ") or 1)
        weight_formation_energy = float(input("Weight for formation energy (lower is better): ") or 1)

        # Rank materials
        ranked_materials = rank_materials(
            materials, 
            weight_density=weight_density, 
            weight_band_gap=weight_band_gap, 
            weight_formation_energy=weight_formation_energy
        )

        # Display results
        print("\nTop Materials (Ranked):")
        for idx, material in enumerate(ranked_materials[:10], start=1):
            print(f"{idx}. {material['material_id']} - Score: {material['score']:.2f}")
            print(f"   Density: {material['density']} g/cm³, Band Gap: {material['band_gap']} eV, Formation Energy: {material['energy_above_hull']} eV")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
