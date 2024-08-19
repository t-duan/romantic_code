import pandas as pd
from plot_feature import boxplot_feature

# import csv as dataframe
file_path = '../'+input("Enter the path to the CSV file: ")
df = pd.read_csv(file_path,sep='\t',encoding='utf-8')

# create new column 'catagory', iterate over all rows if the value in 'epoche' is "Romantik" or the value in 'label' startswith 'Romantik', then the value in 'catagory' is "romantik", else the value in 'catagory' is "other"
df['catagory'] = df.apply(lambda x: 'Romantik' if x['epoche'] == 'Romantik' or (x['epoche'] == 'not defined' and x['label'].startswith('Romantik')) else 'Non-Romantik', axis=1)

df['fantasie'] = df['n_konj_vf'] / df['n_vfin']
df['fantasie_2'] = df['fantasie'] * df['n_vv'] / (df['n_v']-df['n_vv'])

print('n_konj_vf / n_vfin')
# print the rows with the maximum and minimum value of the column 'fantasie' where the value in 'catagory' is "Romantik"
print(df.loc[df[df['catagory'] == 'Romantik']['fantasie'].idxmax()])
# print the rows with the maximum and minimum value of the column 'fantasie' where the value in 'catagory' is "Non-Romantik"
print(df.loc[df[df['catagory'] == 'Non-Romantik']['fantasie'].idxmax()])

boxplot_feature(df, 'fantasie', 'l_002_p_konj_vf.png', 'Relation von Konjunktiv II zu finiten Verben', 0.0006)

print('n_konj_vf / n_vvfin')
# print the rows with the maximum and minimum value of the column 'fantasie' where the value in 'catagory' is "Romantik"
print(df.loc[df[df['catagory'] == 'Romantik']['fantasie_2'].idxmax()])
# print the rows with the maximum and minimum value of the column 'fantasie' where the value in 'catagory' is "Non-Romantik"
print(df.loc[df[df['catagory'] == 'Non-Romantik']['fantasie_2'].idxmax()])

boxplot_feature(df, 'fantasie_2', 'l_002_p_konj_vf2.png', 'Relation von Konjunktiv II zu finiten Vollverben', 0.0006)