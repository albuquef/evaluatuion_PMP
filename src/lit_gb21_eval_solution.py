
import os
import math


def calculate_euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

def read_customer_data(filename):
    customer_data = {}
    with open(filename, 'r') as file:
        next(file)  # Skip the header line
        for line in file:
            parts = line.strip().split()
            customer_id = int(parts[0])
            weight = float(parts[1])
            coord_x = float(parts[2])
            coord_y = float(parts[3])
            customer_data[customer_id] = (coord_x, coord_y)
    return customer_data

def read_assignments_and_clusters(filename):
    assignments = {}
    cluster_distances = {}
    current_cluster = None
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("Cluster"):
                current_cluster = int(line.split()[1])
            elif line.startswith("Distance ="):
                if current_cluster is not None:
                    distance = float(line.split('=')[1].strip())
                    cluster_distances[current_cluster] = distance
            elif line:
                try:
                    parts = line.split()
                    if len(parts) == 2:
                        customer_id = int(parts[0])
                        location_id = int(parts[1])
                        assignments[customer_id] = location_id
                except ValueError:
                    continue
    return assignments, cluster_distances


def read_assignments(filename):
    assignments = {}

    # Open the file and read it line by line
    with open(filename, 'r') as file:
        for line in file:
            # Split the line into key and value parts
            key, value = line.strip().split(' -> ')
            # Convert them to integers and add to the dictionary
            assignments[int(key)] = int(value)
    return assignments


directory_data = '/home/falbuquerque/Documents/projects/Project_PMP/large-PMP/data/Literature/group3/'
# base_filenames = ['p3038_600', 'p3038_700', 'p3038_800', 'p3038_900', 'p3038_1000']
# base_filenames = ['fnl4461_0020', 'fnl4461_0100', 'fnl4461_0250', 'fnl4461_0500', 'fnl4461_1000']
base_filenames = ['p3038_600']

for base_filename in base_filenames:
    customer_data_file = os.path.join(directory_data, f'cust_weights_{base_filename}.txt')

    customer = read_customer_data(customer_data_file)

    # print(customer)

    assigments = read_assignments(f'data_gb21/assigments_{base_filename}.txt')

    # print(assigments)

    # calculate the sum of the distances
    sum_distance = 0
    for a in assigments:
        assignment = assigments[a]
        # print(f'{a+1} -> {assignment+1}')
        customer_coord = customer[a+1]  # Customer's coordinate
        location_coord = customer[assignment+1]  # Assigned location's coordinate
        distance = calculate_euclidean_distance(customer_coord, location_coord)
        sum_distance += distance
    
    print(f'{base_filename} -> {sum_distance}')

    