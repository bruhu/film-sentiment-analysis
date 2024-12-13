import re
import langcodes

def clean_title(title):
    """
    Cleans a single title by removing leading/trailing spaces, normalizing spaces,
    removing special characters, and converting the text to lowercase.
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

def clean_genres(df, column_name):
    """
    Cleans movie genres in a specified column of a DataFrame by standardizing text to lowercase 
    and ensuring consistent spacing after commas.
    """
    def clean_genre(genre):
        if isinstance(genre, str):  # Check if the genre is a string
            genre = genre.lower()  # Convert to lowercase
            genre = re.sub(r',\s*', ', ', genre)  # Ensure a single space after commas
            return genre
        return None  # Return None for non-string values

    return df[column_name].apply(clean_genre)

def get_language_name(code):
    try:
        return langcodes.Language.make(code).language_name()
    except:
        return code

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

def drop_rows_by_runtime(df, column_name='runtime', min_runtime=40):
    """
    Drops rows where the specified column contains a runtime less than the specified minimum runtime.
    Prints how many rows were dropped and returns the updated DataFrame.
    """
    # Ensure that 'runtime' column is treated as integers (convert non-numeric to NaN)
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

    rows_before = len(df)

    # Drop rows where runtime is less than min_runtime
    df.dropna(subset=[column_name], inplace=True)
    df.drop(df[df[column_name] < min_runtime].index, inplace=True)

    rows_after = len(df)

    rows_dropped = rows_before - rows_after
    print(f'Number of rows dropped (runtime < {min_runtime}): {rows_dropped}')

    return df