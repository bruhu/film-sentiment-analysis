import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from scipy.stats import spearmanr
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

def word_rating_correlation(df, text_column, rating_column, top_n=10):
    """
    Computes and visualizes the Spearman correlation between word frequencies and ratings.
    
    """
    # Ensure all entries in the text column are strings
    df[text_column] = df[text_column].apply(
        lambda x: ' '.join(x) if isinstance(x, list) else str(x)
    )

    # Vectorize the text column
    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(df[text_column])
    word_count_df = pd.DataFrame(x.toarray(), columns=vectorizer.get_feature_names_out())

    # Compute correlations between word frequencies and ratings
    correlations = {}
    for word in word_count_df.columns:
        corr, _ = spearmanr(word_count_df[word], df[rating_column])
        correlations[word] = corr

    # Sort correlations by absolute value
    sorted_correlations = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)

    # Display top correlated words
    top_correlated_words = sorted_correlations[:top_n]
    print("Top Words Correlated with Ratings:")
    for word, corr in top_correlated_words:
        print(f"{word}: {corr:.2f}")

    # Plot the top correlated words
    words, corrs = zip(*top_correlated_words)
    fig = px.bar(x=words, y=corrs, title=f'Top {top_n} Words Correlated with Ratings',
                 labels={'x': 'Words', 'y': 'Spearman Correlation'}, color=corrs,
                 color_continuous_scale='Temps_r')
    fig.update_layout(xaxis_tickangle=-45)
    fig.show()
    
    
def preprocess_text(text):
    """
    Preprocesses text by lowercasing, removing punctuation, tokenizing, and removing stopwords.

    """
    # Lowercase the text
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^a-z\s]', '', text)
    # Tokenize
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return tokens


def analyze_most_common_words(df, text_column, top_n=50):
    """
    Analyzes, visualizes, and prints the most common words in a specified text column.

    """
    # Define the processed column name dynamically
    processed_column = f"processed_{text_column}"

    # Apply text preprocessing
    df[processed_column] = df[text_column].apply(preprocess_text)
    
    # Flatten all tokens
    all_tokens = [word for tokens in df[processed_column] for word in tokens]
    
    # Count word frequencies
    word_freq = Counter(all_tokens)
    most_common_words = word_freq.most_common(top_n)
    
    # Display most common words
    print(f"Most common words in {text_column}:")
    print(most_common_words)
    
    # Extract words and counts for plotting
    words, counts = zip(*most_common_words)
    fig = px.bar(x=words, y=counts, title=f'Most Common Words in {text_column}',
                 labels={'x': 'Words', 'y': 'Frequency'}, color=counts,
                 color_continuous_scale='Matter')
    fig.update_layout(xaxis_tickangle=-45)
    fig.show()
    
    return most_common_words


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