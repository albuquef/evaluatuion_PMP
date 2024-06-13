import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from create_df import create_df_loc_cust
from graphics_sol import create_plot_Evolution_Sol
from graphics_sol import create_comparative_Sol, create_plot_comparative_Sol_covers

def plot_service_solutions(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Filter the DataFrame to include only the relevant methods
    df_filtered = df[df['METHOD'].isin(['exact', 'rssv_exact'])]
    
    # Sort the DataFrame by 'P' values in ascending order
    df_filtered = df_filtered.sort_values(by='P')

    # print values of p
    print(df_filtered['P'].unique())


    # Group the data by the 'SERVICE' column
    services = df_filtered['SERVICE'].unique()

    for service in services:
        plt.figure(figsize=(10, 6))
        
        for method in ['exact', 'rssv_exact']:
            method_data = df_filtered[(df_filtered['SERVICE'] == service) & (df_filtered['METHOD'] == method)]
            unique_p_values = method_data['P'].unique()
            # Plot only the unique P values for each service
            plt.plot(unique_p_values, method_data.groupby('P')['SOLUTION'].mean(), marker='o', label=method)
            plt.xticks(unique_p_values) 
        
        
        # Customize the plot
        plt.title(f'Solutions for Service: {service}')
        plt.xlabel('P') 
        plt.ylabel('Solution')
        plt.legend()
        plt.grid(True)


        # Save the plot as a PDF file with the service name included in the filename
        plt.savefig(f'cpmp_solutions_{service}.pdf', bbox_inches='tight')


        # Show the plot
        plt.show()


def plot_cpmp_cover_service_graphs(csv_file, desired_methods, desired_subareas):
    # Read the CSV data
    data = pd.read_csv(csv_file)

    # Clean up the data (handle missing values and correct data types if needed)
    # data = data.dropna(subset=['SERVICE', 'METHOD', 'SUBAREA', 'P', 'SOLUTION'])

    # Ensure 'null' subarea is treated as a string
    data['SUBAREA'] = data['SUBAREA'].astype(str)

    # Filter data based on desired methods and subareas
    filtered_data = data[(data['METHOD'].isin(desired_methods)) & (data['SUBAREA'].isin(desired_subareas))]



    # # Create a dictionary for line styles and colors
    # line_styles = {'exact': '-', 'rssv_exact': '--'}  # Add more methods if necessary
    # subarea_colors = {'null': 'blue', 'arrond': 'green', 'blue': 'black', 'canton': 'orange', 'commune': 'purple'}  # Add more subareas if necessary

    # Create a dictionary for line styles and colors
    line_styles = {method: style for method, style in zip(desired_methods, ['-', '--', '-.', ':'])}  # Add more methods if necessary
    subarea_colors = {subarea: color for subarea, color in zip(desired_subareas, ['black','blue', 'green', 'red', 'cyan', 'magenta'])}  # Add more subareas if necessary



    # Plot the graphs
    for service in filtered_data['SERVICE'].unique():
        plt.figure(figsize=(10, 6))
        service_data = filtered_data[filtered_data['SERVICE'] == service]
        
        for method in service_data['METHOD'].unique():
            method_data = service_data[service_data['METHOD'] == method]
            
            for subarea in method_data['SUBAREA'].unique():
                subarea_data = method_data[method_data['SUBAREA'] == subarea]
                subarea_data = subarea_data.sort_values(by='P')
                plt.plot(subarea_data['P'], subarea_data['SOLUTION'],
                         linestyle=line_styles.get(method, '-'),
                         marker='o',
                         markersize=6,  # Increase marker size
                         linewidth=2,  # Increase line width
                         alpha=0.7,  # Add transparency
                         color=subarea_colors.get(subarea, 'black'),
                         label=f'{method}-{subarea}')
        
        # suba = 'commune'
        plt.title(f'PACA  Service: {service}')
        plt.xlabel('P')
        plt.xticks(subarea_data['P'].unique())
        plt.ylabel('Solution')
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Position the legend outside the plot
        plt.legend()
        plt.grid(True)
        # plt.tight_layout(rect=[0, 0, 0.75, 1])  # Adjust the plot to make room for the legend

        # Save the plot as a PDF with the name of the service
        plt.savefig(f'./plots/plots_cpmp_cover/cpmp_cover_sols_{service}.pdf', bbox_inches='tight')
        plt.show()



def plot_rel_gap_for_exact_method(csv_file, desired_subareas):
    # Read the CSV data
    data = pd.read_csv(csv_file)
    
    # Ensure 'null' subarea is treated as a string
    data['SUBAREA'] = data['SUBAREA'].astype(str)
    
    method = 'rssv_exact'
    # Filter data for 'exact' method
    exact_data = data[data['METHOD'] == method]
    
    # Clean up the data (handle missing values and correct data types if needed)
    exact_data = exact_data.dropna(subset=['SERVICE', 'SUBAREA', 'P', 'REL_GAP'])
    
    # Filter data based on desired subareas
    filtered_data = exact_data[exact_data['SUBAREA'].isin(desired_subareas)]
    
    # Convert REL_GAP to percentage
    filtered_data['REL_GAP'] = filtered_data['REL_GAP'] * 100

    # Create a dictionary for colors
    subarea_colors = {subarea: color for subarea, color in zip(desired_subareas, ['black', 'blue', 'green', 'red', 'cyan', 'magenta'])}  # Add more subareas if necessary

    # Plot the graphs
    for service in filtered_data['SERVICE'].unique():
        plt.figure(figsize=(12, 8))
        service_data = filtered_data[filtered_data['SERVICE'] == service]
        
        for subarea in service_data['SUBAREA'].unique():
            subarea_data = service_data[service_data['SUBAREA'] == subarea]
            # Sort the data by P in ascending order
            subarea_data = subarea_data.sort_values(by='P')
            
            plt.plot(subarea_data['P'], subarea_data['REL_GAP'],
                     linestyle='-',  # Solid line for 'exact' method
                     marker='s',  # Add marker style
                     markersize=6,  # Increase marker size
                     linewidth=2,  # Increase line width
                     alpha=0.8,  # Add transparency
                     color=subarea_colors.get(subarea, 'black'),
                     label=f'{method}-{subarea}')
        
        plt.title(f'Service: {service}')
        plt.xlabel('P')
        plt.xticks(subarea_data['P'].unique())
        plt.ylabel('Relative Gap (%)')
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small', title='Subarea')  # Position the legend outside the plot
        plt.legend()
        plt.grid(True)
        # plt.tight_layout(rect=[0, 0, 0.75, 1])  # Adjust the plot to make room for the legend
        
        # Save the plot as a PDF with the name of the service
        plt.savefig(f'./plots/plots_cpmp_cover/cpmp_cover_rel_gap_{method}_{service}.pdf', bbox_inches='tight')
        plt.show()


def create_table_statistics(services, pvalues, coverages, methods):
    columns = ['serv', 'p', 'cover', 'method', 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    df_stats = pd.DataFrame(columns=columns)

    df_test_coverages = pd.DataFrame(columns=['serv', 'p', 'cover', 'method', 'num_unique_subareas', 'num_total_subareas'])
    
    all_data = []
    
    for method in methods:
        for serv in services:
            for cover in coverages:
                for pvalue in pvalues:
                    id_path = f'./tables/tables_id/map_id_cust_loc.txt'
                    dist_path = f'./tables/tables_dist/dist_matrix_minutes.txt'
                    txt_path = f'./tables/tables_assign/test_paca_{serv}_{cover}_canton_p_{pvalue}_{method}_cover_{cover}.txt'    
                    if cover == 'null':
                        txt_path = f'./tables/tables_assign/test_paca_{serv}_canton_p_{pvalue}_{method}.txt'
                    df_locations, df_assignment = create_df_loc_cust(id_path, dist_path, txt_path)
                    
                    df_stats.loc[len(df_stats)] = [serv, pvalue, cover, method] + df_assignment['distance'].describe().tolist()
                    
                    txt_coverages = f'./tables/tables_coverages/loc_coverages_{cover}.txt'
                    if cover == 'null':
                        txt_coverages = f'./tables/tables_coverages/loc_coverages_arrond.txt'

                    subarea_data = pd.read_csv(txt_coverages, sep=' ')
                    num_total_subareas = subarea_data['subarea'].nunique() # Count the number total of unique subareas
                    subarea_data_filtered = subarea_data[subarea_data['location'].isin(df_locations['location'])]
                    num_unique_subareas = subarea_data_filtered['subarea'].nunique() # Count the number of unique subareas covered
                    
                    df_test_coverages.loc[len(df_test_coverages)] = [serv, pvalue, cover, method, num_unique_subareas, num_total_subareas]
                    
                    # Collect data for plotting
                    df_assignment['service'] = serv
                    df_assignment['coverage'] = cover
                    all_data.append(df_assignment[['distance', 'service', 'coverage']])
    
        df_stats.to_csv(f'df_stats_{method}.csv', index=False, mode='a')
        df_test_coverages.to_csv(f'df_count_coverages_{method}.csv', index=False, mode='a')
    
    # Combine all data for plotting
    all_data_df = pd.concat(all_data, ignore_index=True)

    # Create violin plots
    for service in all_data_df['service'].unique():
        plt.figure(figsize=(12, 8))
        service_data = all_data_df[all_data_df['service'] == service]
        
        sns.violinplot(x='coverage', y='distance', data=service_data)
        plt.title(f'Violin Plot for Service: {service}')
        plt.xlabel('Coverage Type')
        plt.ylabel('Distance')
        plt.xticks(rotation=45)
        plt.grid(True)
        
        plt.savefig(f'./plots/violin_plots/violin_plot_{service}.pdf', bbox_inches='tight')
        plt.show()

    for service in all_data_df['service'].unique():
        plt.figure(figsize=(12, 8))
        service_data = all_data_df[all_data_df['service'] == service]
        
        sns.violinplot(x='coverage', y='distance', data=service_data, inner=None)  # Set inner to None to remove the inner box plot
        sns.stripplot(x='coverage', y='distance', data=service_data, color='k', alpha=0.5, jitter=True)  # Add the points
        
        plt.title(f'Violin Plot for Service: {service}')
        plt.xlabel('Coverage Type')
        plt.ylabel('Distance')
        plt.xticks(rotation=45)
        plt.grid(True)
        
        plt.savefig(f'./plots/violin_plots/violin_plot_point_{service}.pdf', bbox_inches='tight')
        plt.show()

def plot_coverages():
    # Data
    # data = {
    #     'p_values': [26, 30, 33, 37, 41, 44, 48],
    #     'Exact_Arrond': [13, 13, 13, 15, 15, 15, 15],
    #     'RSSV_Exact_Arrond': [12, 13, 13, 15, 15, 16, 16],
    #     'Exact_EPCI': [13, 15, 14, 18, 15, 19, 20],
    #     'RSSV_Exact_EPCI': [13, 15, 15, 19, 20, 22, 25]
    # }

    data = {
        'p_values': [42, 48, 54, 60, 66, 72, 78],
        'Exact_Arrond':  [15, 16, 15, 16, 17, 16, 17],
        'RSSV_Exact_Arrond': [16, 16, 16, 17, 18, 18, 17],
        'Exact_EPCI': [20, 23, 27, 27, 30, 31, 32],
        'RSSV_Exact_EPCI': [21, 24, 26, 28, 32, 33, 35]
    }


    # Plotting
    plt.figure(figsize=(10, 6))

    # Plotting bars
    plt.bar(data['p_values'], data['Exact_Arrond'], width=0.7, align='center', label='Exact', color='red')
    plt.bar([p + 0.7 for p in data['p_values']], data['RSSV_Exact_Arrond'], width=0.7, align='center', label='RSSV_Exact', color='blue')
    # plt.title('Comparison of Methods with for Maternity and subareas Arrond.')
    plt.title('Comparison of Methods with for Urgency and subareas Arrond.')


    # plt.bar(data['p_values'], data['Exact_EPCI'], width=0.7, align='center', label='Exact', color='red')
    # plt.bar([p + 0.7 for p in data['p_values']], data['RSSV_Exact_EPCI'], width=0.7, align='center', label='RSSV_Exact', color='blue')
    # # plt.title('Comparison of Methods for Maternity  with subareas EPCI')
    # plt.title('Comparison of Methods with for Urgency and subareas EPCI')


    # Adding labels and title
    plt.xlabel('p values')
    plt.ylabel('Number of covered subareas')
    plt.yticks([int(i) for i in plt.yticks()[0]])
    plt.xticks([p + 0.45 for p in data['p_values']], data['p_values'])
    plt.legend()
    plt.legend(loc='upper left')

    #save plot
    # plt.savefig('coverages_mat_arrond.pdf')
    # plt.savefig('coverages_mat_epci.pdf')
    plt.savefig('coverages_urgenc_arrond.pdf')
    # plt.savefig('coverages_urgenc_epci.pdf')
    # Show plot
    #plt.tight_layout()
    # plt.show()


def main():
    print("Main function")
    

    # plot_coverages()


    # services=['mat']
    # # pvalues=[26,30,33,37,41,44,48]
    # services=['urgenc']
    # pvalues=[42,48,54,60,66,72,78]
    # services=['mat']
    # pvalues=[37]
    
    # services=['urgenc']
    # pvalues=[60]
    
    # services=['lycee']
    # pvalues=[352]
    
    # services=['poste']
    # pvalues=[681]

    # coverages=['arrond', 'EPCI', 'canton', 'commune']
    # methods=['RSSV_EXACT_CPMP']

    # create_table_statistics(services,pvalues,coverages,methods)


    # Define the services and their corresponding p-values
    services = ['mat', 'urgenc', 'lycee', 'poste']
    pvalues = [37, 60, 352, 681]

    # Define the coverages and methods
    coverages = ['arrond', 'EPCI', 'canton', 'commune']
    methods = ['RSSV_EXACT_CPMP']

    # Loop through each service and its corresponding p-value
    for service, pvalue in zip(services, pvalues):
        create_table_statistics([service], [pvalue], coverages, methods)


    exit()

    # df_locations.to_csv('output.csv', index=False)


    # Create plot fo x time
    # p=78
    # service='urgenc'
    # path_table = f'./tables/tables_evolution_sol/report_{service}_p_{p}.csv'
    # cover = 'arrond'
    # create_plot_Evolution_Sol(path_table, p, cover)

    # Create comparative plot
    # path_data = './tables/tables_sol/'
    # vet_p = [26]
    # cover = ['arrond', 'epci']
    # create_comparative_Sol(path_data, vet_p, cover)
    # create_plot_comparative_Sol_covers(path_data, vet_p, cover)

    # Plot service solutions
    # path_data = './tables/tables_sol/'
    # csv_file = 'table_cpmp.csv'
    # plot_service_solutions(path_data + csv_file)

    
    # plot cover line
    # path_data = './tables/tables_sol/'
    # csv_file = 'table_cpmp_cover.csv'
    # # desired_methods = ['exact', 'rssv_exact']
    # desired_methods = ['rssv_exact']
    # desired_subareas = ['nan','null','arrond', 'EPCI','canton', 'commune']
    # # desired_subareas = ['nan','null','commune', 'kmeans_commune']
    # # plot_cpmp_cover_service_graphs(path_data + csv_file, desired_methods, desired_subareas)
    # plot_rel_gap_for_exact_method(path_data + csv_file, desired_subareas)




if __name__ == "__main__":
    main()





