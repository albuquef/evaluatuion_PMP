import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def read_distances_from_file(file_path):
    distances = {}
    with open(file_path, 'r') as file:
        next(file)  # Skip header if present
        for line in file:
            cust, loc, distance = line.strip().split()
            cust = int(cust)
            loc = int(loc)
            distance = float(distance)
            if cust not in distances:
                distances[cust] = {}
            distances[cust][loc] = distance
    return distances

def dist(cust, loc):
    # Replace 'distances.txt' with your actual file path
    distances = read_distances_from_file('/home/felipe/Documents/Projects/GeoAvigon/pmp_code/large-PMP/data/filterData_PACA_may23/dist_matrix_minutes.txt')
    if cust in distances and loc in distances[cust]:
        return distances[cust][loc]
    else:
        return None  # Handle case where (cust, loc) pair is not found

def extract_data_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract the "Objective" value
    objective_str = content.split('OBJECTIVE\n')[1].split('\n')[0].strip()
    objective = float(objective_str)

    # Extract "P LOCATIONS"
    p_locations_str = content.split('P LOCATIONS\n')[1].split('\n\n')[0].strip()
    p_locations = list(map(int, p_locations_str.split('\n')))
    p_locations_size = len(p_locations)

    # Extract "CUSTOMER ASSIGNMENTS"
    customer_assignments_str = content.split('CUSTOMER ASSIGNMENTS\n')[1].strip()
    customer_assignments_lines = customer_assignments_str.split('\n')
    customer_assignments = {}
    
    # print("Customer Assignments Lines:")
    # print(customer_assignments_lines)  # Debug print
    
    for line in customer_assignments_lines:
        if ' -> ' in line:
            customer_part, location_part = line.split(' -> ')
            try:
                customer = int(customer_part.split('(')[0].strip())
                
                # Split multiple assignments correctly
                location_assignments = location_part.split(') ')
                for assignment in location_assignments:
                    assignment = assignment.strip()
                    if not assignment:
                        continue
                    location_str, assigned_demand_str = assignment.split(' (')
                    location = int(location_str.strip())
                    assigned_demand = float(assigned_demand_str.strip(')'))
                    usage = assigned_demand  # Assuming usage is the assigned demand for simplicity
                    customer_assignments[(customer, location)] = usage
                
                # print(f"Parsed: Customer {customer}, Assignments {customer_assignments}")  # Debug print
            except ValueError as e:
                # Print the error and the line causing it for debugging
                # print(f"ValueError: {e} for line: {line}")  # Debug print
                # Skip lines that cannot be parsed
                continue
    
    # print(f"Final Customer Assignments: {customer_assignments}")  # Debug print

    return objective, p_locations, p_locations_size, customer_assignments

def read_all_files_in_directory(directory_path):
    file_paths = glob.glob(os.path.join(directory_path, '*.txt'))
    all_data = []
    for file_path in file_paths:
        data = extract_data_from_file(file_path)
        all_data.append(data)
    return all_data

def plot_objectives_vs_p_locations(data):
    objectives = [item[0] for item in data]
    p_locations_sizes = [item[2] for item in data]
    # order data by p_locations_sizes
    objectives = [x for _, x in sorted(zip(p_locations_sizes, objectives))]
    p_locations_sizes = sorted(p_locations_sizes)
    plt.figure(figsize=(10, 6))
    plt.scatter(p_locations_sizes, objectives, color='blue')
    plt.xlabel('Number of P LOCATIONS')
    plt.xticks(p_locations_sizes)
    plt.ylabel('Objective Values')
    plt.title('Objective Values vs. Size of P LOCATIONS')
    plt.grid(True)
    plt.show()

def plot_objectives_vs_p_locations(data_vectors, colors, legends):
    
    np.random.seed(0)  # Set seed for reproducibility
    
    plt.figure(figsize=(10, 6))

    for i, data in enumerate(data_vectors):
        objectives = [item[0] for item in data]
        p_locations_sizes = [item[2] for item in data]

        # Generate jitter values
        jitter = np.random.normal(scale=0.01, size=len(p_locations_sizes))

        # Add jitter to x-coordinates
        p_locations_sizes_jittered = [x + jitter[idx] for idx, x in enumerate(p_locations_sizes)]

        # Sort based on jittered p_locations_sizes
        sorted_indices = np.argsort(p_locations_sizes_jittered)
        p_locations_sizes_sorted = [p_locations_sizes_jittered[idx] for idx in sorted_indices]
        objectives_sorted = [objectives[idx] for idx in sorted_indices]

        label = legends[i]
        plt.scatter(p_locations_sizes_sorted, objectives_sorted, color=colors[i], label=label)

    rounded_p_locations_sizes = [round(x) for x in p_locations_sizes_sorted]
    plt.xticks(rounded_p_locations_sizes)
    plt.xlabel('Number of p')
    plt.ylabel('Objective Values')
    plt.title('Objectives values with different number of p locations')
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_violin_dist_weights(data_vectors, colors, legends, pvalue):
    # Read distances from file
    distances = read_distances_from_file('/home/felipe/Documents/Projects/GeoAvigon/pmp_code/large-PMP/data/filterData_PACA_may23/dist_matrix_minutes.txt')
    
    all_weights = []
    
    for i, data in enumerate(data_vectors):
        # Ensure filtered_data has exactly one item
        filtered_data = [item for item in data if item[2] == pvalue]
        
        if len(filtered_data) != 1:
            raise ValueError(f"Filtered data for dataset {i} does not have exactly one item.")
        
        _, _, _, customer_assignments = filtered_data[0]


        all_products = []
        for (cust, loc), usage in customer_assignments.items():
            # Compute distance
            if cust in distances and loc in distances[cust]:
                distance = distances[cust][loc]
            else:
                raise ValueError(f"Distance not found for customer {cust} and location {loc}.")
            
            # Compute product
            product = usage * distance
            all_products.append(product)
            
        all_products = list(all_products)
        # Append to all_weights
        all_weights.append(all_products)

    # Create a DataFrame if not already in this format
    df = pd.DataFrame(all_weights).transpose()
    df.columns = legends

    # Plot violin plot
    plt.figure(figsize=(12, 8))
    sns.violinplot(data=df, palette=colors)  # Use colors specified in the palette
    
    # Create custom legend handles and labels
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in colors]
    legend_labels = legends[:len(colors)]  # Ensure legend labels match the number of colors

    # Add legend
    plt.legend(legend_handles, legend_labels, title='Datasets')
    
    plt.xlabel('Dataset')
    plt.ylabel('Usage*Dist Values')
    plt.title('Usage*Dist Values Distribution per Dataset')

    plt.tight_layout()
    plt.show()

def plot_sol_and_violin(data_vectors, colors, legends,pvalue):
    np.random.seed(0)  # Set seed for reproducibility
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))  # Create a figure with two subplots
    
    for i, data in enumerate(data_vectors):
        objectives = [item[0] for item in data]
        p_locations_sizes = [item[2] for item in data]

        # Generate jitter values
        jitter = np.random.normal(scale=0.01, size=len(p_locations_sizes))

        # Add jitter to x-coordinates
        p_locations_sizes_jittered = [x + jitter[idx] for idx, x in enumerate(p_locations_sizes)]

        # Sort based on jittered p_locations_sizes
        sorted_indices = np.argsort(p_locations_sizes_jittered)
        p_locations_sizes_sorted = [p_locations_sizes_jittered[idx] for idx in sorted_indices]
        objectives_sorted = [objectives[idx] for idx in sorted_indices]

        label = legends[i]
        ax1.scatter(p_locations_sizes_sorted, objectives_sorted, color=colors[i], label=label)

    rounded_p_locations_sizes = [round(x) for x in p_locations_sizes_sorted]
    ax1.set_xticks(rounded_p_locations_sizes)
    ax1.set_xlabel('Number of p')
    ax1.set_ylabel('Objective Values')
    ax1.set_title('Objectives values with different number of p locations')
    ax1.grid(True)
    ax1.legend()

    # Plot violin plot in the second subplot
    plot_violin_dist_weights_ax(data_vectors, colors, legends, pvalue=pvalue, ax=ax2)

    plt.tight_layout()
    plt.savefig('plots/plots_paca/objectives_vs_violin.pdf')
    plt.show()

def plot_violin_dist_weights_ax(data_vectors, colors, legends, pvalue, ax=None):

    # Read distances from file
    distances = read_distances_from_file('/home/felipe/Documents/Projects/GeoAvigon/pmp_code/large-PMP/data/filterData_PACA_may23/dist_matrix_minutes.txt')

    all_weights = []

    for i, data in enumerate(data_vectors):
        # Ensure filtered_data has exactly one item
        filtered_data = [item for item in data if item[2] == pvalue]

        if len(filtered_data) != 1:
            raise ValueError(f"Filtered data for dataset {i} does not have exactly one item.")

        _, _, _, customer_assignments = filtered_data[0]

        all_products = []
        for (cust, loc), usage in customer_assignments.items():
            # Compute distance
            if cust in distances and loc in distances[cust]:
                distance = distances[cust][loc]
            else:
                raise ValueError(f"Distance not found for customer {cust} and location {loc}.")

            # Compute product
            product = usage * distance
            all_products.append(product)

        all_weights.append(all_products)

    # Create a DataFrame
    df = pd.DataFrame(all_weights).transpose()
    df.columns = legends

    # If ax is None, create a new figure and axis
    if ax is None:
        plt.figure(figsize=(12, 8))
        ax = plt.gca()

    # Plot violin plot
    sns.violinplot(data=df, palette=colors, ax=ax)

    # Create custom legend handles and labels
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in colors]
    legend_labels = legends[:len(colors)]  # Ensure legend labels match the number of colors

    # Add legend
    ax.legend(legend_handles, legend_labels, title='Datasets')

    ax.set_xlabel('Dataset')
    ax.set_ylabel('Usage*Dist Values')
    ax.set_title('Usage*Dist Values Distribution per Dataset')





# without coverages
directory_path_mat = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_Tests_Cyrille/Cyrille/distr_pop/original/outputs/solutions/2024-07-01_PACA/Assignments/mat/'
directory_path_poste = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_Tests_Cyrille/Cyrille/distr_pop/original/outputs/solutions/2024-07-01_PACA/Assignments/poste/'

# without coverages diff weights
directory_path_mat_weight_shuffled = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_Tests_Cyrille/Cyrille/distr_pop/shuffle/outputs/solutions/2024-07-02_PACA_weight_shuffled/Assignments/mat/'
directory_path_mat_weight_split = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_Tests_Cyrille/Cyrille/distr_pop/split/outputs/solutions/2024-07-02_PACA/Assignments/mat/'
directory_path_poste_weight_shuffled = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_Tests_Cyrille/Cyrille/distr_pop/shuffle/outputs/solutions/2024-07-02_PACA_weight_shuffled/Assignments/poste/'
directory_path_poste_weight_split = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_Tests_Cyrille/Cyrille/distr_pop/split/outputs/solutions/2024-07-02_PACA/Assignments/poste/'



# Specify the directory containing the .txt files
directory_path_multiechelle_poste = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_Tests_Cyrille/Cyrille/multiechelles/outputs/solutions/2024-07-02_PACA_multiechelles/Assignments/poste/'
directory_path_multiechelle_mat = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_Tests_Cyrille/Cyrille/multiechelles/outputs/solutions/2024-07-02_PACA_multiechelles/Assignments/mat/'
# mutiechelle mat = (arrond + canton) | multi echelle poste = (canton + commune)

# Original covers
directory_path_mat_cover_arrond = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_save_cluster/Cyrille/decoupages/original/outputs/solutions/2024-07-02_PACA/Assignments/mat_cover_arrond/'
directory_path_mat_cover_EPCI = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_save_cluster/Cyrille/decoupages/original/outputs/solutions/2024-07-02_PACA/Assignments/mat_cover_EPCI/'
directory_path_mat_cover_canton = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_save_cluster/Cyrille/decoupages/original/outputs/solutions/2024-07-02_PACA/Assignments/mat_cover_canton/'
directory_path_poste_cover_canton = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_save_cluster/Cyrille/decoupages/original/outputs/solutions/2024-07-02_PACA/Assignments/poste_cover_canton/'
directory_path_poste_cover_commune = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_save_cluster/Cyrille/decoupages/original/outputs/solutions/2024-07-02_PACA/Assignments/poste_cover_commune/'

# kMeans covers
directory_path_mat_cover_kmeans_arrond = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_save_cluster/Cyrille/decoupages/kmeans/outputs/solutions/2024-07-02_PACA/Assignments/mat_cover_kmeans_arrond/'
directory_path_mat_cover_kmeans_EPCI = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_save_cluster/Cyrille/decoupages/kmeans/outputs/solutions/2024-07-02_PACA/Assignments/mat_cover_kmeans_EPCI/'
directory_path_mat_cover_kmeans_canton = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_save_cluster/Cyrille/decoupages/kmeans/outputs/solutions/2024-07-02_PACA/Assignments/mat_cover_kmeans_canton/'
directory_path_poste_cover_kmeans_canton = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_save_cluster/Cyrille/decoupages/kmeans/outputs/solutions/2024-07-02_PACA/Assignments/poste_cover_kmeans_canton/'
directory_path_poste_cover_kmeans_commune = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-02_save_cluster/Cyrille/decoupages/kmeans/outputs/solutions/2024-07-02_PACA/Assignments/poste_cover_kmeans_commune/'


# Grid covers   
directory_path_mat_cover_grid_arrond = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-03_save_cluster/Cyrille/decoupages/grid/outputs/solutions/2024-07-02_PACA/Assignments/mat_cover_grid_arrond/'
directory_path_mat_cover_grid_EPCI = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-03_save_cluster/Cyrille/decoupages/grid/outputs/solutions/2024-07-02_PACA/Assignments/mat_cover_grid_EPCI/'
directory_path_mat_cover_grid_canton = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-03_save_cluster/Cyrille/decoupages/grid/outputs/solutions/2024-07-02_PACA/Assignments/mat_cover_grid_canton/'
directory_path_poste_cover_grid_canton = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-03_save_cluster/Cyrille/decoupages/grid/outputs/solutions/2024-07-02_PACA/Assignments/poste_cover_grid_canton/'
directory_path_poste_cover_grid_commune = '/home/felipe/Documents/Projects/GeoAvigon/save_cluster/24-07-03_save_cluster/Cyrille/decoupages/grid/outputs/solutions/2024-07-02_PACA/Assignments/poste_cover_grid_commune/'




# Extract data from all files in the specified directory
all_extracted_data_mat = read_all_files_in_directory(directory_path_mat)
all_extracted_data_poste = read_all_files_in_directory(directory_path_poste)

all_extracted_data_mat_weight_shuffled = read_all_files_in_directory(directory_path_mat_weight_shuffled)
all_extracted_data_mat_weight_split = read_all_files_in_directory(directory_path_mat_weight_split)
all_extracted_data_poste_weight_shuffled = read_all_files_in_directory(directory_path_poste_weight_shuffled)
all_extracted_data_poste_weight_split = read_all_files_in_directory(directory_path_poste_weight_split)

all_extracted_data_multiechelle_poste = read_all_files_in_directory(directory_path_multiechelle_poste)
all_extracted_data_multiechelle_mat = read_all_files_in_directory(directory_path_multiechelle_mat)

all_extracted_data_mat_cover_arrond = read_all_files_in_directory(directory_path_mat_cover_arrond)
all_extracted_data_mat_cover_EPCI = read_all_files_in_directory(directory_path_mat_cover_EPCI)
all_extracted_data_mat_cover_canton = read_all_files_in_directory(directory_path_mat_cover_canton)
all_extracted_data_poste_cover_canton = read_all_files_in_directory(directory_path_poste_cover_canton)
all_extracted_data_poste_cover_commune = read_all_files_in_directory(directory_path_poste_cover_commune)

all_extracted_data_mat_cover_kmeans_arrond = read_all_files_in_directory(directory_path_mat_cover_kmeans_arrond)
all_extracted_data_mat_cover_kmeans_EPCI = read_all_files_in_directory(directory_path_mat_cover_kmeans_EPCI)
all_extracted_data_mat_cover_kmeans_canton = read_all_files_in_directory(directory_path_mat_cover_kmeans_canton)
all_extracted_data_poste_cover_kmeans_canton = read_all_files_in_directory(directory_path_poste_cover_kmeans_canton)
all_extracted_data_poste_cover_kmeans_commune = read_all_files_in_directory(directory_path_poste_cover_kmeans_commune)

all_extracted_data_mat_cover_grid_arrond = read_all_files_in_directory(directory_path_mat_cover_grid_arrond)
all_extracted_data_mat_cover_grid_EPCI = read_all_files_in_directory(directory_path_mat_cover_grid_EPCI)
all_extracted_data_mat_cover_grid_canton = read_all_files_in_directory(directory_path_mat_cover_grid_canton)
all_extracted_data_poste_cover_grid_canton = read_all_files_in_directory(directory_path_poste_cover_grid_canton)
all_extracted_data_poste_cover_grid_commune = read_all_files_in_directory(directory_path_poste_cover_grid_commune)




# print only the customers_assignments
# for data in all_extracted_data:e
# print(all_extracted_data_mat)

# Plots compare solutions with diff weightsds
# mat
colors = ['black', 'blue', 'green']
legends = ['mat','mat_shuffled', 'mat_split']
plot_objectives_vs_p_locations([all_extracted_data_mat, all_extracted_data_mat_weight_shuffled, all_extracted_data_mat_weight_split], colors, legends)
plot_violin_dist_weights([all_extracted_data_mat, all_extracted_data_mat_weight_shuffled, all_extracted_data_mat_weight_split], colors, legends, 37)
plot_sol_and_violin([all_extracted_data_mat, all_extracted_data_mat_weight_shuffled, all_extracted_data_mat_weight_split], colors, legends, 37)


# poste
colors = ['black', 'blue', 'green']
legends = ['poste','poste_shuffled', 'poste_split']
plot_objectives_vs_p_locations([all_extracted_data_poste, all_extracted_data_poste_weight_shuffled, all_extracted_data_poste_weight_split], colors, legends)
plot_violin_dist_weights([all_extracted_data_poste, all_extracted_data_poste_weight_shuffled, all_extracted_data_poste_weight_split], colors, legends, 681)
plot_sol_and_violin([all_extracted_data_poste, all_extracted_data_poste_weight_shuffled, all_extracted_data_poste_weight_split], colors, legends, 681)

# plot different covers
colors = ['black', 'blue', 'green', 'orange']
legends = ['mat','mat_arrond', 'mat_kmeans_arrond', 'mat_grid_arrond']
plot_objectives_vs_p_locations([all_extracted_data_mat, all_extracted_data_mat_cover_arrond, all_extracted_data_mat_cover_kmeans_arrond, all_extracted_data_mat_cover_grid_arrond], colors, legends)
plot_violin_dist_weights([all_extracted_data_mat, all_extracted_data_mat_cover_arrond, all_extracted_data_mat_cover_kmeans_arrond,all_extracted_data_mat_cover_grid_arrond], colors, legends, 37)
plot_sol_and_violin([all_extracted_data_mat, all_extracted_data_mat_cover_arrond, all_extracted_data_mat_cover_kmeans_arrond, all_extracted_data_mat_cover_grid_arrond], colors, legends, 37)


colors = ['black', 'blue', 'green', 'orange']
legends = ['mat','mat_EPCI', 'mat_kmeans_EPCI', 'mat_grid_EPCI']
plot_objectives_vs_p_locations([all_extracted_data_mat, all_extracted_data_mat_cover_EPCI, all_extracted_data_mat_cover_kmeans_EPCI, all_extracted_data_mat_cover_grid_EPCI], colors, legends)
plot_violin_dist_weights([all_extracted_data_mat, all_extracted_data_mat_cover_EPCI, all_extracted_data_mat_cover_kmeans_EPCI, all_extracted_data_mat_cover_grid_EPCI], colors, legends, 37)
plot_sol_and_violin([all_extracted_data_mat, all_extracted_data_mat_cover_EPCI, all_extracted_data_mat_cover_kmeans_EPCI, all_extracted_data_mat_cover_grid_EPCI], colors, legends, 37)


colors = ['black', 'blue', 'green', 'orange']
legends = ['mat','mat_canton', 'mat_kmeans_canton', 'mat_grid_canton']
plot_objectives_vs_p_locations([all_extracted_data_mat, all_extracted_data_mat_cover_canton, all_extracted_data_mat_cover_kmeans_canton, all_extracted_data_mat_cover_grid_canton], colors, legends)
plot_violin_dist_weights([all_extracted_data_mat, all_extracted_data_mat_cover_canton, all_extracted_data_mat_cover_kmeans_canton,all_extracted_data_mat_cover_grid_canton], colors, legends, 37)
plot_sol_and_violin([all_extracted_data_mat, all_extracted_data_mat_cover_canton, all_extracted_data_mat_cover_kmeans_canton, all_extracted_data_mat_cover_grid_canton], colors, legends, 37)   

colors = ['black', 'blue', 'green', 'orange']
legends = ['poste','poste_canton', 'poste_kmeans_canton', 'poste_grid_canton']
plot_objectives_vs_p_locations([all_extracted_data_poste, all_extracted_data_poste_cover_canton, all_extracted_data_poste_cover_kmeans_canton, all_extracted_data_poste_cover_grid_canton], colors, legends)
plot_violin_dist_weights([all_extracted_data_poste, all_extracted_data_poste_cover_canton, all_extracted_data_poste_cover_kmeans_canton,all_extracted_data_poste_cover_grid_canton], colors, legends, 681)
plot_sol_and_violin([all_extracted_data_poste, all_extracted_data_poste_cover_canton, all_extracted_data_poste_cover_kmeans_canton, all_extracted_data_poste_cover_grid_canton], colors, legends, 681)
colors = ['black', 'blue', 'green', 'orange']
legends = ['poste','poste_commune', 'poste_kmeans_commune', 'poste_grid_commune']
plot_objectives_vs_p_locations([all_extracted_data_poste, all_extracted_data_poste_cover_commune, all_extracted_data_poste_cover_kmeans_commune, all_extracted_data_poste_cover_grid_commune], colors, legends)
plot_violin_dist_weights([all_extracted_data_poste, all_extracted_data_poste_cover_commune, all_extracted_data_poste_cover_kmeans_commune,all_extracted_data_poste_cover_grid_commune], colors, legends, 681)
plot_sol_and_violin([all_extracted_data_poste, all_extracted_data_poste_cover_commune, all_extracted_data_poste_cover_kmeans_commune, all_extracted_data_poste_cover_grid_commune], colors, legends, 681)


# Plost Multiechelles vs Original covers
# mat
colors = ['black', 'blueviolet', 'blue', 'green', 'orange']
legends = ['mat','mat_arrond_canton', 'mat_arrond', 'mat_canton', 'mat_EPCI']
plot_objectives_vs_p_locations([all_extracted_data_mat, all_extracted_data_multiechelle_mat, all_extracted_data_mat_cover_arrond, all_extracted_data_mat_cover_canton,all_extracted_data_mat_cover_EPCI], colors, legends)
plot_violin_dist_weights([all_extracted_data_mat, all_extracted_data_multiechelle_mat, all_extracted_data_mat_cover_arrond, all_extracted_data_mat_cover_canton,all_extracted_data_mat_cover_EPCI], colors, legends, 37)
plot_sol_and_violin([all_extracted_data_mat, all_extracted_data_multiechelle_mat, all_extracted_data_mat_cover_arrond, all_extracted_data_mat_cover_canton,all_extracted_data_mat_cover_EPCI], colors, legends, 37)

colors = ['black', 'blueviolet', 'blue', 'green']
legends = ['poste','poste_canton_commune', 'poste_canton', 'poste_commune']
plot_objectives_vs_p_locations([all_extracted_data_poste, all_extracted_data_multiechelle_poste, all_extracted_data_poste_cover_canton, all_extracted_data_poste_cover_commune], colors, legends)
plot_violin_dist_weights([all_extracted_data_poste, all_extracted_data_multiechelle_poste, all_extracted_data_poste_cover_canton, all_extracted_data_poste_cover_commune], colors, legends, 681)
plot_sol_and_violin([all_extracted_data_poste, all_extracted_data_multiechelle_poste, all_extracted_data_poste_cover_canton, all_extracted_data_poste_cover_commune], colors, legends, 681) 


# colors = ['blueviolet', 'green']
# legends = ['poste_canton_commune', 'poste_commune']
# plot_objectives_vs_p_locations([all_extracted_data_multiechelle_poste, all_extracted_data_poste_cover_commune], colors, legends)



# # # Print the extracted data
# for data in all_extracted_data_mat:
#     objective, p_locations, p_locations_size, customer_assignments = data
#     print(f"Objective: {objective}")
#     print(f"P LOCATIONS: {p_locations} (Size: {p_locations_size})")
#     print(f"CUSTOMER ASSIGNMENTS: {customer_assignments}")
#     print(len(customer_assignments))
#     print()