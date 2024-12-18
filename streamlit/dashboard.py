import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import numpy as np

# Custom CSS to load Manrope font and apply it globally
manrope_font_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&display=swap');

body, p, div, h1, h2, h3, h4, h5, h6 {
    font-family: 'Manrope', sans-serif;
    font-weight: 400;
    color: #333333; /* Optional: Custom text color */
    background-color: white;
}

h1 {
    font-weight: 800; /* Bold headings */
    color: #FF6347;   /* Optional: Custom color for headings */
}

h2, h3 {
    font-weight: 600; /* Semi-bold subheadings */
}
</style>
"""

# Inject custom CSS
st.markdown(manrope_font_css, unsafe_allow_html=True)

# Directly load the CSV file (replace with the path to your CSV file)
# csv_file_path = 

# Read the CSV into a DataFrame
df = pd.read_csv('./data/clean/letterboxd_clean_films.csv')

# Streamlit content
st.title("🚀 Streamlit Dashboard with Manrope Font")
st.subheader("This is a subheader with Manrope font.")
st.write("Manrope is a clean, modern, and versatile font loaded from Google Fonts.")

st.write("You can customize font weights, sizes, and colors using the CSS above.")

# Example Table
# st.subheader("Example Table:")
# st.table({"Column 1": [1, 2, 3], "Column 2": ["A", "B", "C"]})

# Example Chart
# st.subheader("Example Chart:")
# data = pd.DataFrame({
#     "Category": ["A", "B", "C", "D"],
#     "Values": [10, 20, 30, 40]
# })
# fig = px.bar(data, x="Category", y="Values", title="Bar Chart Example")
# st.plotly_chart(fig)

# Show a preview of the data
num_rows, num_cols = df.shape
print(f'Number of Rows: {num_rows}')
print(f'Number of Columns: {num_cols}')

# languages
languages = df['language'].dropna().str.split(',').explode().str.strip()
unique_languages = languages.nunique()
print(f'Number of Languages: {unique_languages}')

# countries
countries = df['countries'].dropna().str.split(',').explode().str.strip()
unique_countries = countries.nunique()
print(f'Number of Countries: {unique_countries}')

# genres
genres = df['genres'].dropna().str.split(',').explode().str.strip()
unique_genres = genres.nunique()
print(f'Number of Genres: {unique_genres}')

# earliest and latest year
earliest_year = df['release_year'].min()
latest_year = df['release_year'].max()
print(f'Earliest Year: {earliest_year}')
print(f'Latest Year: {latest_year}')

# longest and shortest runtime
shortest_runtime = df['runtime'].min()
longest_runtime = df['runtime'].max()
print(f'Shortest Runtime: {shortest_runtime} minutes')
print(f'Longest Runtime: {longest_runtime} minutes')

    
st.write("Data Preview:")
st.dataframe(df.head())

# 1. Distribution of numerical columns (Histograms)
st.subheader("Distribution of Numerical Features")
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
if numeric_cols:
    for col in numeric_cols:
        fig = px.histogram(df, x=col, title=f"Distribution of {col}")
        st.plotly_chart(fig)
        