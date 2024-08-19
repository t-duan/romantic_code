import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def boxplot_feature(df, feat_name, output_path, label_y, position_adjustment_vertical):

    # Define the order of categories explicitly
    category_order = ['Romantik', 'Non-Romantik']

    # Create the boxplot using seaborn
    plt.figure(figsize=(10, 6))

    sns.boxplot(x='catagory', y=feat_name, data=df, showmeans=True, 
                meanprops={"marker":".", "markerfacecolor":"red", "markeredgecolor":"red", "markersize":"5"},
                boxprops=dict(facecolor=(0, 0, 0, 0), edgecolor='black'),  # Transparent box fill
                whiskerprops=dict(color='black'),
                capprops=dict(color='black'),
                medianprops=dict(color='blue'),
                order=category_order)  # Set order of categories

    plt.ylabel(label_y)
    plt.xlabel('')

    # Use tight_layout to automatically adjust the layout
    plt.tight_layout()

    # Calculate and plot means and medians with different vertical alignment
    means = df.groupby('catagory')[feat_name].mean()
    medians = df.groupby('catagory')[feat_name].median()
    max = df.groupby('catagory')[feat_name].max()
    min = df.groupby('catagory')[feat_name].min()

    for i, cat in enumerate(category_order):
        print(f'{cat}:')
        print(f'mean: {means[cat]}, median: {medians[cat]}')
        print(f'max: {max[cat]}, min: {min[cat]}')
        if means[cat] > medians[cat]:
            plt.text(i, means[cat] + position_adjustment_vertical, f'Durchschnitt: {means[cat]:.4f}', 
                     horizontalalignment='center', color='red', verticalalignment='bottom')
            plt.text(i, medians[cat] - position_adjustment_vertical, f'Mittelwert: {medians[cat]:.4f}', 
                     horizontalalignment='center', color='blue', verticalalignment='top')
        else:
            plt.text(i, means[cat] - position_adjustment_vertical, f'Durchschnitt: {means[cat]:.4f}', 
                     horizontalalignment='center', color='red', verticalalignment='top')
            plt.text(i, medians[cat] + position_adjustment_vertical, f'Mittelwert: {medians[cat]:.4f}', 
                     horizontalalignment='center', color='blue', verticalalignment='bottom')
    plt.savefig(output_path)