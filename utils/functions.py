import pandas as pd
import numpy as np
from datetime import datetime
import re


# Data Reading

def show_data_types(df):
    """Show data types of all columns in the DataFrame."""
    print('Data Types of Columns:')
    print(df.dtypes)

def show_missing_values(df):
    """Show the number of missing values per column."""
    print('\nMissing Values in Columns:')
    print(df.isnull().sum())

def show_basic_info(df):
    """Show basic information about the DataFrame including shape, dtypes, and missing values."""
    print(f'\nDataFrame Shape: {df.shape}')
    print(f'Number of Rows: {df.shape[0]}')
    print(f'Number of Columns: {df.shape[1]}')
    print('\nData Types of Columns:')
    print(df.dtypes)
    print('\nMissing Values per Column:')
    print(df.isnull().sum())
    print('\nFirst 5 Rows of Data:')
    print(df.head())

def show_column_summary(df):
    """Show summary statistics for all columns."""
    print('\nSummary Statistics for All Columns:')
    print(df.describe(include='all'))

def show_column_values(df, column_name):
    """Show unique values for a specific column."""
    if column_name in df.columns:
        print(f'\nUnique values in column {column_name}:')
        print(df[column_name].unique())
    else:
        print(f'Column {column_name} does not exist in the DataFrame.')

def show_column_value_counts(df, column_name):
    """Show value counts for a specific column."""
    if column_name in df.columns:
        print(f'\nValue counts for column {column_name}:')
        print(df[column_name].value_counts())
    else:
        print(f'Column {column_name} does not exist in the DataFrame.')

def check_for_duplicates(df):
    """Check for duplicate rows in the DataFrame."""
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f'\nThere are {duplicates} duplicate rows in the DataFrame.')
    else:
        print('\nNo duplicate rows found in the DataFrame.')

def show_column_info(df, column_name):
    """Show detailed information about a specific column."""
    if column_name in df.columns:
        print(f'\nColumn Info for {column_name}:')
        print(f'Data Type: {df[column_name].dtype}')
        print(f'Number of Unique Values: {df[column_name].nunique()}')
        print(f'Number of Missing Values: {df[column_name].isnull().sum()}')
        print(f'Unique Values:')
        print(df[column_name].unique())
    else:
        print(f'Column {column_name} does not exist in the DataFrame.')

def show_null_percentage(df):
    """Show percentage of missing values in each column."""
    null_percentage = df.isnull().mean() * 100
    print('\nPercentage of Missing Values in Each Column:')
    print(null_percentage)


# Basic Data Cleaning

def remove_duplicates(df):
    """Remove duplicate rows from a DataFrame."""
    before_count = len(df)
    df = df.drop_duplicates()
    after_count = len(df)
    removed_count = before_count - after_count
    print(f'Removed {removed_count} duplicate rows.')
    return df

def drop_empty_rows(df):
    # Get the original row count before dropping empty rows
    original_row_count = df.shape[0]
    
    # Drop rows with missing values (NaN)
    df = df.dropna()
    
    # Get the row count after dropping empty rows
    cleaned_row_count = df.shape[0]
    
    # Calculate the number of rows removed
    rows_removed = original_row_count - cleaned_row_count
    
    # Return the cleaned DataFrame and the number of rows removed
    print(f'Rows removed: {rows_removed}')
    return df, rows_removed

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

def get_column_summary(df, column_name):
    """Get a summary of statistics for a specific column."""
    return df[column_name].describe()


# Cleaning

def convert_strings_to_lowercase(df):
    """
    Converts all string entries in a DataFrame to lowercase per column
    and ensures there is a space after any comma in the strings, removes 
    quote marks, and adjusts commas according to the specified conditions.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with string entries converted to lowercase,
                      adjusted for spaces after commas, and processed quote marks 
                      and commas.
    """
    for col in df.select_dtypes(include=['object', 'string']):
        df[col] = df[col].map(
            lambda x: (
                x.lower()
                .replace('"', '')  # Remove all double quotes
                .lstrip(',')  # Remove leading commas (and any spaces after them)
                .replace(', ', ',')  # Remove spaces after commas
                .replace(',', ', ')  # Add space after commas where necessary
            ) if isinstance(x, str) else x
        )
    return df


def filter_future_years(df, year_column):
    """
    Removes rows from the DataFrame where the year in the specified column
    is greater than the current year.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame.
        year_column (str): Name of the column containing year values.
    
    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    current_year = datetime.now().year
    return df[df[year_column] <= current_year]

def generate_clean_titles(df, title_col='title', clean_col='clean_title'):
    """
    Cleans the movie titles by removing special characters and unnecessary data.
    
    Parameters:
    df (pd.DataFrame): Input DataFrame.
    title_col (str): Name of the column containing movie titles.
    clean_col (str): Name of the new column for cleaned titles.
    
    Returns:
    pd.DataFrame: DataFrame with an added column for cleaned titles.
    """
    def clean_title(title):
        # Remove special characters and anything in parentheses or brackets
        title = re.sub(r'[\[\]\(\)\{\}]', '', title)  # Remove brackets and parentheses
        title = re.sub(r'[^a-zA-Z0-9\s]', '', title)  # Remove special characters
        title = re.sub(r'\s+', ' ', title).strip()    # Remove extra spaces
        return title

    df[clean_col] = df[title_col].apply(clean_title)
    return df

def clean_titles(title):
    """
    Clean the movie title by:
    - Stripping leading/trailing spaces
    - Replacing multiple spaces with a single space
    - Converting to lowercase
    """
    if isinstance(title, str):  # Check if the title is a string
        title = title.strip()  # Remove leading/trailing spaces
        title = re.sub(r'\s+', ' ', title)  # Replace multiple spaces with a single space
    return title

def clean_and_remove_duplicates(df, column_name='title'):
    """
    Clean the title column (strip spaces, normalize multiple spaces, convert to lowercase),
    remove duplicates based on the cleaned titles, 
    and return the cleaned DataFrame along with the count of rows removed.
    """

    df[column_name] = df[column_name].apply(clean_titles)
    
    duplicates = df[df[column_name].duplicated(keep=False)]
    
    num_duplicates = len(duplicates)
    print(f'Number of duplicate rows before cleaning: {num_duplicates}')
    
    rows_before = len(df)
    df = df.drop_duplicates(subset=column_name, keep='first')
    
    rows_after = len(df)
    rows_removed = rows_before - rows_after
    print(f'Number of rows removed: {rows_removed}')
    
    return df