import pandas as pd

# ------------------------------
# General DataFrame Info Functions
# ------------------------------

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


def show_null_percentage(df):
    """Show percentage of missing values in each column."""
    null_percentage = df.isnull().mean() * 100
    print('\nPercentage of Missing Values in Each Column:')
    print(null_percentage)


# ------------------------------
# Column-Specific Functions
# ------------------------------

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


# ------------------------------
# Data Quality Functions
# ------------------------------

def check_for_duplicates(df):
    """Check for duplicate rows in the DataFrame."""
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f'\nThere are {duplicates} duplicate rows in the DataFrame.')
    else:
        print('\nNo duplicate rows found in the DataFrame.')


