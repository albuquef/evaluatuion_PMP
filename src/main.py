import pandas as pd

from create_df import create_df_loc_cust
from graphics_sol import create_plot_Evolution_Sol
from graphics_sol import create_comparative_Sol

def create_table_statistics(services,pvalues,coverages,methods):
    
    columns=['serv','p','cover','method', 'count','mean','std','min','25%','50%','75%','max']
    df_stats = pd.DataFrame(columns=columns)

    df_test_coverages = pd.DataFrame(columns=['serv','p','cover','method', 'num_unique_subareas','num_total_subareas'])
    
    for method in methods:
        for serv in services:
            for pvalue in pvalues:
                for cover in coverages:
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
    
            print(df_stats)
            print(df_test_coverages)


def main():
    print("Main function")
    
    # services=['mat']
    # pvalues=[26,33]
    # coverages=['null']
    # methods=['EXACT_CPMP']

    # create_table_statistics(services,pvalues,coverages,methods)


    # df_locations.to_csv('output.csv', index=False)


    # Create plot fo x time
    # p=26
    # path_table = f'./tables_evolution_sol/report_mat_p_{p}.csv'
    # cover = 'null'
    # create_plot_Evolution_Sol(path_table, p, cover)

    # Create comparative plot
    path_data = './tables/tables_sol/'
    vet_p = [26]
    cover = 'null'
    create_comparative_Sol(path_data, vet_p, cover)





if __name__ == "__main__":
    main()





