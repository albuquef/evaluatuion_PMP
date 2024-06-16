import pandas as pd

def create_df_loc_cust(id_path, dist_path, txt_path):
    
    # Read the identifiers file
    identifiers_df = pd.read_csv(id_path, sep='\s+')
    # Read the distance file
    df_distance = pd.read_csv(dist_path, sep='\s+')
    
    # Read the text file
    with open(txt_path, 'r') as file:
        lines = file.readlines()

    # Find the indices where the different sections start and end
    location_usages_index = lines.index('LOCATION USAGES\n') + 2
    customer_assignments_index = lines.index('CUSTOMER ASSIGNMENTS\n') + 2

    # Parse location usages
    location_usages = []
    for line in lines[location_usages_index:customer_assignments_index-1]:
        if '(' in line:  # Skip header line
            parts = line.split('(')
            location = int(parts[0].strip())
            usage_capacity = parts[1].split('/')
            usage = float(usage_capacity[0].strip())
            capacity = float(usage_capacity[1].replace(')', '').strip())
            location_usages.append((location, usage, capacity))

    # Parse customer assignments
    customer_assignments = []
    current_assignment = None
    for line in lines[customer_assignments_index:]:
        parts = line.split('->')
        customer_demand = parts[0].strip().split()
        customer = int(customer_demand[0])
        demand = float(customer_demand[1].strip('()'))
        assignments = parts[1].split()
        for i in range(0, len(assignments), 2):
            location = int(assignments[i])
            assigned_demand = float(assignments[i + 1].strip('()'))
            customer_assignments.append((customer, demand, location, assigned_demand))


    # Create DataFrames
    df_locations = pd.DataFrame(location_usages, columns=['location', 'usage', 'capacity'])
    # Merge with identifiers DataFrame
    df_locations = df_locations.merge(identifiers_df, left_on='location', right_on='id').drop('id', axis=1)

    df_assignment = pd.DataFrame(customer_assignments, columns=['customer', 'demand', 'location', 'assigned_demand'])
    # Merge df_assignment with identifiers_df for customer
    df_assignment = df_assignment.merge(identifiers_df, how='left', left_on='customer', right_on='id').drop('id', axis=1)
    df_assignment.rename(columns={'identif': 'identif_cust'}, inplace=True)

    # Merge df_assignment with identifiers_df for location
    df_assignment = df_assignment.merge(identifiers_df, how='left', left_on='location', right_on='id').drop('id', axis=1)
    df_assignment.rename(columns={'identif': 'identif_loc'}, inplace=True)

    # Merge df_assignment with distance_df
    df_assignment = df_assignment.merge(df_distance, how='left', on=['customer', 'location'])

    # new collumn with the weighted distance
    df_assignment['weighted_distance'] = df_assignment['distance'] * df_assignment['assigned_demand']

    return df_locations, df_assignment