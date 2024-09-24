import os

# Step 1: Read sol.txt to extract P LOCATIONS
def read_sol_file(file_path):
    p_locations = set()
    with open(file_path, 'r') as file:
        lines = file.readlines()
        p_start = False
        for line in lines:
            line = line.strip()
            if line == "P LOCATIONS":
                p_start = True
                continue
            if p_start:
                if line.isdigit():
                    p_locations.add(int(line))  # Add location to the set
                else:
                    break  # Stop when location list ends
    return p_locations

# Step 2: Read subarea files to extract subarea information
def read_subarea_file(file_path):
    subarea_mapping = {}
    with open(file_path, 'r') as file:
        next(file)  # Skip the first line (header)
        for line in file:
            parts = line.strip().split(maxsplit=2)
            if len(parts) == 3:
                location = int(parts[0])
                subarea = int(parts[1])
                subarea_mapping[location] = subarea
    return subarea_mapping

# Step 3: Count the unique subareas in the solution
def count_unique_subareas(sol_locations, subarea_mappings):
    unique_subareas = set()
    for location in sol_locations:
        for mapping in subarea_mappings:
            if location in mapping:
                unique_subareas.add(mapping[location])
    return len(unique_subareas)

# Main function
def main():
    # Read P LOCATIONS from sol.txt
    sol_file_path = 'solutions/solution_cinema_p_900.txt'
    p_locations = read_sol_file(sol_file_path)

    # Read all subarea files
    subarea_mappings = []
    DIR='/home/falbuquerque/Documents/projects/Project_PMP/benchmark_cpmp/outputs/PACA_Jul24/'
    subarea_files = ['loc_coverages_arrond_2037.txt', 'loc_coverages_EPCI_2037.txt', 'loc_coverages_canton_2037.txt', 'loc_coverages_commune_2037.txt']  # Add all subarea files here
    for subarea_file in subarea_files:
        subarea_mappings.append(read_subarea_file(DIR+subarea_file))
        # Count unique subareas covered by the solution
        unique_subarea_count = count_unique_subareas(p_locations, subarea_mappings)
        # Extract and print just the subarea name
        subarea_name = subarea_file.split('_')[2]  # Extract the subarea part
        print(subarea_name)
        print(f'Number of unique subareas covered: {unique_subarea_count}')
        print()

# Run the main function
if __name__ == "__main__":
    main()