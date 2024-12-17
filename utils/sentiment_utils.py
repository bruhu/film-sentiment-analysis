import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from scipy.stats import spearmanr
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
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

def explode_column(df, column, separator=','):
    """
    Splits the specified column by a separator and explodes the values into separate rows.

    """
    # Split the column by the separator
    df[column] = df[column].str.split(separator)

    # Explode the column into separate rows
    df_exploded = df.explode(column)
    
    return df_exploded

def explode_column_from_string(df, column, separator=','):
    """
    Explodes a specified column in the DataFrame by splitting its string values by a separator
    and creating separate rows for each split value.
    
    """
    # Ensure the column is a list or split it if it's a string
    df[column] = df[column].apply(lambda x: x.split(separator) if isinstance(x, str) else x)
    
    # Explode the column into separate rows
    df_exploded = df.explode(column)
    
    return df_exploded

def plot_sentiment_distribution(df, category_column, sentiment_column, title, xaxis_title, yaxis_title):
    """
    Visualizes the sentiment distribution by a specified categorical column (e.g., language, events, themes).
    
    """
    fig = px.box(df, 
                 x=category_column, 
                 y=sentiment_column, 
                 title=title,
                 labels={category_column: xaxis_title, sentiment_column: yaxis_title})
    
    fig.update_layout(xaxis_tickangle=-45)
    fig.show()
    


# Initialize the sentiment intensity analyzer


def get_sentiment_score(text):
    """Calculates the sentiment score for a given text."""
    
    sia = SentimentIntensityAnalyzer()
    
    if isinstance(text, str):  # Check if the text is a valid string
        return sia.polarity_scores(text)['compound']
    return 0  # Return 0 for non-string values

def add_sentiment_columns(df, columns):
    """
    Adds sentiment score columns to the DataFrame for each specified text column.
    
    Parameters:
    - df: The DataFrame containing the data.
    - columns: A list of column names that contain text to analyze for sentiment.
    
    Returns:
    - df: The DataFrame with added sentiment columns.
    """
    for column in columns:
        sentiment_column_name = f'sentiment_{column}'
        df[sentiment_column_name] = df[column].apply(get_sentiment_score)
    
    return df

def calculate_overall_sentiment(df, sentiment_columns, new_column_name='overall_sentiment'):
    """
    Calculate the overall sentiment for the DataFrame by averaging the sentiment scores
    from the specified columns.

    """
    # Calculate the overall sentiment by averaging the specified sentiment columns
    df[new_column_name] = df[sentiment_columns].mean(axis=1)
    return df


