import pandas as pd

# Step 1: Read and parse the files
# Read customer assignments from sol.txt
def parse_sol(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Find the index where customer assignments start
    customer_assignments_index = 0
    for i, line in enumerate(lines):
        if "CUSTOMER ASSIGNMENTS" in line:
            customer_assignments_index = i + 2  # Skip the header line and start reading assignments
            break
    
    # Parse customer assignments
    customer_assignments = []
    for line in lines[customer_assignments_index:]:
        if '->' in line:
            try:
                parts = line.split('->')
                customer_demand = parts[0].strip().split()
                customer = int(customer_demand[0])
                demand = float(customer_demand[1].strip('()'))
                assignments = parts[1].split()
                for i in range(0, len(assignments), 2):
                    location = int(assignments[i])
                    assigned_demand = float(assignments[i + 1].strip('()'))
                    customer_assignments.append((customer, demand, location, assigned_demand))
            except (ValueError, IndexError) as e:
                print(f"Error parsing customer assignment line: {line.strip()} - {e}")
    
    # Convert the parsed assignments to a dictionary for easy access
    assignments_dict = {(customer, location): assigned_demand for customer, _, location, assigned_demand in customer_assignments}
    return assignments_dict

# Read distances from dist.txt
def parse_dist(file_path):
    dist_df = pd.read_csv(file_path, sep=' ', header=0)
    dist_dict = {}
    for _, row in dist_df.iterrows():
        dist_dict[(int(row['customer']), int(row['location']))] = float(row['distance'])
    return dist_dict

# Read customer weights from cust.txt
def parse_cust(file_path):
    cust_df = pd.read_csv(file_path, sep=' ', header=0)
    weights = {}
    for _, row in cust_df.iterrows():
        weights[int(row['customer'])] = float(row['weight'])
    return weights

# Step 2: Calculate Objective Functions
def calculate_objectives(assignments, distances, weights):
    obj1 = 0.0
    obj2 = 0.0
    for (customer, location), assigned_demand in assignments.items():
        dist = distances.get((customer, location), 0.0)
        weight = weights.get(customer, 0.0)
        obj1 += dist * assigned_demand/weight
        obj2 += dist * assigned_demand
    return obj1, obj2


# File paths
sol_file = 'solutions/solution_cinema_p_900.txt'
dist_file = '/home/falbuquerque/Documents/projects/GeoAvignon/PMPSolver/data/PACA_Jul24/dist_matrix_minutes_2037.txt'
cust_file = '/home/falbuquerque/Documents/projects/GeoAvignon/PMPSolver/data/PACA_Jul24/cust_weights_PACA_2037_Jul24.txt'

# Parse files
assignments = parse_sol(sol_file)
distances = parse_dist(dist_file)
weights = parse_cust(cust_file)

# Calculate objective functions
objective_1, objective_2 = calculate_objectives(assignments, distances, weights)

print(sol_file)
print(f"Objective Function Unweighted: {objective_1}")
print(f"Objective Function Weighted: {objective_2}")