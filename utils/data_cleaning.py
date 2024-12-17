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

def group_and_join_columns(
    df_main, df_to_group, group_by_col, join_col, new_col_name=None, separator=', ', fillna_value=''
):
    """
    Groups and joins values from a specified column, then merges the result back to the main dataframe.
    """
    if new_col_name is None:
        new_col_name = join_col + 's'
    
    # Group by and join values
    grouped = (
        df_to_group.groupby(group_by_col)[join_col]
        .apply(lambda x: separator.join(x))
        .reset_index()
    )

    # Rename the join_col in df_to_group to avoid conflicts (e.g., 'name' -> 'director')
    grouped.rename(columns={join_col: new_col_name}, inplace=True)

    # Merge with the main dataframe
    df_main = df_main.merge(grouped, on=group_by_col, how='left')

    # Replace NaN values with the specified value
    df_main[new_col_name] = df_main[new_col_name].fillna(fillna_value)

    return df_main


def update_empty_column(
    df_main, df_mapping, main_column, mapping_column, new_column, default_column=None
):
    """
    Updates a column in the main dataframe ('df_main') by mapping values from a secondary dataframe ('df_mapping').
    
    This function fills missing values in the 'new_column' of the main dataframe by mapping values from the
    'mapping_column' of the 'df_mapping' dataframe based on matching values from 'main_column'. If the
    'mapping_column' is missing in the mapping dataframe or if the 'new_column' does not exist in the main
    dataframe, the function handles those cases gracefully. Optionally, it can also use a default column 
    ('default_column') in the mapping dataframe to fill any remaining missing values after the initial mapping.

    """
    if mapping_column in df_mapping.columns:
        mapping_dict = df_mapping.set_index(main_column)[mapping_column]

        # Ensure that the 'new_column' exists in the main dataframe
        if new_column not in df_main.columns:
            df_main[new_column] = pd.NA 

        df_main[new_column] = df_main[new_column].combine_first(
            df_main[main_column].map(mapping_dict)
        )

        if default_column and default_column in df_mapping.columns:
            df_main[new_column] = df_main[new_column].fillna(
                df_main[main_column].map(df_mapping.set_index(main_column)[default_column])
            )
    else:
        print(f"Warning: '{mapping_column}' is missing in the mapping dataframe. Skipping update.")
    
    return df_main


def filter_future_years(df, year_column):
    """
    Removes rows from the DataFrame where the year in the specified column
    is greater than the current year.
    """
    current_year = datetime.now().year
    return df[df[year_column] <= current_year]
