import os
import csv

# Specify the directory containing the CSV files
directory = '/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/savecluster_Literature/2024-06-14_save-cluster/outputs/solutions/2024-06-14_LIT/Results_cplex/'

# List all CSV files in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# Specify the path for the merged output file
output_file = './outputs/merge_csv/results_cplex.csv'

# Open the output file in write mode
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    
    # Iterate over the CSV files
    for csv_file in csv_files:
        file_path = os.path.join(directory, csv_file)
        
        # Open each CSV file
        with open(file_path, 'r', newline='') as infile:
            reader = csv.reader(infile)
            
            # # Write a new line to separate contents of different files (if outfile is not empty)
            # if outfile.tell() != 0:
            #     writer.writerow([])
            
            # Write the contents of the current CSV file to the output file
            for row in reader:
                writer.writerow(row)

print("CSV files merged successfully with each file's content on a new line!")






