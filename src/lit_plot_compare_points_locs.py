import os
import re
import csv
import matplotlib.pyplot as plt

# Directory where .out files are located
directory_logs = '/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/savecluster_Literature/2024-06-14_save-cluster/'
# directory = '/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/savecluster_Literature/artificial/'
directory_sols = '/home/falbuquerque/Documents/projects/Project_PMP/large-PMP/data/Literature/solutions_lit/'
loc_coord = '/home/falbuquerque/Documents/projects/Project_PMP/large-PMP/data/Literature/'

# Regex patterns to match the required lines
pattern_filtered_locations = re.compile(r'Filtered (\d+) locations: (.+)')
pattern_instance = re.compile(r'service: (.+)')

def map_group(instance):
    if instance in ['SJC1', 'SJC2', 'SJC3a', 'SJC3b', 'SJC4a', 'SJC4b']:
        return 'group2/'
    if instance in ['p3038_600', 'p3038_700', 'p3038_800', 'p3038_900', 'p3038_1000']:
        return 'group3/'
    if instance in ['spain737_148_1', 'spain737_148_2', 'spain737_74_1', 'spain737_74_2']:
        return 'group4/'
    if instance in ['ali535_005', 'ali535_025', 'ali535_050', 'ali535_100', 'ali535_150', 
                   'fnl4461_0020', 'fnl4461_0100', 'fnl4461_0250', 'fnl4461_0500', 'fnl4461_1000', 
                   'lin318_005', 'lin318_015', 'lin318_040', 'lin318_070', 'lin318_100', 
                   'pr2392_020', 'pr2392_075', 'pr2392_150', 'pr2392_300', 'pr2392_500', 
                   'rl1304_010', 'rl1304_050', 'rl1304_100', 'rl1304_200', 'rl1304_300', 
                   'u724_010', 'u724_030', 'u724_075', 'u724_125', 'u724_200']:
        return 'group5/'

def extract_information(file_path):
    filtered_locations = None
    instance = None
    
    with open(file_path, 'r') as f:
        for line in f:
            # Match filtered locations line
            match_filtered = pattern_filtered_locations.match(line)
            if match_filtered:
                # Extract the number and the locations
                num_locations = int(match_filtered.group(1))
                filtered_locations = match_filtered.group(2).strip().split()
                filtered_locations = list(map(int, filtered_locations))  # Convert strings to integers
            
            # Match instance line
            match_instance = pattern_instance.match(line)
            if match_instance:
                instance = match_instance.group(1).strip()
                
            # If both are found, no need to continue
            if filtered_locations is not None and instance is not None:
                break
    
    return filtered_locations, instance

def find_instance_file(directory, instance):
    # Patterns for finding the instance file
    pattern_solucao = rf'solucao\.{instance}_\d+\.txt'
    pattern_soluOPT = rf'soluOPT\.{instance}_\d+\.txt'
    
    for filename in os.listdir(directory):
        if re.match(pattern_solucao, filename) or re.match(pattern_soluOPT, filename):
            return os.path.join(directory, filename)
    
    return None

def extract_solution_literature(file_path_solutions_lit):
    unique_values = []  # List to store unique values

    with open(file_path_solutions_lit, 'r') as f:
        lines = f.readlines()
        for line in lines:
            values = line.strip().split()
            for value in values:
                try:
                    numeric_value = int(value.strip())  # Convert to int
                    if numeric_value in unique_values:
                        return unique_values  # Return if numeric_value is duplicated
                    else:
                        unique_values.append(numeric_value)  # Add to result list
                except ValueError:
                    pass  # Handle non-numeric values if needed

    return unique_values

def calculate_equal_percentage(filtered_locations, unique_values):
    # Count how many unique values from filtered_locations are also in unique_values
    count_equal = len(set(filtered_locations) & set(unique_values))
    
    # Total number of unique values
    total_unique_values = len(unique_values)
    
    # Calculate percentage
    if total_unique_values > 0:
        percentage_equal = (count_equal / total_unique_values) * 100
    else:
        percentage_equal = 0.0
    
    return percentage_equal

def plot_locations(filtered_locations, unique_values, loc_coord_instance, instance, percentage_equal):
    # Read coordinates file
    coords = {}
    cust_weights = {}
    with open(loc_coord_instance, 'r') as f:
        next(f)  # Skip the header line
        for line in f:
            values = line.strip().split()
            try:
                loc_id = int(values[0])
                cust_weights[loc_id] = float(values[1])
                coords[loc_id] = (float(values[2]), float(values[3]))  # Coord_x, Coord_y
            except ValueError:
                pass  # Skip invalid lines
    
    # Prepare data for plotting
    all_coords = list(coords.values())
    filtered_coords = [coords[loc] for loc in filtered_locations if loc in coords]
    unique_coords = [coords[loc] for loc in unique_values if loc in coords]
    unique_only_coords = [coords[loc] for loc in unique_values if loc not in filtered_locations and loc in coords]

    all_x, all_y = zip(*all_coords) if all_coords else ([], [])
    filtered_x, filtered_y = zip(*filtered_coords) if filtered_coords else ([], [])
    unique_x, unique_y = zip(*unique_coords) if unique_coords else ([], [])
    unique_only_x, unique_only_y = zip(*unique_only_coords) if unique_only_coords else ([], [])

    # Convert tuples to lists for concatenation
    all_x, all_y = list(all_x), list(all_y)
    filtered_x, filtered_y = list(filtered_x), list(filtered_y)
    unique_x, unique_y = list(unique_x), list(unique_y)
    unique_only_x, unique_only_y = list(unique_only_x), list(unique_only_y)

    # Determine axis limits
    delta = 0.05
    x_min = min(all_x + filtered_x + unique_x + unique_only_x) - delta * min(all_x + filtered_x + unique_x + unique_only_x)
    x_max = max(all_x + filtered_x + unique_x + unique_only_x) + delta * max(all_x + filtered_x + unique_x + unique_only_x)
    y_min = min(all_y + filtered_y + unique_y + unique_only_y) - delta * min(all_y + filtered_y + unique_y + unique_only_y)
    y_max = max(all_y + filtered_y + unique_y + unique_only_y) + delta * max(all_y + filtered_y + unique_y + unique_only_y)

    # Create subplots
    fig, axs = plt.subplots(1, 3, figsize=(22, 7))

    # Plot all locations
    axs[0].scatter(all_x, all_y, c='gray', label=f'{instance} - All Locations')
    axs[0].set_title(f'All Locations ({len(all_coords)})')
    axs[0].set_xlabel('Coord_x')
    axs[0].set_ylabel('Coord_y')
    axs[0].legend()
    axs[0].set_xlim(x_min, x_max)
    axs[0].set_ylim(y_min, y_max)

    # Plot filtered locations
    axs[1].scatter(filtered_x, filtered_y, c='blue', label=f'{instance} - Voted Locations')
    axs[1].set_title(f'Filtered Locations ({len(filtered_coords)})')
    axs[1].set_xlabel('Coord_x')
    axs[1].set_ylabel('Coord_y')
    axs[1].legend()
    axs[1].set_xlim(x_min, x_max)
    axs[1].set_ylim(y_min, y_max)

    # Plot unique locations
    axs[2].scatter(unique_x, unique_y, c='red', label=f'{instance} - Solution')
    axs[2].scatter(unique_only_x, unique_only_y, c='green', label=f'{instance} - Solution Only')
    axs[2].set_title(f'Unique Locations ({len(unique_coords)}) - Hit Rate: {percentage_equal:.2f}%')
    axs[2].set_xlabel('Coord_x')
    axs[2].set_ylabel('Coord_y')
    axs[2].legend()
    axs[2].set_xlim(x_min, x_max)
    axs[2].set_ylim(y_min, y_max)

    # Show plots
    plt.tight_layout()
    plt.savefig(f'./outputs/comparative_points_locs/{instance}_locations_plot.png')
    plt.show()

def process_out_files(directory_logs):

    # create a filter to instances names to be processed
    # filter_instances = ['SJC1', 'SJC2', 'SJC3a', 'SJC3b', 'SJC4a', 'SJC4b']
    # filter_instances = ['pr2392_020', 'pr2392_075', 'pr2392_150', 'pr2392_300', 'pr2392_500']
    filter_instances = ['pr2392_075']


    for filename in os.listdir(directory_logs):
        if filename.endswith(".out"):
            file_path = os.path.join(directory_logs, filename)
            filtered_locations, instance = extract_information(file_path)
            
            if filtered_locations and instance and instance in filter_instances:
                print(f"File: {filename}")
                print(f"Number of filtered locations: {len(filtered_locations)}")
                print(f"instance: {instance}")
                
                # Find and open the corresponding instance file
                file_path_solutions_lit = find_instance_file(directory_sols, instance)
                if file_path_solutions_lit:
                    solution_literature = extract_solution_literature(file_path_solutions_lit)
                    print(f"Number of unique values found: {len(solution_literature)}")
                    
                    # Calculate percentage of equal values
                    percentage_equal = calculate_equal_percentage(filtered_locations, solution_literature)
                    print(f"Percentage of equal values: {percentage_equal:.2f}%")

                    # Get coordinates from a file txt
                    coord_filename = f'cust_weights_{instance}.txt'
                    # Directory depends on the instance name
                    group = map_group(instance)
                    loc_coord_instance = os.path.join(loc_coord, group, coord_filename)

                    # Plot the locations
                    plot_locations(filtered_locations, solution_literature, loc_coord_instance, instance, percentage_equal)

                else:
                    print(f"No instance file found for instance: {instance}")
                
                print("--------------------------------")

# Example usage
process_out_files(directory_logs)
