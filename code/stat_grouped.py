import pandas as pd

def process_dataframe(csv_path, group_column=['epoche'], value_column='n_tok'):
    """
    Processes the CSV file to group by a specified column and aggregate data.

    Parameters:
    csv_path (str): The path to the CSV file to be processed.
    group_column (str): The column to group the data by.
    value_column (str): The column to sum up during aggregation.

    Returns:
    pd.DataFrame: A DataFrame with aggregated data by the specified group.
    int: Total sum of the value column across all groups.
    int: Total number of rows across all groups.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path, sep='\t')
    df = df[df['label'] == 'not defined']

    # Check if the necessary columns are present
    #if group_column not in df.columns or value_column not in df.columns:
     #   raise ValueError(f"Required columns '{group_column}' or '{value_column}' are missing in the CSV file.")

    # Group by the specified column, count rows, and sum the value column
    grouped = df.groupby(group_column).agg(
        count=('textPath', 'count'),  # Counting the number of rows in each group
        total_tokens=(value_column, 'sum')  # Summing the values in the specified column
    )

    # Calculate the total sum of the value column across all groups
    total_sum = df[value_column].sum()
    total_rows = df.shape[0]

    return grouped, total_rows, total_sum

if __name__ == "__main__":
    # Example usage
    csv_path = 'meta_20240605.csv'  # Replace this with your actual CSV file path
    summary_df, total_rows, total_sum = process_dataframe(csv_path)
    print(summary_df)
    print(f"Total number of rows across all categories:", total_rows)
    print(f"Total sum of '{summary_df.columns[1]}':", total_sum)  # Displaying the name of the summed column