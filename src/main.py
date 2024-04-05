import pandas as pd

from create_df import create_df_loc_cust
from graphics_sol import create_plot_Evolution_Sol
from graphics_sol import create_comparative_Sol

def main():
    print("Main function")

    # id_path = 'map_id_cust_loc.txt'
    # dist_path = 'dist_matrix_minutes.txt'
    # # txt_path = 'test_paca_mat_arrond_p_26_RSSV_EXACT_CPMP_cover_arrond.txt'
    # txt_path = 'test_paca_mat_null_p_26_EXACT_CPMP.txt'
    # df_locations, df_customers = create_df_loc_cust(id_path, dist_path, txt_path)
    # print("Location Usages:")
    # print(df_locations)
    # print("\nCustomer Assignments:")
    # print(df_customers)

    # # Print statistics about distance
    # print("Statistics about distance:")
    # print(df_customers['distance'].describe())

    # df_locations.to_csv('output.csv', index=False)



    # Create plot fo x time
    # p=26
    # path_table = f'./tables_evolution_sol/report_mat_p_{p}.csv'
    # cover = 'null'
    # create_plot_Evolution_Sol(path_table, p, cover)

    # Create comparative plot
    path_data = './tables_sol/'
    vet_p = [26]
    cover = 'null'
    create_comparative_Sol(path_data, vet_p, cover)












if __name__ == "__main__":
    main()





# # Read the text file
# with open('test_paca_mat_arrond_p_26_RSSV_EXACT_CPMP_cover_arrond.txt', 'r') as file:
#     lines = file.readlines()

# identifiers_df = pd.read_csv('map_id_cust_loc.txt', sep='\s+')

# # Find the indices where the different sections start and end
# location_usages_index = lines.index('LOCATION USAGES\n') + 2
# customer_assignments_index = lines.index('CUSTOMER ASSIGNMENTS\n') + 2

# # Parse location usages
# location_usages = []
# for line in lines[location_usages_index:customer_assignments_index-1]:
#     if '(' in line:  # Skip header line
#         parts = line.split('(')
#         location = int(parts[0].strip())
#         usage_capacity = parts[1].split('/')
#         usage = float(usage_capacity[0].strip())
#         capacity = float(usage_capacity[1].replace(')', '').strip())
#         location_usages.append((location, usage, capacity))

# # Parse customer assignments
# customer_assignments = []
# current_assignment = None
# for line in lines[customer_assignments_index:]:
#     parts = line.split('->')
#     customer_demand = parts[0].strip().split()
#     customer = int(customer_demand[0])
#     demand = float(customer_demand[1].strip('()'))
#     assignments = parts[1].split()
#     for i in range(0, len(assignments), 2):
#         location = int(assignments[i])
#         assigned_demand = float(assignments[i + 1].strip('()'))
#         customer_assignments.append((customer, demand, location, assigned_demand))



# # Create DataFrames
# df_locations = pd.DataFrame(location_usages, columns=['location', 'usage', 'capacity'])
# # Merge with identifiers DataFrame
# df_locations = df_locations.merge(identifiers_df, left_on='location', right_on='id').drop('id', axis=1)

# df_customers = pd.DataFrame(customer_assignments, columns=['customer', 'demand', 'location', 'assigned_demand'])
# # Merge df_customers with identifiers_df for customer
# df_customers = df_customers.merge(identifiers_df, how='left', left_on='customer', right_on='id').drop('id', axis=1)
# df_customers.rename(columns={'identif': 'identif_cust'}, inplace=True)

# # Merge df_customers with identifiers_df for location
# df_customers = df_customers.merge(identifiers_df, how='left', left_on='location', right_on='id').drop('id', axis=1)
# df_customers.rename(columns={'identif': 'identif_loc'}, inplace=True)


# # Read the distance file
# df_distance = pd.read_csv('dist_matrix_minutes.txt', sep='\s+')
# # Merge df_customers with distance_df
# df_customers = df_customers.merge(df_distance, how='left', on=['customer', 'location'])

# # print("Location Usages:")
# # print(df_locations)
# # print("\nCustomer Assignments:")
# # print(df_customers[949:1000])


# # Print statistics about distance
# print("Statistics about distance:")
# print(df_customers['distance'].describe())

