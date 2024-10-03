import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Function to read data and plot with optional y-axis adaptation
def plot_sol_form(filepath, adapt_y_axis=False):
    # Reading the dataset
    df = pd.read_csv(filepath)
    
    # Filter for p >= 41
    filtered_df = df[df['p'] >= 41]
    
    # Set up the figure and axes for three subplots side by side
    fig, axs = plt.subplots(1, 3, figsize=(18, 6), sharey=not adapt_y_axis)  # Share y-axis only if adapt_y_axis is False
    
    # Define intervals for p
    intervals = [(41, 61), (96, 326), (500, 1022)]
    titles = ['p in [41, 61]', 'p in [96, 326]', 'p in [500, 1022]']
    
    # Choose a better color palette
    colors = sns.color_palette('Set2')  # A more distinct palette
    # colors = sns.color_palette('Set2')
    colors = sns.color_palette('rocket')
    
    # Plot each interval in a separate subplot
    for i, (p_min, p_max) in enumerate(intervals):
        subset = filtered_df[(filtered_df['p'] >= p_min) & (filtered_df['p'] <= p_max)]
        sns.lineplot(
            x='p', y='Sol_Form', hue='cover', 
            palette=colors, data=subset, marker='o', 
            ax=axs[i], linewidth=2.5, alpha=0.8,  # Line width and transparency
            style='cover'  # Different line styles based on 'cover'
        )
        axs[i].set_title(titles[i])
        axs[i].set_xlabel('p')
        axs[i].grid(True)
    
    # Set a common y-label
    axs[0].set_ylabel('Sum(wi * dij)')
    
    # Rotate x-tick labels for better readability
    for ax in axs:
        ax.set_xticks(sorted(ax.get_lines()[0].get_xdata()))
        ax.set_xticklabels(sorted(ax.get_lines()[0].get_xdata()), rotation=45, ha='right')


    # add title
    plt.suptitle('Sum(wi * dij) vs p for different types of cover - Shuffle Dataset')

    # Adjust the layout and display the plots
    plt.tight_layout()
    plt.show()


# Function to plot number of subareas for different types of cover
def plot_subareas(filepath, adapt_y_axis=False):
    # Read the dataset
    df = pd.read_csv(filepath)
    
    # Filter for p >= 41
    filtered_df = df[df['p'] >= 41]
    
    # Set up the figure and axes for four subplots side by side
    fig, axs = plt.subplots(1, 4, figsize=(20, 6), sharey=not adapt_y_axis)  # Share y-axis unless adapt_y_axis is True
    
    # Define the subareas columns and titles
    subareas_columns = ['#subareas_arrond', '#subareas_EPCI', '#subareas_canton', '#subareas_commune']
    titles = ['Arrond Subareas', 'EPCI Subareas', 'Canton Subareas', 'Commune Subareas']
    
    # Choose a color palette
    # colors = sns.color_palette('Set2')
    colors = sns.color_palette('rocket')
    
    # Plot each subarea type in a separate subplot
    for i, (col, title) in enumerate(zip(subareas_columns, titles)):
        sns.lineplot(
            x='p', y=col, hue='cover', palette=colors, data=filtered_df,
            marker='o', ax=axs[i], linewidth=2.5, alpha=0.8, style='cover'
        )
        axs[i].set_title(title)
        axs[i].set_xlabel('p')
        axs[i].grid(True)
    
    # Set a common y-label
    axs[0].set_ylabel('Number of Subareas')
    
    # Rotate x-tick labels for better readability
    for ax in axs:
        ax.set_xticks(sorted(ax.get_lines()[0].get_xdata()))
        ax.set_xticklabels(sorted(ax.get_lines()[0].get_xdata()), rotation=45, ha='right')

    # Adjust the layout and display the plots
    plt.tight_layout()
    plt.show()


# Function to plot the number of subareas for different types of cover in specified intervals of p
def plot_subareas_by_interval(filepath, adapt_y_axis=False):
    # Read the dataset
    df = pd.read_csv(filepath)
    
    # Set up the figure and axes for three rows, each with four subplots
    fig, axs = plt.subplots(3, 4, figsize=(20, 12), sharey=not adapt_y_axis)  # Share y-axis unless adapt_y_axis is True
    
    # Define the intervals for p
    intervals = [(41, 61), (96, 326), (500, 1022)]
    
    # Define the subareas columns and titles
    subareas_columns = ['#subareas_arrond', '#subareas_EPCI', '#subareas_canton', '#subareas_commune']
    titles = ['Arrond Subareas', 'EPCI Subareas', 'Canton Subareas', 'Commune Subareas']
    
    # Choose a color palette
    # colors = sns.color_palette('Set2')
    colors = sns.color_palette('rocket')
    
    # Plot each interval in a separate row
    for row, (p_min, p_max) in enumerate(intervals):
        subset = df[(df['p'] >= p_min) & (df['p'] <= p_max)]  # Filter based on the interval
        for col, title in zip(subareas_columns, titles):
            sns.lineplot(
                x='p', y=col, hue='cover', palette=colors, data=subset,
                marker='o', ax=axs[row, subareas_columns.index(col)], linewidth=2.5, alpha=0.8, style='cover'
            )
            axs[row, subareas_columns.index(col)].set_title(f'{title} (p in [{p_min}, {p_max}])')
            axs[row, subareas_columns.index(col)].set_xlabel('p')
            axs[row, subareas_columns.index(col)].grid(True)
            axs[row, subareas_columns.index(col)].legend(fontsize='small')  # Reduce legend size

            # Set y-ticks to be discrete integer values
            y_ticks = axs[row, subareas_columns.index(col)].get_yticks()
            axs[row, subareas_columns.index(col)].set_yticks([int(y) for y in y_ticks])  # Ensure y-ticks are integers
    
    # Set a common y-label
    axs[0, 0].set_ylabel('Number of Subareas')
    
    # Rotate x-tick labels for better readability and convert to int
    for ax in axs.flat:
        ax.set_xticks(sorted(ax.get_lines()[0].get_xdata()))
        ax.set_xticklabels([int(x) for x in sorted(ax.get_lines()[0].get_xdata())], rotation=45, ha='right')

    # Adjust the layout and display the plots
    plt.tight_layout()
    plt.show()


# Example usage
# plot_sol_form('table_paca_orginal_dataset.csv', adapt_y_axis=True)
plot_sol_form('table_paca_shuffle_dataset.csv', adapt_y_axis=True)
# plot_subareas('table_paca_orginal_dataset.csv', adapt_y_axis=True)
# plot_subareas_by_interval('table_paca_orginal_dataset.csv', adapt_y_axis=True)