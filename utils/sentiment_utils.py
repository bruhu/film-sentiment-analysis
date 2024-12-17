import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from scipy.stats import spearmanr
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter

# -------------------------
# Text Preprocessing Functions
# -------------------------

def preprocess_text(text):
    """
    Preprocesses text by lowercasing, removing punctuation, tokenizing, and removing stopwords.

    """
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = word_tokenize(text) # tokenize
    stop_words = set(stopwords.words('english')) # remove stopwords
    tokens = [word for word in tokens if word not in stop_words]
    return tokens


def explode_column(df, column, separator=','):
    """
    Splits the specified column by a separator and explodes the values into separate rows.

    """
    df[column] = df[column].str.split(separator)

    df_exploded = df.explode(column) # explode column into rows
    
    return df_exploded


def explode_column_from_string(df, column, separator=','):
    """
    Explodes a specified column in the DataFrame by splitting its string values by a separator
    and creating separate rows for each split value.
    
    """
    df[column] = df[column].apply(lambda x: x.split(separator) if isinstance(x, str) else x)  #  split col if it's a string and not a list
    
    df_exploded = df.explode(column) # explode col into rows
    
    return df_exploded


# ------------------------
# Sentiment Analysis Functions
# ------------------------

def get_sentiment_score(text):
    """Calculates the sentiment score for a given text."""
    
    sia = SentimentIntensityAnalyzer()
    
    if isinstance(text, str):
        return sia.polarity_scores(text)['compound']
    return 0  # 0 for non-string values


def add_sentiment_columns(df, columns):
    """
    Adds sentiment score columns to the DataFrame for each specified text column.
    
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
    df[new_column_name] = df[sentiment_columns].mean(axis=1) # overall sentiment averaging the specified sentiment columns
    return df


# ---------------------------
# Correlation and Word Analysis
# ---------------------------

def word_rating_correlation(df, text_column, rating_column, top_n=10):
    """
    Computes and visualizes the Spearman correlation between word frequencies and ratings.
    
    """
    df[text_column] = df[text_column].apply(
        lambda x: ' '.join(x) if isinstance(x, list) else str(x) # check dtype
    )

    vectorizer = CountVectorizer() # vectorize text column
    x = vectorizer.fit_transform(df[text_column])
    word_count_df = pd.DataFrame(x.toarray(), columns=vectorizer.get_feature_names_out())

    correlations = {}
    for word in word_count_df.columns:
        corr, _ = spearmanr(word_count_df[word], df[rating_column])
        correlations[word] = corr

    sorted_correlations = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True) # correlation by absolute value

    top_correlated_words = sorted_correlations[:top_n]
    print("Top Words Correlated with Ratings:")
    for word, corr in top_correlated_words:
        print(f"{word}: {corr:.2f}")

    words, corrs = zip(*top_correlated_words)
    fig = px.bar(x=words, y=corrs, title=f'Top {top_n} Words Correlated with Ratings',
                 labels={'x': 'Words', 'y': 'Spearman Correlation'}, color=corrs,
                 color_continuous_scale='Temps_r')
    fig.update_layout(xaxis_tickangle=-45)
    fig.show()  
    

def analyze_most_common_words(df, text_column, top_n=50):
    """
    Analyzes, visualizes, and prints the most common words in a specified text column.

    """
    processed_column = f"processed_{text_column}"

    df[processed_column] = df[text_column].apply(preprocess_text) # text preprocessing
    
    all_tokens = [word for tokens in df[processed_column] for word in tokens] # flatten tokens
    
    word_freq = Counter(all_tokens)
    most_common_words = word_freq.most_common(top_n)
    
    print(f'Most common words in {text_column}:')
    print(most_common_words)
    
    words, counts = zip(*most_common_words)
    fig = px.bar(x=words, y=counts, title=f'Most Common Words in {text_column}',
                 labels={'x': 'Words', 'y': 'Frequency'}, color=counts,
                 color_continuous_scale='Matter')
    fig.update_layout(xaxis_tickangle=-45)
    fig.show()
    
    return most_common_words


# ------------------------------
# Visualization Functions
# ------------------------------

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