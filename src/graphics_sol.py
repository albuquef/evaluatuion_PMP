
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def create_plot_comparative_Sol_covers(path_data, vet_p, cover):

    df_results_cover=pd.read_csv(path_data+'table_cpmp_cover.csv')
    df_results_cover=df_results_cover.sort_values(by='P').reset_index(drop=True)

    for serv in ['mat', 'urgenc']:
        #for suba in cover: #['arrond', 'epci']:
        
        p_values=df_results_cover[(df_results_cover.SERVICE == serv) & (df_results_cover.METHOD == 'exact') & (df_results_cover.SUBAREA == cover[0])].P
        sol_exact_cover_1=df_results_cover[(df_results_cover.SERVICE == serv) & (df_results_cover.METHOD == 'exact') & (df_results_cover.SUBAREA == cover[0])].SOLUTION
        sol_rssv_exact_cover_1=df_results_cover[(df_results_cover.SERVICE == serv) & (df_results_cover.METHOD == 'rssv_exact') & (df_results_cover.SUBAREA == cover[0])].SOLUTION
        sol_exact_cover_2=df_results_cover[(df_results_cover.SERVICE == serv) & (df_results_cover.METHOD == 'exact') & (df_results_cover.SUBAREA == cover[1])].SOLUTION
        sol_rssv_exact_cover_2=df_results_cover[(df_results_cover.SERVICE == serv) & (df_results_cover.METHOD == 'rssv_exact') & (df_results_cover.SUBAREA == cover[1])].SOLUTION


        # Plot points and line with the same color
        plt.plot(p_values, sol_exact_cover_1, color='red', marker='s', linestyle='-', label=f'Exact_{cover[0]}')
        plt.plot(p_values, sol_rssv_exact_cover_1, color='blue', marker='s', linestyle='-', label=f'RSSV-Exact_{cover[0]}')

        plt.plot(p_values, sol_exact_cover_2, color='red', marker='^', linestyle='-', label=f'Exact_{cover[1]}')
        plt.plot(p_values, sol_rssv_exact_cover_2, color='blue', marker='^', linestyle='-', label=f'RSSV-Exact_{cover[1]}')

        # Add labels and title
        plt.xlabel('Values of p')
        plt.ylabel('Solution value')
        # if suba!="null": plt.title(f'Solutions with differents values of p: {serv} | {suba}')
    # else:
        plt.title(f'Solutions with differents values of p: {serv} | {cover[0]} and {cover[1]}')
        plt.xticks(p_values)
        plt.legend()
        plt.savefig(f'plots/{serv}_plot_cover_{cover[0]}_{cover[1]}.pdf')

        plt.show()

def create_comparative_Sol(path_data, vet_p, cover):

    df_results=pd.read_csv(path_data+'table_cpmp.csv')
    df_results_cover=pd.read_csv(path_data+'table_cpmp_cover.csv')
    df_results=df_results.sort_values(by='P').reset_index(drop=True)
    df_results_cover=df_results_cover.sort_values(by='P').reset_index(drop=True)

    for serv in ['mat', 'urgenc', 'lycee', 'poste']:
        for suba in cover: #['arrond', 'epci']:
            # p_values=df_results_cover[(df_results_cover.SERVICE == serv) & (df_results_cover.METHOD == 'exact') & (df_results_cover.SUBAREA == suba)].P
            p_values=df_results[(df_results.SERVICE == serv) & (df_results.METHOD == 'exact')].P
            # print(p_values)
            sol_exact=df_results[(df_results.SERVICE == serv) & (df_results.METHOD == 'exact') & (df_results.P.isin(p_values))].SOLUTION
            sol_rssv_exact=df_results[(df_results.SERVICE == serv) & (df_results.METHOD == 'rssv_exact') & (df_results.P.isin(p_values))].SOLUTION
            sol_exact_cover=df_results_cover[(df_results_cover.SERVICE == serv) & (df_results_cover.METHOD == 'exact') & (df_results_cover.SUBAREA == suba)].SOLUTION
            sol_rssv_exact_cover=df_results_cover[(df_results_cover.SERVICE == serv) & (df_results_cover.METHOD == 'rssv_exact') & (df_results_cover.SUBAREA == suba)].SOLUTION


            # Plot points and line with the same color
            # plt.plot(p_values, sol_exact, color='red', marker='o', ls='-', label='Exact')
            # plt.plot(p_values, sol_rssv_exact, color='blue', marker='o', ls='-', label='RSSV-Exact')

            plt.plot(p_values, sol_exact_cover, color='red', marker='o', linestyle='-', label=f'Exact_{suba}')
            plt.plot(p_values, sol_rssv_exact_cover, color='blue', marker='o', linestyle='-', label=f'RSSV-Exact_{suba}')

            # Add labels and title
            plt.xlabel('Values of p')
            plt.ylabel('Solution value')
            if suba!="null": plt.title(f'Solutions with differents values of p: {serv} | {suba}')
            else: plt.title(f'Solutions with differents values of p: {serv}')
            plt.xticks(p_values) 
            # Add legend
            plt.legend()
            # Save the plot as a PDF file
            if suba!="null": plt.savefig(f'plots/{serv}_plot_cover_{suba}.pdf')
            else: plt.savefig(f'plots/{serv}_plot.pdf')
            # Show plot
            plt.show()
            
def create_plot_Evolution_Sol(path_table, p, cover):

    # Read the data from a CSV file
    df = pd.read_csv(path_table)
    # p = 26
    # cover = 'null'

    # df.plot(x='time_exact', y='sol_exact', kind='line')
    # plt.plot(df.exact_time, df.exact_sol, color='red', label='Exact',linestyle="--")
    plt.plot(df.exact_TL_time, df.exact_TL_sol, color='red', label='Exact')
    plt.plot(df.rssv_tbPMP_exact_time+300, df.rssv_tbPMP_exact_sol, color='blue', label='RSSV-exact')
    # plt.plot(df.rssv_tbPMP_exact_vns_time, df.rssv_tbPMP_exact_vns_sol, color='green', label='RSSV-exact-vns')


    # Add labels and legend
    plt.xlabel('Real Time')
    plt.ylabel('FO')
    plt.legend()

    # Add a title
    if (cover!= "null"): plt.title(f'Urgency p = {p} cover {cover}')
    else: plt.title(f'Urgency p = {p}')


    # Save the plot as a PDF file
    if (cover!= "null"): plt.savefig(f'plots/maternity_ESplot_p_{p}_{cover}.pdf')
    else : plt.savefig(f'plots/urgency_ESplot_p_{p}.pdf')


    # Show the plot (optional)
    # plt.show()
    
def create_violin_plot(all_data_assigments):

    # Create violin plots
    for service in all_data_assigments['service'].unique():
        plt.figure(figsize=(12, 8))
        service_data = all_data_assigments[all_data_assigments['service'] == service]
        
        sns.violinplot(x='coverage', y='weighted_distance', data=service_data)
        plt.title(f'Violin Plot for Service: {service}')
        plt.xlabel('Coverage Type')
        plt.ylabel('weighted_distance')
        plt.xticks(rotation=45)
        plt.grid(True)
        
        plt.savefig(f'./plots/violin_plots/violin_plot_{service}.pdf', bbox_inches='tight')
        plt.show()

    for service in all_data_assigments['service'].unique():
        plt.figure(figsize=(12, 8))
        service_data = all_data_assigments[all_data_assigments['service'] == service]
        
        sns.violinplot(x='coverage', y='weighted_distance', data=service_data, inner=None)  # Set inner to None to remove the inner box plot
        sns.stripplot(x='coverage', y='weighted_distance', data=service_data, color='k', alpha=0.5, jitter=True)  # Add the points
        
        plt.title(f'Violin Plot for Service: {service}')
        plt.xlabel('Coverage Type')
        plt.ylabel('weighted_distance')
        plt.xticks(rotation=45)
        plt.grid(True)
        
        plt.savefig(f'./plots/violin_plots/violin_plot_point_{service}.pdf', bbox_inches='tight')
        plt.show()