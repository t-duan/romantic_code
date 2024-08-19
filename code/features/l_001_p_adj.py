import pandas as pd
from plot_feature import boxplot_feature

# import csv as dataframe
file_path = '../'+input("Enter the path to the CSV file: ")
df = pd.read_csv(file_path,sep='\t',encoding='utf-8')

# create new column 'catagory', iterate over all rows if the value in 'epoche' is "Romantik" or the value in 'label' startswith 'Romantik', then the value in 'catagory' is "romantik", else the value in 'catagory' is "other"
df['catagory'] = df.apply(lambda x: 'Romantik' if x['epoche'] == 'Romantik' or (x['epoche'] == 'not defined' and x['label'].startswith('Romantik')) else 'Non-Romantik', axis=1)

# create new column 'p_adja', the value is division of 'n_tok_no_punct' and 'n_adja'
df['p_adja'] = df['n_adja'] / df['n_tok_no_punct']
df['p_adja_nn'] = df['n_adja'] / df['n_nn']

# Create boxplot for 'p_adja'
boxplot_feature(df, 'p_adja', 'l_001_p_adja.png', 'Anteil der Adjektive an allen Tokens ohne Satzzeichen', 0.001)
boxplot_feature(df, 'p_adja_nn', 'l_001_p_adja_nn.png', 'Relation von Adjektiven zu Substantiven', 0.006)