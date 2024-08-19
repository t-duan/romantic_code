import pandas as pd

file_path = input('Enter the file path: ')

df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
# get statistics of the column 'n_sent'
print(df['n_sent'].describe())
print(df['n_sent'].quantile(0.05))
print(df['n_sent'].quantile(0.95))

# get statistics of the column 'n_tok_no_punct'
print(df['n_tok_no_punct'].describe())
print(df['n_tok_no_punct'].quantile(0.05))
print(df['n_tok_no_punct'].quantile(0.95))

print(df['n_tok_no_punct'].sum()/df['n_sent'].sum())