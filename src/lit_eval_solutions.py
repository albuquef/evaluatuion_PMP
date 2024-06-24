import os
import math
import glob
import statistics

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

def read_customer_assignments(filename):
    assignments = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        # Flag to identify the section of the file
        in_location_assignments = False
        
        for line in lines:
            line = line.strip()
            
            if not line or line.startswith("CUSTOMER ASSIGNMENTS"):
                continue
            
            # Handle the new format
            if line == "P LOCATIONS":
                in_location_assignments = False
                continue
            
            if line == "LOCATION ASSIGNMENTS":
                in_location_assignments = True
                continue
            
            if not in_location_assignments:
                if "->" in line:
                    customer_part, location_part = line.split("->")
                    try:
                        customer = int(customer_part.split()[0])
                        location = int(location_part.split()[0])
                        assignments[customer] = location
                    except ValueError:
                        continue
            else:
                if ':' in line:
                    location_part, customers_part = line.split(":")
                    try:
                        location = int(location_part.strip())
                        customers = map(int, customers_part.split())
                        for customer in customers:
                            assignments[customer] = location
                    except ValueError:
                        continue
    
    return assignments

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

def calculate_euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

def min_dit_bigger_than_zero(distances):
    min_dist_diff_zero = max(distances)
    for d in distances:
        if d > 0 and d < min_dist_diff_zero:
            min_dist_diff_zero = d
    return min_dist_diff_zero

def process_files(directory_data, directory_sols_method, directory_sol_lit, base_filenames):
    for base_filename in base_filenames:
        customer_data_file = os.path.join(directory_data, f'cust_weights_{base_filename}.txt')
        # assignment_files = glob.glob(os.path.join(directory_sols_method, f'test_lit_{base_filename}_p_*_RSSV_EXACT_CPMP_BIN.txt'))
        assignment_files = glob.glob(os.path.join(directory_sols_method, f'test_lit_{base_filename}_p_*.txt'))
        # solution_file = glob.glob(os.path.join(directory_sol_lit, f'solucao.{base_filename}_*.txt'))[0]
        solution_file = glob.glob(os.path.join(directory_sol_lit, f'soluOPT.{base_filename}_*.txt'))[0]

        print(f"Processing files for base filename {base_filename}:")
        print(f"Customer Data File: {customer_data_file}")

        # Read customer data
        customer_data = read_customer_data(customer_data_file)

        for assignment_file in assignment_files:
            print(f"Assignments File: {assignment_file}")

            # Read customer assignments
            customer_assignments = read_customer_assignments(assignment_file)

            distances = []
            for customer, location in customer_assignments.items():
                if customer in customer_data and location in customer_data:
                    coord_customer = customer_data[customer]
                    coord_location = customer_data[location]
                    distance = calculate_euclidean_distance(coord_customer, coord_location)
                    distances.append(distance)
                else:
                    print(f"Customer {customer} or Location {location} data not found")

            total_distance = sum(distances)
            if distances:
                max_distance = max(distances)
                min_distance = min(distances)
                min_dist_diff_zero = min_dit_bigger_than_zero(distances)
                avg_distance = statistics.mean(distances)
                stddev_distance = statistics.stdev(distances)
            else:
                max_distance = avg_distance = stddev_distance = min_distance = min_dist_diff_zero = 0

            print(f"Total Euclidean Distance: {total_distance}")
            print(f"Maximum Distance: {max_distance}")
            print(f"Minimum Distance: {min_distance}")
            print(f"Minimum Distance Different from Zero: {min_dist_diff_zero}")
            print(f"Average Distance: {avg_distance}")
            print(f"Standard Deviation of Distances: {stddev_distance}")
            print('-' * 50)


        print('-' * 50)
        print(f"Solution File: {solution_file}")

        # Read solution data
        assignments, cluster_distances = read_assignments_and_clusters(solution_file)

        distances = []
        for customer, location in assignments.items():
            if customer in customer_data and location in customer_data:
                coord_customer = customer_data[customer]
                coord_location = customer_data[location]
                distance = calculate_euclidean_distance(coord_customer, coord_location)
                distances.append(distance)
            else:
                print(f"Customer {customer} or Location {location} data not found")

        total_distance = sum(distances)
        if distances:
            max_distance = max(distances)
            min_distance = min(distances)
            min_dist_diff_zero = min_dit_bigger_than_zero(distances)
            avg_distance = statistics.mean(distances)
            stddev_distance = statistics.stdev(distances)
        else:
            max_distance = avg_distance = stddev_distance = 0

        print(f"Total Euclidean Distance: {total_distance}")
        print(f"Maximum Distance: {max_distance}")
        print(f"Minimum Distance: {min_distance}")
        print(f"Minimum Distance Different from Zero: {min_dist_diff_zero}")
        print(f"Average Distance: {avg_distance}")
        print(f"Standard Deviation of Distances: {stddev_distance}")

        sum_cluster_distances = sum(cluster_distances.values())
        print(f"Sum of Distances from Clusters: {sum_cluster_distances}")
        print()

def main():
    # directory_data = '/home/falbuquerque/Documents/projects/Project_PMP/large-PMP/data/Literature/group5/'
    # directory_sol_lit = '/home/falbuquerque/Documents/projects/Project_PMP/large-PMP/data/Literature/solutions_lit/'
    # directory_sols_method = '/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/24-06-24_save_cluster/Literature_test_2/outputs/solutions/2024-06-24_LIT/Assignments'
    # base_filenames = ['pr2392_020', 'pr2392_075', 'pr2392_150', 'pr2392_300', 'pr2392_500']
    
    directory_data = '/home/felipe/Documents/Projects/GeoAvigon/pmp_code/large-PMP/data/Literature/group2/'
    directory_sol_lit = '/home/felipe/Documents/Projects/GeoAvigon/pmp_code/large-PMP/data/Literature/solutions_lit/'
    directory_sols_method = '/home/felipe/Documents/Projects/GeoAvigon/pmp_code/large-PMP/outputs/solutions/2024-06-24_LIT/Assignments'
    base_filenames = ['SJC1']
    
    process_files(directory_data, directory_sols_method, directory_sol_lit, base_filenames)

if __name__ == "__main__":
    main()
