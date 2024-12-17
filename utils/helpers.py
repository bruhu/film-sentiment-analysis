import pandas as pd
import re
import langcodes


# ------------------------------
# Title Cleaning Functions
# ------------------------------

def clean_title(title):
    """
    Cleans a single title by removing leading/trailing spaces, normalizing spaces,
    removing special characters, and converting the text to lowercase.
    """
    if isinstance(title, str): 
        title = title.strip()  
        title = re.sub(r'\s+', ' ', title) 
        title = re.sub(
            r'[^\w\sàáâäãåçèéêëìíîïñòóôöõùúûüýÿÀÁÂÄÃÅÇÈÉÊËÌÍÎÏÑÒÓÔÖÕÙÚÛÜÝ]', '', title # remove special chars, keep Latin chars and spaces
        )
        title = title.lower()  
        return title
    return None  


def prepare_clean_titles(df, column_name):
    """
    Cleans the titles in a specified column of a DataFrame by removing special characters, 
    normalizing spaces, and converting text to lowercase. The cleaned titles are returned 
    as a pandas Series.
    """ 
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


# ------------------------------
# Genre Cleaning Functions
# ------------------------------

def clean_genres(df, column_name):
    """
    Cleans movie genres in a specified column of a DataFrame by standardizing text to lowercase 
    and ensuring consistent spacing after commas.
    """
    def clean_genre(genre):
        if isinstance(genre, str):  
            genre = genre.lower()  
            genre = re.sub(r',\s*', ', ', genre)  
            return genre
        return None 

    return df[column_name].apply(clean_genre)


# ------------------------------
# Language Functions
# ------------------------------

def get_language_name(code):
    """
    Returns the language name based on the provided language code using the langcodes library.
    If the code is invalid, it returns the code itself.
    """
    try:
        return langcodes.Language.make(code).language_name()
    except:
        return code


# ------------------------------
# Runtime Filtering Functions
# ------------------------------

def drop_rows_by_runtime(df, column_name='runtime', min_runtime=40, max_runtime=300):
    """
    Drops rows where the specified column contains a runtime less than the specified minimum runtime 
    or greater than the maximum runtime.
    Prints how many rows were dropped and returns the updated DataFrame.
    
    """
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

    rows_before = len(df)

    df.dropna(subset=[column_name], inplace=True)

    df.drop(df[(df[column_name] < min_runtime) | (df[column_name] > max_runtime)].index, inplace=True)

    rows_after = len(df)

    rows_dropped = rows_before - rows_after
    print(f'Number of rows dropped (runtime < {min_runtime} or runtime > {max_runtime}): {rows_dropped}')

    return df
