import pandas as pd
import re
from datetime import datetime

def remove_duplicates(df):
    """Remove duplicate rows from a DataFrame."""
    before_count = len(df)
    df = df.drop_duplicates()
    after_count = len(df)
    removed_count = before_count - after_count
    print(f'Removed {removed_count} duplicate rows.')
    return df

def drop_empty_rows(df):
    """
    Cleans the DataFrame by removing rows with missing values and reports the number of rows removed.
    """
    original_row_count = df.shape[0]
    df = df.dropna()
    cleaned_row_count = df.shape[0]
    
    rows_removed = original_row_count - cleaned_row_count
    print(f'Rows removed: {rows_removed}')
    
    return df, rows_removed

def drop_empty_rows_from_column(df, column_name):
    """
    Drops rows where the specified column has missing values and returns the updated DataFrame.
    Also prints the number of rows deleted.
    """
    initial_rows = len(df)
    df = df.dropna(subset=[column_name])
    
    deleted_rows = initial_rows - len(df)
    print(f'Number of rows deleted: {deleted_rows}')
    
    return df

def rename_columns(df, rename_dict):
    """Rename columns based on a dictionary."""
    return df.rename(columns=rename_dict)

def standardize_column_names(df):
    """Standardize column names (lowercase, replace spaces with underscores, and convert camelCase to snake_case)."""
    
    # convert camelCase to snake_case
    def camel_to_snake(name):
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower() # underscore before uppercase letters
    
    df.columns = [camel_to_snake(col.strip().replace(' ', '_')) for col in df.columns] # apply all transformations
    
    return df

def convert_strings_to_lowercase(df, column_name):
    """
    Converts all string entries in a specified column of a DataFrame to lowercase,
    ensures there is a space after any comma in the strings, removes quote marks,
    and adjusts commas according to the specified conditions.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame.
        column_name (str): The name of the column to process.

    Returns:
        pd.DataFrame: DataFrame with the specified column processed.
    """
    if column_name in df.columns and df[column_name].dtype in ['object', 'string']:
        df[column_name] = df[column_name].map(
            lambda x: (
                x.lower()
                .replace('"', '')  # Remove all double quotes
                .lstrip(',')  # Remove leading commas (and any spaces after them)
                .replace(', ', ',')  # Remove spaces after commas
                .replace(',', ', ')  # Add space after commas where necessary
            ) if isinstance(x, str) else x
        )
    else:
        raise ValueError(f"Column '{column_name}' does not exist or is not of type object/string.")
    return df

def convert_columns_to_int(df, columns):
    """
    Converts specified columns in the DataFrame to Int64 type, handling errors gracefully.
    """
    # Check if the columns exist in the DataFrame
    columns_to_convert = [col for col in columns if col in df.columns]

    # Convert the specified columns to 'Int64' type, handling errors gracefully
    df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric, errors='coerce').astype('Int64')

    return df


def filter_future_years(df, year_column):
    """
    Removes rows from the DataFrame where the year in the specified column
    is greater than the current year.
    """
    current_year = datetime.now().year
    return df[df[year_column] <= current_year]
