
import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np


def create_comparative_Sol(path_data, vet_p, cover):

    df_results=pd.read_csv(path_data+'table_cpmp.csv')
    df_results_cover=pd.read_csv(path_data+'table_cpmp_cover.csv')
    df_results=df_results.sort_values(by='P').reset_index(drop=True)
    df_results_cover=df_results_cover.sort_values(by='P').reset_index(drop=True)

    for serv in ['mat', 'urgenc']:
        for suba in ["null"]: #['arrond', 'epci']:
            # p_values=df_results_cover[(df_results_cover.SERVICE == serv) & (df_results_cover.METHOD == 'exact') & (df_results_cover.SUBAREA == suba)].P
            p_values=df_results[(df_results.SERVICE == serv) & (df_results.METHOD == 'exact')].P
            # print(p_values)
            sol_exact=df_results[(df_results.SERVICE == serv) & (df_results.METHOD == 'exact') & (df_results.P.isin(p_values))].SOLUTION
            sol_rssv_exact=df_results[(df_results.SERVICE == serv) & (df_results.METHOD == 'rssv_exact') & (df_results.P.isin(p_values))].SOLUTION
            # sol_exact_cover=df_results_cover[(df_results_cover.SERVICE == serv) & (df_results_cover.METHOD == 'exact') & (df_results_cover.SUBAREA == suba)].SOLUTION
            # sol_rssv_exact_cover=df_results_cover[(df_results_cover.SERVICE == serv) & (df_results_cover.METHOD == 'rssv_exact') & (df_results_cover.SUBAREA == suba)].SOLUTION


            # Plot points and line with the same color
            # plt.plot(p_values, sol_exact, color='red', marker='o', ls='--', label='Exact')
            # plt.plot(p_values, sol_rssv_exact, color='blue', marker='o', ls='--', label='RSSV-Exact')

            plt.plot(p_values, sol_exact, color='red', marker='o', linestyle='-', label='Exact_cover')
            plt.plot(p_values, sol_rssv_exact, color='blue', marker='o', linestyle='-', label='RSSV-Exact_cover')

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
    plt.plot(df.rssv_tbPMP_exact_time+600, df.rssv_tbPMP_exact_sol, color='blue', label='RSSV-exact')
    # plt.plot(df.rssv_tbPMP_exact_vns_time, df.rssv_tbPMP_exact_vns_sol, color='green', label='RSSV-exact-vns')


    # Add labels and legend
    plt.xlabel('Real Time')
    plt.ylabel('FO')
    plt.legend()

    # Add a title
    if (cover!= "null"): plt.title(f'Maternity p = {p} cover {cover}')
    else: plt.title(f'Maternity p = {p}')


    # Save the plot as a PDF file
    if (cover!= "null"): plt.savefig(f'plots/maternity_ESplot_p_{p}_{cover}.pdf')
    else : plt.savefig(f'plots/maternity_ESplot_p_{p}.pdf')


    # Show the plot (optional)
    # plt.show()