import os
import pandas as pd
from fuzzywuzzy import fuzz

def generate_populationtable(df, target_col, columns):
    """
    Generate a population table for the given column in the DataFrame.
    
    :param df: DataFrame 
    :param target_col: The column whose unique values will serve as rows in the result
    :param columns: List of columns to calculate the percentage of non-null values
    :return: A DataFrame where each row corresponds to a unique value in target_col,
             and each column is the percentage of non-nulls for the specified columns
    """
    
    # Initialize an empty list to store the population data
    population_data = []
    
    # Get the unique values in the target column
    unique_values = df[target_col].unique()
    
    for value in unique_values:
        value_data = df[df[target_col] == value]
        
        # Finding the percentage of non-null values for each specified column
        percentages = value_data[columns].notnull().mean() * 100
        
        # Create a dictionary with the value of target_col as the first entry
        # and the percentages as the remaining entries
        row_data = {target_col: value}
        row_data.update(percentages.to_dict())
        
        # Append this dictionary to population_data
        population_data.append(row_data)
    
    # Convert the list of dictionaries into a DataFrame
    population_table = pd.DataFrame(population_data)
    
    return population_table

def highlight_nans(df):
    """
    Print a DataFrame to the terminal, highlighting NaNs in red.
    :param df: DataFrame to print
    """
    # ANSI color code strings
    RED = '\033[91m'
    END = '\033[0m'
    
    # Make sure column names are strings
    df.columns = df.columns.map(str)
    
    # Find the maximum width for each column
    col_widths = df.applymap(lambda x: len(str(x))).max()
    
    # Create and print the column names row
    header_row = ""
    for j, col_name in enumerate(df.columns):
        header_row += f"{col_name[7:-2]:>{col_widths[j]}} "
    print(header_row)
    
    # Print a horizontal line separating the column names and data
    print('-' * (sum(col_widths) + len(col_widths)))

    # Create a formatted string with spacing for each row
    for i, row in df.iterrows():
        formatted_row = ""
        for j, val in enumerate(row):
            val_str = str(val)
            if pd.isna(val):
                formatted_row += f"{RED}{'NaN':>{col_widths[j]}}{END} "
            else:
                formatted_row += f"{val_str:>{col_widths[j]}} "
        print(formatted_row)
        
    print()
def is_numeric(val):
    """
    Check if the value is numeric (int or float)
    """
    return isinstance(val, (int, float))

def color_df(df):
    """
    Print a DataFrame to the terminal, highlighting 
    0-50:red, 50-70:orange, 70-90:yellow, 90-100:green
    
    :param df: DataFrame to print
    """
    # ANSI color code strings
    RED = '\033[91m'
    ORANGE = '\033[93m'
    YELLOW = '\033[92m'
    GREEN = '\033[94m'
    END = '\033[0m'
    
    # Find the maximum width for each column
    col_widths = df.applymap(lambda x: len(str(x))).max()
    
    # Create a formatted string with spacing for each row
    for i, row in df.iterrows():
        formatted_row = ""
        for j, val in enumerate(row):
            if pd.isna(val):
                formatted_row += f"{'NaN':>{col_widths[j]}} "
            elif is_numeric(val):
                if val >= 0 and val < 50:
                    formatted_row += f"{RED}{val:>{col_widths[j]}}{END} "
                elif val >= 50 and val < 70:
                    formatted_row += f"{ORANGE}{val:>{col_widths[j]}}{END} "
                elif val >= 70 and val < 90:
                    formatted_row += f"{YELLOW}{val:>{col_widths[j]}}{END} "
                elif val >= 90 and val <= 100:
                    formatted_row += f"{GREEN}{val:>{col_widths[j]}}{END} "
                else:
                    formatted_row += f"{val:>{col_widths[j]}} "
            else:
                formatted_row += f"{val:>{col_widths[j]}} "
        print(formatted_row)

    print()


def side_by_side(df_g, df_m, g_col='callsign', m_col='callsign'):
    
    # Check for duplicate values in the index columns of both DataFrames
    if not df_g[g_col].is_unique or not df_m[m_col].is_unique:
        print("Warning: The index columns have duplicate values.")
        
        # Create a new unique index for both DataFrames
        df_g['new_index'] = range(1, len(df_g) + 1)
        df_m['new_index'] = range(1, len(df_m) + 1)
        
        g_col = 'new_index'
        m_col = 'new_index'

    # Now, set the index and concatenate
    df_all = pd.concat([df_g.set_index(g_col), df_m.set_index(m_col)], axis='columns', keys=['G', 'M'])
    
    def highlight_diff(data, color='yellow'):
        attr = 'background-color: {}'.format(color)
        other = data.xs('G', axis='columns', level=-1)
        return pd.DataFrame(np.where(data.ne(other, level=0), attr, ''),
                            index=data.index, columns=data.columns)

    # df_all.style.apply(highlight_diff, axis=None)
    return df_all

def find_potential_misspelled_names(df,col='name',similarity_threshold=95):
    # Compare each row with every other row
    num_rows = len(df)
    for i in range(num_rows):
        for j in range(i+1, num_rows):
            row1 = df.loc[i]
            row2 = df.loc[j]
            
            # Skip if the one of the names is empty
            if pd.isnull(row1[col]) or pd.isnull(row2[col]):
                continue

            # Skip if the rows are the same
            if row1[col] == row2[col]:
                continue
            
            # Remove numbers from both strings
            str1 = ''.join(filter(lambda x: not x.isdigit(), row1[col]))
            str2 = ''.join(filter(lambda x: not x.isdigit(), row2[col]))

            # Compute similarity score \
            callsign_similarity = fuzz.ratio(str1,str2)
          
            # If similarity is above the threshold for both columns, print potential duplicate
            if callsign_similarity > similarity_threshold and callsign_similarity < 100:
                  print(f"Match found in {folder_path}: {row1[col]} - {row2[col]}")
              

def find_duplicates_in_dataset(df):
 
    # Check for duplicates based on 'callsign' and 'name' columns
    duplicates = df[df.duplicated(subset=['callsign', 'name'], keep=False)]
    
    return duplicates

def compare_datasets(df_g,df_m,g_col='name',m_col='name',similarity_threshold=85):
    # Compare datasets and try to match rows
    for idx_g, row_g in df_g.iterrows():
        for idx_m, row_m in df_m.iterrows():
           # Compare 'callsign' columns using fuzzy matching
            
            # Skip if the one of the names is empty
            if pd.isnull(row_g[g_col]) or pd.isnull(row_m[m_col]):
                continue

            # Skip if the rows are the same
            if row_g[g_col] == row_m[m_col]:
                continue

            #print(row_g['name'], row_m['name'])
            similarity = fuzz.ratio(row_g[g_col], row_m[m_col])
            
            # Consider it a match if similarity is above 85 (tune as needed)
            if similarity > similarity_threshold and similarity < 100:
                print(f"Match found in {folder_path}: {row_g[g_col]} - {row_m[m_col]}")
                # print("General Data Row:", row_g)
                # print("Modified Data Row:", row_m)
                print("Similarity Score:", similarity)
                print('---')

def load_datasets(folder_path):
    # Path to the General and Modified CSV files
    path_g = os.path.join(folder_path, 'ships_G.csv')
    path_m = os.path.join(folder_path, 'ships_M.csv')
    
    # Read CSV files
    try:
        print(f"Reading CSV files in {folder_path}")
        print("reading general_csv:", path_g)
        df_g = pd.read_csv(path_g)
        print("reading modified_csv:", path_m)
        df_m = pd.read_csv(path_m)
        return df_m, df_g

    except FileNotFoundError:
        print(f"CSV files not found in {folder_path}")
        return None, None
    

# Get the path where the script is running
script_path = os.path.dirname(os.path.abspath(__file__))


# Dictionary mapping current column names to new column names
new_column_names = {
    'shipType': 'ship_type',
    'pax':'passengers',
    'stons': 'weight'
}


# Iterate over all folders in the script path
for folder_name in os.listdir(script_path):
    folder_path = os.path.join(script_path, folder_name)
    if os.path.isdir(folder_path):
        # Compare datasets in this folder
        df_m, df_g = load_datasets(folder_path)
        if df_m is not None and df_g is not None:

           # Rename the columns
            df_g.rename(columns=new_column_names, inplace=True)

            #compare_datasets(df_g, df_m)
            find_duplicates_in_dataset(df_g)
            find_duplicates_in_dataset(df_g)
            #find_potential_misspelled_names(df_m)
            #find_potential_misspelled_names(df_g)
            exc = side_by_side(df_g,df_m)
            highlight_nans(exc)
            color_df(generate_populationtable(df_g,'ship_type',['fuel','passengers','weight','lat','long']))