import pandas as pd
import numpy as np
from datetime import datetime
import re
import langcodes

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
    """
    Cleans the DataFrame by removing rows with missing values and reports the number of rows removed.

    Parameters:
        df (pd.DataFrame): The input DataFrame to be cleaned.

    Returns:
        tuple: A tuple containing the cleaned DataFrame and the number of rows removed.
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

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The column to check for missing values.

    Returns:
        pd.DataFrame: The updated DataFrame with rows dropped.
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

def get_column_summary(df, column_name):
    """Get a summary of statistics for a specific column."""
    return df[column_name].describe()


# Cleaning

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

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    columns (list): List of column names to convert.

    Returns:
    pd.DataFrame: The DataFrame with specified columns converted to Int64 type.
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
    
    Parameters:
        df (pd.DataFrame): Input DataFrame.
        year_column (str): Name of the column containing year values.
    
    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    current_year = datetime.now().year
    return df[df[year_column] <= current_year]


def clean_title(title):
    """
    Cleans a single title by removing leading/trailing spaces, normalizing spaces,
    removing special characters, and converting the text to lowercase.

    Parameters:
    -----------
    title : str
        The title string to be cleaned.

    Returns:
    --------
    str or None
        The cleaned title if the input is a string, otherwise None.
    """
    if isinstance(title, str):  # Check if the title is a string
        title = title.strip()  # Remove leading/trailing spaces
        title = re.sub(r'\s+', ' ', title)  # Replace multiple spaces with a single space
        # Preserve Latin characters and spaces while removing other special characters
        title = re.sub(
            r'[^\w\sàáâäãåçèéêëìíîïñòóôöõùúûüýÿÀÁÂÄÃÅÇÈÉÊËÌÍÎÏÑÒÓÔÖÕÙÚÛÜÝ]', '', title
        )
        title = title.lower()  # Convert the title to lowercase
        return title
    return None  # Return None for non-string values


def prepare_clean_titles(df, column_name):
    """
    Cleans the titles in a specified column of a DataFrame by removing special characters, 
    normalizing spaces, and converting text to lowercase. The cleaned titles are returned 
    as a pandas Series.
    
    Returns:
    --------
    pandas.Series
        A Series with cleaned titles, where:
        - Leading and trailing spaces are removed.
        - Multiple spaces are replaced with a single space.
        - Special characters (non-alphanumeric except Latin characters) are removed.
        - Text is converted to lowercase.
        - Non-string values are converted to None.
    """ 
    # Apply the clean_title function to the specified column
    return df[column_name].apply(clean_title)

def clean_and_remove_duplicates(df, column_name='title'):
    """
    Clean the title column (strip spaces, normalize multiple spaces, convert to lowercase),
    remove duplicates based on the cleaned titles, 
    and return the cleaned DataFrame along with the count of rows removed.
    """

    df[column_name] = df[column_name].apply(clean_title)
    
    duplicates = df[df[column_name].duplicated(keep=False)]
    
    num_duplicates = len(duplicates)
    print(f'Number of duplicate rows before cleaning: {num_duplicates}')
    
    rows_before = len(df)
    df = df.drop_duplicates(subset=column_name, keep='first')
    
    rows_after = len(df)
    rows_removed = rows_before - rows_after
    print(f'Number of rows removed: {rows_removed}')
    
    return df

def clean_genres(df, column_name):
    """
    Cleans movie genres in a specified column of a DataFrame by standardizing text to lowercase 
    and ensuring consistent spacing after commas.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the column with movie genres to be cleaned.
    column_name : str
        The name of the column in the DataFrame that contains the genres to be cleaned.

    Returns:
    --------
    pandas.Series
        A Series with cleaned genres where:
        - Text is converted to lowercase.
        - Commas are followed by a single space for consistency.
        - Non-string values are replaced with None.
    """
    def clean_genre(genre):
        if isinstance(genre, str):  # Check if the genre is a string
            genre = genre.lower()  # Convert to lowercase
            genre = re.sub(r',\s*', ', ', genre)  # Ensure a single space after commas
            return genre
        return None  # Return None for non-string values

    # Apply the clean_genre function to the specified column
    return df[column_name].apply(clean_genre)

def get_language_name(code):
    try:
        # Get the language name in English
        return langcodes.Language.make(code).language_name()
    except:
        # If the language code is not recognized, return the original code
        return code

def drop_rows_by_runtime(df, column_name='runtime', min_runtime=40):
    """
    Drops rows where the specified column contains a runtime less than the specified minimum runtime.
    Prints how many rows were dropped and returns the updated DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to process.
    column_name : str
        The name of the column containing runtime values.
    min_runtime : int
        The minimum runtime value. Rows with runtime less than this value will be dropped.

    Returns:
    --------
    pandas.DataFrame
        The updated DataFrame with rows dropped.
    """
    # Ensure that 'runtime' column is treated as integers (convert non-numeric to NaN)
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

    # Count rows before filtering
    rows_before = len(df)

    # Drop rows where runtime is less than min_runtime
    df.dropna(subset=[column_name], inplace=True)  # Drop rows where 'runtime' is NaN after conversion
    df.drop(df[df[column_name] < min_runtime].index, inplace=True)

    # Count rows after filtering
    rows_after = len(df)

    # Print how many rows have been dropped
    rows_dropped = rows_before - rows_after
    print(f'Number of rows dropped (runtime < {min_runtime}): {rows_dropped}')

    return df  # Return the updated DataFrame

# After modifying the function, now you can call it as:


