import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def clean_and_convert(value):
    if pd.isnull(value):  
        return np.nan
    elif isinstance(value, str):  # Check if value is a string
        if value == '−':  # Replace "−" with NaN
            return np.nan
        else: 
            return float(value.replace(',', '.'))
    else:  
        return value

def load_and_filter_data(file_path, method, method_column='Method', instance_column='instance'):
    data = pd.read_csv(file_path, delimiter=';')
    data = data[data[method_column] == method]
    data['solution'] = data['solution'].apply(clean_and_convert)
    return data

def prepare_and_sort_data(data, filter_instances, instance_column='instance'):
    data[instance_column] = pd.Categorical(data[instance_column], categories=filter_instances, ordered=True)
    data = data[data[instance_column].isin(filter_instances)].sort_values(instance_column)
    data = data.groupby([instance_column, 'Method']).agg({'solution': 'min'}).reset_index()
    return data

def plot_results(results_list, labels, instance_column='instance'):
    plt.figure(figsize=(12, 6))
    for results, label in zip(results_list, labels):
        plt.plot(results[instance_column], results['solution'], 'o-', label=label)
    plt.title('Comparison of the Results')
    plt.xlabel('Instance')
    plt.xticks(rotation=45)
    plt.ylabel('Solution')
    plt.legend()
    plt.tight_layout()
    plt.savefig('./outputs/plot_results.png')
    plt.show()

def main():
    # filter_instances = ['lin318_005', 'lin318_015', 'lin318_040', 'lin318_070', 'lin318_100', 
    #                     'ali535_005', 'ali535_025', 'ali535_050', 'ali535_100', 'ali535_150', 
    #                     'u724_010', 'u724_030', 'u724_075', 'u724_125', 'u724_200', 
    #                     'rl1304_010', 'rl1304_050', 'rl1304_100', 'rl1304_200', 'rl1304_300']
    # filter_instances = ['SJC1', 'SJC2', 'SJC3a', 'SJC3b', 'SJC4a', 'SJC4b']
    # filter_instances = ['lin318_005', 'lin318_015', 'lin318_040', 'lin318_070', 'lin318_100']
    # filter_instances = [ 'ali535_005', 'ali535_025', 'ali535_050', 'ali535_100', 'ali535_150']
    # filter_instances = ['u724_010', 'u724_030', 'u724_075', 'u724_125', 'u724_200']
    # filter_instances = ['rl1304_010', 'rl1304_050', 'rl1304_100', 'rl1304_200', 'rl1304_300']
    # filter_instances = ['pr2392_020', 'pr2392_075', 'pr2392_150', 'pr2392_300', 'pr2392_500']
    # filter_instances = ['fnl4461_0020', 'fnl4461_0100', 'fnl4461_0250', 'fnl4461_0500', 'fnl4461_1000']
    # filter_instances = ['p3038_600', 'p3038_700', 'p3038_800', 'p3038_900', 'p3038_1000']
    filter_instances = ['fnl4461_0020', 'fnl4461_0100', 'fnl4461_0250', 'fnl4461_0500', 'fnl4461_1000']



    results_mario21 = load_and_filter_data('./tables/tables_general/results_mario21.csv', 'Mario_21')
    results_stef_mario21 = load_and_filter_data('./tables/tables_general/results_mario21.csv', 'Mario_Stef_21')
    results_stefanello15 = load_and_filter_data('./tables/tables_general/results_stefanello15.csv', 'Stef_15')
    results_cplex = load_and_filter_data('./tables/tables_general/test_all_results.csv', 'EXACT_CPMP_BIN', instance_column='type_service')
    
    # results_rssv_2 = load_and_filter_data('/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/savecluster_Literature/24-06-20_save_cluster_128G_without_mipstart_weighted_subTBPMP/outputs/solutions/2024-06-20_LIT/Results_cplex/results_all_cplex.csv', 'RSSV_EXACT_CPMP_BIN', instance_column='type_service')
    # results_rssv_2 = load_and_filter_data('/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/24-06-24_save_cluster/Literature_test_2/outputs/solutions/2024-06-24_LIT/Results_cplex/results_all_cplex.csv', 'RSSV_EXACT_CPMP_BIN', instance_column='type_service')
    # results_rssv_2 = load_and_filter_data('/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/24-06-24_save_cluster/Literature_test_2/outputs/solutions/2024-06-24_LIT/Results_cplex/results_all_cplex.csv', 'RSSV_EXACT_CPMP_BIN', instance_column='type_service')
    # results_rssv_3 = load_and_filter_data('/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/24-06-26_save_cluster/test_h_bandwidth_smaller/hx05/outputs/solutions/2024-06-25_LIT/Results_cplex/results_all_cplex.csv', 'RSSV_EXACT_CPMP_BIN', instance_column='type_service')
    # results_rssv_4 = load_and_filter_data('/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/24-06-26_save_cluster/test_h_bandwidth_smaller/hx04/outputs/solutions/2024-06-25_LIT_hx04/Results_cplex/results_all_cplex.csv', 'RSSV_EXACT_CPMP_BIN', instance_column='type_service')

    results_rssv = load_and_filter_data('/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/24-07-15_save_cluster/test_code/outputs/solutions/2024-07-14_LIT/Results_cplex/results_all_cplex.csv', 'RSSV_EXACT_CPMP_BIN', instance_column='type_service')
    results_rssv_2 = load_and_filter_data('/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/24-07-16_save_cluster/test/outputs/solutions/2024-07-15_LIT_bestbound/Results_cplex/results_all_cplex_postopt.csv', 'RSSV_EXACT_CPMP_BIN', instance_column='type_service')
    results_rssv_3 = load_and_filter_data('/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/24-07-16_save_cluster/test/outputs/solutions/2024-07-15_LIT_bestbound/Results_cplex/results_all_cplex.csv', 'RSSV_EXACT_CPMP_BIN', instance_column='type_service')
    # results_rssv_4 = load_and_filter_data('/home/falbuquerque/Documents/projects/Project_PMP/saves/SaveCluster/24-07-09_save_cluster/test_lit_hx010_first/outputs/solutions/2024-07-09_LIT_hx01/Results_cplex/results_all_cplex.csv', 'RSSV_EXACT_CPMP_BIN', instance_column='type_service')
    
    # results_rssv_4 = load_and_filter_data('', 'RSSV_EXACT_CPMP_BIN', instance_column='type_service')






    results_mario21 = prepare_and_sort_data(results_mario21, filter_instances)
    results_stef_mario21 = prepare_and_sort_data(results_stef_mario21, filter_instances)
    results_stefanello15 = prepare_and_sort_data(results_stefanello15, filter_instances)
    results_cplex = prepare_and_sort_data(results_cplex, filter_instances, instance_column='type_service')
    results_rssv = prepare_and_sort_data(results_rssv, filter_instances, instance_column='type_service')
    results_rssv_2 = prepare_and_sort_data(results_rssv_2, filter_instances, instance_column='type_service')
    results_rssv_3 = prepare_and_sort_data(results_rssv_3, filter_instances, instance_column='type_service')
    # results_rssv_4 = prepare_and_sort_data(results_rssv_4, filter_instances, instance_column='type_service')

    # Rename 'type_service' to 'instance' in CPLEX results for uniformity
    results_cplex.rename(columns={'type_service': 'instance'}, inplace=True)
    results_rssv.rename(columns={'type_service': 'instance'}, inplace=True)
    results_rssv_2.rename(columns={'type_service': 'instance'}, inplace=True)
    results_rssv_3.rename(columns={'type_service': 'instance'}, inplace=True)
    # results_rssv_4.rename(columns={'type_service': 'instance'}, inplace=True)

    # Debug prints to verify sorting add time column
    print("Results Mario21:")
    print(results_mario21[['instance', 'solution']])
    print("\nResults Stef_Mario21:")
    print(results_stef_mario21[['instance', 'solution']])
    print("\nResults Stefanello15:")
    print(results_stefanello15[['instance', 'solution']])
    print("\nResults CPLEX:")
    print(results_cplex[['instance', 'solution']])
    # print("\nResults RSSV:")    
    # print(results_rssv[['instance', 'solution']])
    print("\nResults RSSV:")    
    print(results_rssv_3[['instance', 'solution']])
    print("\nResults RSSV + postopt:")
    print(results_rssv_2[['instance', 'solution']])
    # print("\nResults RSSV + postopt 5 neighb:")
    # print(results_rssv_3[['instance', 'solution']])
    # print("\nResults RSSV_hx0.1:")
    # print(results_rssv_4[['instance', 'solution']])

    # plot_results([results_mario21, results_stefanello15, results_cplex, results_rssv], 
    #              ['Mario21', 'Stefanello15', 'CPLEX', 'RSSV'], instance_column='instance')
    plot_results([results_mario21, results_stef_mario21, results_stefanello15, results_cplex, results_rssv_3, results_rssv_2], 
                 ['Mario21', 'Stef_mario21', 'Stefanello15', 'CPLEX', 'RSSV', 'RSSV_postopt'], instance_column='instance')
    # plot_results([results_mario21, results_stef_mario21, results_stefanello15, results_cplex, results_rssv, results_rssv_3], 
    #              ['Mario21', 'Stef_mario21', 'Stefanello15', 'CPLEX', 'RSSV_Hx0,5', 'RSSV_Hx0.25'], instance_column='instance')
    # plot_results([results_stefanello15, results_cplex, results_rssv, results_rssv_2, results_rssv_3, results_rssv_4], 
    #             ['Stefanello15', 'CPLEX', 'RSSV', 'RSSV_hx2', 'RSSV_hx0.5', 'RSSV_hx0.4'], instance_column='instance')
    # plot_results([results_stefanello15, results_cplex, results_rssv, results_rssv_2, results_rssv_3, results_rssv_4], 
    #             ['Stefanello15', 'CPLEX', 'RSSV', 'RSSV_hx2', 'RSSV_hx0.5', 'RSSV_hx0.4'], instance_column='instance')
    # plot_results([results_stefanello15, results_cplex], 
    #             ['Stefanello15', 'CPLEX'], instance_column='instance')    
        # plot_results([results_cplex, results_rssv], 
    #             ['CPLEX', 'RSSV'], instance_column='instance')

if __name__ == "__main__":
    main()
