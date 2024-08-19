import pandas as pd
from plot_feature import boxplot_feature

# import csv as dataframe
file_path = '../'+input("Enter the path to the CSV file: ")
df = pd.read_csv(file_path,sep='\t',encoding='utf-8')

# create new column 'catagory', iterate over all rows if the value in 'epoche' is "Romantik" or the value in 'label' startswith 'Romantik', then the value in 'catagory' is "romantik", else the value in 'catagory' is "other"
df['catagory'] = df.apply(lambda x: 'Romantik' if x['epoche'] == 'Romantik' or (x['epoche'] == 'not defined' and x['label'].startswith('Romantik')) else 'Non-Romantik', axis=1)

df['r_acc_1'] = df['n_acc'] / df['n_dat']
df['r_acc_2'] = df['n_acc_doppelt'] / (df['n_dat_doppelt'])

print('r_acc_1')
# print the rows with the maximum and minimum value of the column 'fantasie' where the value in 'catagory' is "Romantik"
print(df.loc[df[df['catagory'] == 'Romantik']['r_acc_1'].idxmax()])
# print the rows with the maximum and minimum value of the column 'fantasie' where the value in 'catagory' is "Non-Romantik"
print(df.loc[df[df['catagory'] == 'Non-Romantik']['r_acc_1'].idxmax()])

boxplot_feature(df, 'r_acc_1', 'l_003_r_acc_1.png', 'Relation von akkusativ zu dativ Präpositionen', 0.05)

print('r_acc_2')
# print the rows with the maximum and minimum value of the column 'fantasie' where the value in 'catagory' is "Romantik"
print(df.loc[df[df['catagory'] == 'Romantik']['r_acc_2'].idxmax()])
# print the rows with the maximum and minimum value of the column 'fantasie' where the value in 'catagory' is "Non-Romantik"
print(df.loc[df[df['catagory'] == 'Non-Romantik']['r_acc_2'].idxmax()])

boxplot_feature(df, 'r_acc_2', 'l_003_r_acc_2.png', 'Relation von akkusativ zu dativ Doppelpräpositionen', 0.12)