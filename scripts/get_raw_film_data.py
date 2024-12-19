# # TMDB + IMDB dataset 
# https://www.kaggle.com/datasets/alanvourch/tmdb-movies-daily-updates


import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns


import sys
sys.path.append('./utils')
import data_cleaning
import data_inspection
import helpers


tmdb_df = pd.read_csv('./data/local/raw/TMDB_all_movies.csv')

data_inspection.show_basic_info(tmdb_df)

# drop columns
tmdb_df.drop(columns=['cast', 'director_of_photography', 'music_composer', 'poster_path', 'writers', 'spoken_languages', 
                      'tagline', 'overview', 'production_companies', 'production_countries', 'producers'], inplace=True)


# check for duplicates
data_inspection.check_for_duplicates(tmdb_df)


# remove rows where 'status' is not 'Released'
print(f'Unique values in status column:\n{tmdb_df['status'].unique()}\n')

initial_rows = len(tmdb_df)
tmdb_df = tmdb_df[tmdb_df['status'] == 'Released'] # keep rows where 'status' is 'Released'
final_rows = len(tmdb_df)
removed_rows = initial_rows - final_rows
print(f'\nNumber of rows removed: {removed_rows}')


# remove 'status' column after sorting
tmdb_df.drop(['status'], axis=1, inplace=True)


# create copy
df = tmdb_df.copy()


# convert 'release_date' to datetime, extract year and convert it to int
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['release_year'] = df['release_date'].dt.year.astype('Int64')
print(df[['release_date', 'release_year']].head())


# drop 'release_date' column
df.drop(columns='release_date', inplace=True)


release_year_counts = df['release_year'].value_counts().sort_index()
print(f'Movie releases per year:\n{release_year_counts}')


# filter out rows for a specific timeframe (eg between 1906 and 2018)
initial_count = len(df)
df = df[(df['release_year'] >= 1906) & (df['release_year'] <= 2018)]
final_count = len(df)
rows_dropped = initial_count - final_count
print(f'Rows dropped after filtering year: {rows_dropped}')
print(df)


release_year_counts = df['release_year'].value_counts().sort_index()
print(f'Movie releases per year:\n{release_year_counts}')


data_inspection.show_missing_values(df)


# drop missing titles
df = data_cleaning.drop_empty_rows_from_column(df, 'title')


# data conversion to int
columns_to_convert = ['imdb_votes', 'revenue', 'budget', 'runtime', 'vote_count']
data_cleaning.convert_columns_to_int(df, columns_to_convert)


# get language names
df['language'] = df['original_language'].apply(helpers.get_language_name)


# handle unknown language(s)
print(f'Unique values in language column:\n{df['language'].unique()}')
print(f'Value counts in language column:\n{df['language'].value_counts()}')


# replace [cn] with a proper label
unknown_lang = df[df['original_language'] == 'cn']
df['language'] = df['language'].replace('Unknown language [cn]', 'Cantonese')


# replace [xx] with a proper label
unknown_lang = df[df['original_language'] == 'xx']
df['language'] = df['language'].replace('Unknown language [xx]', 'Unknown')


print(f'Unique values in language column after re labeling: {df['language'].unique()}')


# drop column after extracting languages
df.drop(columns='original_language', inplace=True)


# parse 'genres' column, make sure they're al lowcase, no extra empty spaces, separated by commas
df['genres'] = helpers.clean_genres(df, 'genres')
print('Unique genres:')
print(df['genres'].unique())


def drop_rows_with_specific_genres(df, column_name='genres', genres_to_exclude=None):
    if genres_to_exclude is None:
        genres_to_exclude = {'documentary', 'music'}

    def contains_excluded_genre(genres):
        if isinstance(genres, list):  # If genres is a list
            return any(genre.strip().lower() in genres_to_exclude for genre in genres)
        elif isinstance(genres, str):  # If genres is a comma-separated string
            return any(genre.strip().lower() in genres_to_exclude for genre in genres.split(','))
        return False  # For NaN or other invalid cases

    rows_before = len(df)  # Number of rows before filtering
    filtered_df = df[~df[column_name].apply(contains_excluded_genre)]
    rows_after = len(filtered_df)  # Number of rows after filtering

    rows_dropped = rows_before - rows_after
    print(f'Number of rows dropped: {rows_dropped}')

    return filtered_df

df = drop_rows_with_specific_genres(df, column_name='genres')


df = helpers.drop_rows_by_runtime(df, column_name='runtime', min_runtime=40)


def remove_title_keywords(df, column_name, words_list):
    if df is None:
        raise ValueError("Input DataFrame is None")
    
    pattern = '|'.join([rf'\b{re.escape(word)}\b' for word in words_list])
    
    initial_count = len(df)  # This will fail if df is None

    df_filtered = df[~df[column_name].str.contains(pattern, case=False, na=False)]

    filtered_count = len(df_filtered)
    print(f'Rows removed: {initial_count - filtered_count}')
    
    return df_filtered

words_to_remove = ['vixen', 'rape', 'slut', 'playboy', 'live at', 'baby einstein', 'championship', 'standup', 'wwe', 'wec', 'fia', 'playoff', 'ufc', 'mma', 'wcw', 'porn', 'snuff', 'nfl', 'nhl', 'raw sex', 'milf', 'molester', 'bondage', 'nba', 'tits', 'f1']
df = remove_title_keywords(df, 'title', words_to_remove)


data_inspection.show_missing_values(df)


rename_columns = {
    'id': 'tmdb_id',
    'vote_average': 'tmdb_rating',
    'vote_count': 'tmdb_votes'
}

df.rename(columns=rename_columns, inplace=True)


# round decimals
df['popularity'] = df['popularity'].round(1)
df['tmdb_rating'] = df['tmdb_rating'].round(1)


# generate clean title column
df['clean_title'] = helpers.prepare_clean_titles(df, 'title')


# restructure columns
new_column_order = [
    'title', 'clean_title', 'original_title', 'genres', 'director', 'release_year',
    'runtime', 'budget', 'revenue', 'popularity', 'tmdb_rating', 'tmdb_votes', 
    'imdb_rating', 'imdb_votes', 'language', 'tmdb_id', 'imdb_id'
]

# Ensure all columns are included, add any missing ones from the original DataFrame
final_column_order = [col for col in new_column_order if col in df.columns]
missing_columns = [col for col in df.columns if col not in final_column_order]
final_column_order.extend(missing_columns)

df = df[final_column_order]

## create .csv file
df = df.sort_values(by='tmdb_id').reset_index(drop=True)
# df.to_csv('../data/local/clean/films_before19_backup.csv', index=False)