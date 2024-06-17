import os
import re
import csv
import matplotlib.pyplot as plt
import numpy as np

# Directory where .out files are located
# directory_logs = '/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/savecluster_Literature/2024-06-14_save-cluster/'
directory_logs =  '/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/savecluster_Literature/2024-06-13_save-cluster/'
# directory = '/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/savecluster_Literature/artificial/'
directory_sols_lit = '/home/falbuquerque/Documents/projects/Project_PMP/large-PMP/data/Literature/solutions_lit/'
directory_sols_method = '/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/savecluster_Literature/2024-06-13_save-cluster/outputs/solutions/2024-06-12_LIT/Assignments/'
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

def extract_p_locs_literature(file_path_solutions_lit):
    sol_values = []  # List to store unique values

    with open(file_path_solutions_lit, 'r') as f:
        lines = f.readlines()
        for line in lines:
            values = line.strip().split()
            for value in values:
                try:
                    numeric_value = int(value.strip())  # Convert to int
                    if numeric_value in sol_values:
                        return sol_values  # Return if numeric_value is duplicated
                    else:
                        sol_values.append(numeric_value)  # Add to result list
                except ValueError:
                    pass  # Handle non-numeric values if needed

    return sol_values

def extract_solution_method(file_path_solutions_method, instance):
    # Extract p_value from the instance string
    p_value = int(instance.split('_')[1])

    # Define the method and file path
    METHOD = 'RSSV_EXACT_CPMP_BIN'
    file_name = f'test_lit_{instance}_p_{p_value}_{METHOD}.txt'
    file_path = f'{file_path_solutions_method}/{file_name}'

    # Initialize a list to store the P LOCATIONS
    p_locations = []

    # Read the file and extract the P LOCATIONS section
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        # Flag to start reading P LOCATIONS
        p_locations_section = False
        
        for line in lines:
            stripped_line = line.strip()
            if stripped_line == "P LOCATIONS":
                p_locations_section = True
            elif stripped_line == "LOCATION USAGES":
                break
            elif p_locations_section:
                # Add location to the list if the line is not empty
                if stripped_line:
                    try:
                        p_locations.append(int(stripped_line))
                    except ValueError:
                        print(f"Skipping invalid line: {stripped_line}")

    return p_locations

def calculate_equal_percentage(filtered_locations, sol_values):
    # Count how many unique values from filtered_locations are also in sol_values
    count_equal = len(set(filtered_locations) & set(sol_values))
    
    # Total number of unique values
    total_sol_values = len(sol_values)
    
    # Calculate percentage
    if total_sol_values > 0:
        percentage_equal = (count_equal / total_sol_values) * 100
    else:
        percentage_equal = 0.0
    
    return percentage_equal

def plot_locations(filtered_locations, sol_values_lit, solution_method, loc_coord_instance, instance, percentage_equal, interval_size=10):
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
    solution_lit_coords = [coords[loc] for loc in sol_values_lit if loc in coords]
    solution_lit_only_coords = [coords[loc] for loc in sol_values_lit if loc not in filtered_locations and loc in coords]
    solution_method_coords = [coords[loc] for loc in solution_method if loc in coords]
    solution_method_only_coords = [coords[loc] for loc in solution_method if loc not in sol_values_lit and loc in coords]

    all_x, all_y = zip(*all_coords) if all_coords else ([], [])
    filtered_x, filtered_y = zip(*filtered_coords) if filtered_coords else ([], [])
    unique_x, unique_y = zip(*solution_lit_coords) if solution_lit_coords else ([], [])
    unique_only_x, unique_only_y = zip(*solution_lit_only_coords) if solution_lit_only_coords else ([], [])
    solution_method_x, solution_method_y = zip(*solution_method_coords) if solution_method_coords else ([], [])
    solution_method_only_x, solution_method_only_y = zip(*solution_method_only_coords) if solution_method_only_coords else ([], [])

    # Convert tuples to lists for concatenation
    all_x, all_y = list(all_x), list(all_y)
    filtered_x, filtered_y = list(filtered_x), list(filtered_y)
    unique_x, unique_y = list(unique_x), list(unique_y)
    unique_only_x, unique_only_y = list(unique_only_x), list(unique_only_y)
    solution_method_x, solution_method_y = list(solution_method_x), list(solution_method_y)
    solution_method_only_x, solution_method_only_y = list(solution_method_only_x), list(solution_method_only_y)

    # Determine axis limits
    delta = 0.05
    x_min = min(all_x + filtered_x + unique_x + unique_only_x + solution_method_x) - delta * min(all_x + filtered_x + unique_x + unique_only_x + solution_method_x)
    x_max = max(all_x + filtered_x + unique_x + unique_only_x + solution_method_x) + delta * max(all_x + filtered_x + unique_x + unique_only_x + solution_method_x)
    y_min = min(all_y + filtered_y + unique_y + unique_only_y + solution_method_y) - delta * min(all_y + filtered_y + unique_y + unique_only_y + solution_method_y)
    y_max = max(all_y + filtered_y + unique_y + unique_only_y + solution_method_y) + delta * max(all_y + filtered_y + unique_y + unique_only_y + solution_method_y)


    # Create subplots
    fig, axs = plt.subplots(2, 3, figsize=(22, 14))

    # Plot all locations
    axs[0, 0].scatter(all_x, all_y, c='gray', alpha=0.6, label=f'{instance} - All Locations')
    axs[0, 0].set_title(f'All Locations ({len(all_coords)})')
    axs[0, 0].set_xlabel('Coord_x')
    axs[0, 0].set_ylabel('Coord_y')
    axs[0, 0].legend()
    axs[0, 0].set_xlim(x_min, x_max)
    axs[0, 0].set_ylim(y_min, y_max)

    # Plot filtered locations
    axs[0, 1].scatter(filtered_x, filtered_y, c='blue', alpha=0.6, label=f'{instance} - Voted Locations')
    axs[0, 1].set_title(f'Filtered Locations ({len(filtered_coords)})')
    axs[0, 1].set_xlabel('Coord_x')
    axs[0, 1].set_ylabel('Coord_y')
    axs[0, 1].legend()
    axs[0, 1].set_xlim(x_min, x_max)
    axs[0, 1].set_ylim(y_min, y_max)

    # Plot unique locations
    axs[0, 2].scatter(unique_x, unique_y, c='green', alpha=0.6, label=f'{instance} - Solution')
    axs[0, 2].scatter(unique_only_x, unique_only_y, c='red', alpha=0.6, label=f'{instance} - Solution Only')
    axs[0, 2].set_title(f'Solution Literature ({len(solution_lit_coords)}) - Hit Rate: {percentage_equal:.2f}%')
    axs[0, 2].set_xlabel('Coord_x')
    axs[0, 2].set_ylabel('Coord_y')
    axs[0, 2].legend()
    axs[0, 2].set_xlim(x_min, x_max)
    axs[0, 2].set_ylim(y_min, y_max)

    # Add heatmap overlay on the first plot (all locations)
    if cust_weights:
        # Prepare heatmap data
        heatmap_data = np.zeros_like(all_x, dtype=float)
        for loc_id, weight in cust_weights.items():
            if loc_id in coords:
                idx = list(coords.keys()).index(loc_id)
                heatmap_data[idx] = weight

        # Normalize heatmap data for color intensity
        normalized_heatmap_data = (heatmap_data - np.min(heatmap_data)) / (np.max(heatmap_data) - np.min(heatmap_data))

        # Scatter plot with normalized color intensity
        sc = axs[1, 0].scatter(all_x, all_y, c=normalized_heatmap_data, cmap='hot', alpha=0.6)

        # Add colorbar based on the same normalization
        cbar = plt.colorbar(sc, ax=axs[1, 0], label='Normalized Weight')

    # Calculate cumulative matches
    intervals = range(0, len(filtered_locations) + interval_size, interval_size)
    cumulative_matches = [len(set(filtered_locations[:i]) & set(sol_values_lit)) for i in intervals]

    # Plot cumulative matches
    axs[1, 1].bar(intervals, cumulative_matches, width=interval_size, align='edge', color='purple', alpha=0.6)
    axs[1, 1].set_title(f'Cumulative Matches ({cumulative_matches[-1]})')
    axs[1, 1].set_xlabel('Number of Filtered Locations')
    axs[1, 1].set_ylabel('Number of Matches')
    axs[1, 1].set_xlim(0, intervals[-1])
    axs[1, 1].set_ylim(0, max(cumulative_matches) + 1)

    # Plot histogram of weights
    # if cust_weights:
    #     weights = list(cust_weights.values())
    #     axs[1, 2].hist(weights, bins=20, color='orange', alpha=0.6)
    #     axs[1, 2].set_title(f'Weights Histogram')
    #     axs[1, 2].set_xlabel('Weight')
    #     axs[1, 2].set_ylabel('Frequency')

    #plot solution method

    # Plot solution method locations
    axs[1, 2].scatter(solution_method_x, solution_method_y, c='black', alpha=0.6, label=f'{instance} - Intersection with Sol Lit')
    axs[1, 2].scatter(solution_method_only_x, solution_method_only_y, c='orange', alpha=0.6, label=f'{instance} - Solution Method Only')
    axs[1, 2].set_title(f'Solution Method Locations ({len(solution_method_coords)}) | Instersection: {len(set(solution_method) & set(sol_values_lit))}')
    axs[1, 2].set_xlabel('Coord_x')
    axs[1, 2].set_ylabel('Coord_y')
    axs[1, 2].legend()
    axs[1, 2].set_xlim(x_min, x_max)
    axs[1, 2].set_ylim(y_min, y_max)


    # Adjust layout to fit the new subplot
    plt.tight_layout()
    plt.savefig(f'./outputs/comparative_points_locs/{instance}_locations_plot.png')
    plt.show()

def process_out_files(directory_logs):

    # create a filter to instances names to be processed
    # filter_instances = ['SJC1', 'SJC2', 'SJC3a', 'SJC3b', 'SJC4a', 'SJC4b']
    filter_instances = ['pr2392_020', 'pr2392_075', 'pr2392_150', 'pr2392_300', 'pr2392_500']
    # filter_instances = ['pr2392_075']


    for filename in os.listdir(directory_logs):
        if filename.endswith(".out"):
            file_path = os.path.join(directory_logs, filename)
            filtered_locations, instance = extract_information(file_path)
            


            if filtered_locations and instance and instance in filter_instances:
                print(f"File: {filename}")
                print(f"Number of filtered locations: {len(filtered_locations)}")
                # print(f"Filtered locations: {filtered_locations}")
                print(f"instance: {instance}")
                
                # Find and open the corresponding instance file
                file_path_solutions_lit = find_instance_file(directory_sols_lit, instance)
                if file_path_solutions_lit:
                    p_locs_literature = extract_p_locs_literature(file_path_solutions_lit)
                    print(f"Number of unique values found: {len(p_locs_literature)}")
                    
                    # Calculate percentage of equal values
                    percentage_equal = calculate_equal_percentage(filtered_locations, p_locs_literature)
                    print(f"Percentage of equal values: {percentage_equal:.2f}%")

                    # Get coordinates from a file txt
                    coord_filename = f'cust_weights_{instance}.txt'
                    # Directory depends on the instance name
                    group = map_group(instance)
                    loc_coord_instance = os.path.join(loc_coord, group, coord_filename)

                    # get solutions from method
                    p_locs_method = extract_solution_method(directory_sols_method,instance)


                    # print p locs
                    # print(f'P locs solution literature: {p_locs_literature}')
                    # print('-------------------')
                    # print(f'P locs solution method: {p_locs_method}')

                    # num elements intersection of p_locs_literature and p_locs_method
                    print(f'Number of elements in intersection solutions: {len(set(p_locs_literature) & set(p_locs_method))}')
                    # list elements in intersection of p_locs_literature and p_locs_method
                    # print(f'Elements in intersection: {list(set(p_locs_literature) & set(p_locs_method))}')


                    # Plot the locations
                    plot_locations(filtered_locations, p_locs_literature, p_locs_method, loc_coord_instance, instance, percentage_equal)

                else:
                    print(f"No instance file found for instance: {instance}")
                
                print("--------------------------------")

# Example usage
process_out_files(directory_logs)
