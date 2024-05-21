import pandas as pd
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




def create_table_statistics(services,pvalues,coverages,methods):
    
    columns=['serv','p','cover','method', 'count','mean','std','min','25%','50%','75%','max']
    df_stats = pd.DataFrame(columns=columns)

    df_test_coverages = pd.DataFrame(columns=['serv','p','cover','method', 'num_unique_subareas','num_total_subareas'])
    
    for method in methods:
        for serv in services:
            for cover in coverages:
                for pvalue in pvalues:
                    id_path = f'./tables/tables_id/map_id_cust_loc.txt'
                    dist_path = f'./tables/tables_dist/dist_matrix_minutes.txt'
                    txt_path = f'./tables/tables_assign/test_paca_{serv}_{cover}_p_{pvalue}_{method}.txt'    
                    df_locations, df_assignment = create_df_loc_cust(id_path, dist_path, txt_path)
                    # print("Location Usages:")
                    # print(df_locations)
                    # print("\nCustomer Assignments:")
                    # print(df_assignment)
                    # print("Statistics about distance:")
                    # print(df_assignment['distance'].describe())

                    df_stats.loc[len(df_stats)] = [serv,pvalue,cover,method] + df_assignment['distance'].describe().tolist()
    
                    
                    txt_coverages = f'./tables/tables_coverages/loc_coverages_{cover}.txt'
                    if cover == 'null':
                        txt_coverages = f'./tables/tables_coverages/loc_coverages_arrond.txt'

                    subarea_data = pd.read_csv(txt_coverages, sep=' ')
                    num_total_subareas = subarea_data['subarea'].nunique() # Count the number total of unique subareas
                    # Filter subarea data for locations present in df_locations
                    subarea_data_filtered = subarea_data[subarea_data['location'].isin(df_locations['location'])]
                    num_unique_subareas = subarea_data_filtered['subarea'].nunique() # Count the number of unique subareas covered
                    # print(f"Number of unique subareas covered: {num_unique_subareas} / {num_total_subareas}")  
                    
                    df_test_coverages.loc[len(df_test_coverages)] = [serv,pvalue,cover,method, num_unique_subareas,num_total_subareas]
    
        df_stats.to_csv(f'df_stats_{method}.csv', index=False, mode='a')
        df_test_coverages.to_csv(f'df_count_coverages_{method}.csv', index=False, mode='a')


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
    # pvalues=[26,30,33,37,41,44,48]
    
    # services=['urgenc']
    # pvalues=[42,48,54,60,66,72,78]

    # coverages=['null']
    # methods=['RSSV_EXACT_CPMP']

    # create_table_statistics(services,pvalues,coverages,methods)


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
    path_data = './tables/tables_sol/'
    csv_file = 'table_cpmp.csv'
    plot_service_solutions(path_data + csv_file)





if __name__ == "__main__":
    main()





