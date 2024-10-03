import os
import pandas as pd
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
    unique_subareas = set()  # Set to store unique subarea identifiers
    for location in sol_locations:
        if location in subarea_mappings:
            unique_subareas.add(subarea_mappings[location])  # Add subarea (the value) to the set
    return len(unique_subareas)
def set_subareas_covered(sol_locations, subarea_mappings):
    unique_subareas = set()  # Set to store unique subarea identifiers
    for location in sol_locations:
        if location in subarea_mappings:
            unique_subareas.add(subarea_mappings[location])  # Add subarea (the value) to the set
    return unique_subareas


# Main function
def main():
    # Directory containing the solution files
    # SOL_DIR = '/home/falbuquerque/Documents/projects/GeoAvignon/tests_Cyrille/original_dataset/cover_commune/'
    SOL_DIR = '/home/falbuquerque/Documents/projects/GeoAvignon/tests_Cyrille/shuffle_dataset/nocover/nocover/'
    # SOL_DIR = 'solutions/'
    
    # List all solution files in the directory
    sol_files = [f for f in os.listdir(SOL_DIR) if f.endswith('.txt')]

    # Directory containing the subarea files
    DIR = '/home/falbuquerque/Documents/projects/GeoAvignon/PMPSolver/data/PACA_jul24/'
    
    # Constant subarea files
    subarea_files = ['loc_coverages_arrond_2037.txt', 'loc_coverages_EPCI_2037.txt', 
                     'loc_coverages_canton_2037.txt', 'loc_coverages_commune_2037.txt']

    # Read all subarea files once
    subarea_mappings = [read_subarea_file(DIR + subarea_file) for subarea_file in subarea_files]

    print ("Subarea mappings read successfully!")
    # print size
    print(len(subarea_mappings))

    # Create a table to store results
    result_table = pd.DataFrame(columns=["p_locations_size"] + [f"number_cover_{file.split('_')[2]}" for file in subarea_files])

    # Process each solution file
    for sol_file in sol_files:
        # Read P LOCATIONS from each solution file
        sol_file_path = os.path.join(SOL_DIR, sol_file)
        p_locations = read_sol_file(sol_file_path)

        # Initialize a row to store results for this solution
        result_row = {"p_locations_size": len(p_locations)}

        # Count unique subareas covered by the current solution
        for idx, subarea_mapping in enumerate(subarea_mappings):


            # print size
            # print(subarea_mapping)

            unique_subarea_count = count_unique_subareas(p_locations, subarea_mapping)
            # print(f"Solution {sol_file} covers {unique_subarea_count} unique subareas in {subarea_files[idx]}")

            unique_subareas_covered = set_subareas_covered(p_locations, subarea_mapping)

            # Extract subarea name from file and store the result
            subarea_name = subarea_files[idx].split('_')[2]
            result_row[f"number_cover_{subarea_name}"] = unique_subarea_count

            # if p_locations_size > len(subarea_mapping) then we have a solution that covers all subareas check and print
            # create a test to see if the solution covers all subareas

            # get unique subareas from the subarea_mapping
            unique_subareas_total = set(subarea_mapping.values())

            print(len(unique_subareas_total ))
            if len(p_locations) >= len(unique_subareas_total):
                if unique_subarea_count == len(unique_subareas_total):
                    print(f"Solution {sol_file} covers all subareas in {subarea_files[idx]}")
                else:
                    print(f"Solution {sol_file} does not cover all subareas in {subarea_files[idx]}")
                    # print the subarea that have more than one location covered
                    # for location in p_locations:
                    #     if location in subarea_mapping:
                    #         # print only have more than one location covered
                    #         if list(subarea_mapping.values()).count(subarea_mapping[location]) > 1:
                    #             print(f"Location {location} is in subarea {subarea_mapping[location]}")
                    #print the subareas that are not covered
                    for subarea in unique_subareas_total:
                        if subarea not in unique_subareas_covered:
                            print(f"Subarea {subarea} is not covered")

            # if p_locations_size < len(subarea_mapping) then we have a solution that covers at least p_locations_size subareas
            # create a test to see if the solution covers at least p_locations_size subareas
            if len(p_locations) < len(unique_subareas_total):
                if unique_subarea_count >= len(p_locations):
                    print(f"Solution {sol_file} covers at least {len(p_locations)} subareas in {subarea_files[idx]}")
                else:
                    print(f"Solution {sol_file} does not cover at least {len(p_locations)} subareas in {subarea_files[idx]}")
                    # print the subarea that have more than one location covered
                    # for location in p_locations:
                    #     if location in subarea_mapping:
                    #         # print only have more than one location covered
                    #         if list(subarea_mapping.values()).count(subarea_mapping[location]) > 1:
                    #             print(f"Location {location} is in subarea {subarea_mapping[location]}")
                    # for subarea in unique_subareas_total:
                    #     if subarea not in unique_subareas_covered:
                    #         print(f"Subarea {subarea} is not covered")



        # Append the row to the table
        # result_table = result_table.append(result_row, ignore_index=True)
        # result_table = result_table._append(result_row, ignore_index=True)
        result_table = pd.concat([result_table, pd.DataFrame([result_row])], ignore_index=True)



    # sort the columns by p_locations_size
    result_table = result_table.sort_values(by="p_locations_size")

    # Save the table to a CSV file
    result_table.to_csv('outputs/coverage_summary.csv', index=False)
    print("Table saved successfully!")

# Run the main function
if __name__ == "__main__":
    main()