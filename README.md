# **Sentiment Analysis of Movie Reviews by Genre and Trigger Warning**

## **Overview**
This project investigates the sentiment of movie reviews by analyzing the differences between genres and movies with or without trigger warnings. The goal is to explore if there are noticeable patterns in sentiment scores based on genre or trigger warning content. Additionally, we will analyze the relationship between sentiment scores and movie ratings, box office earnings, and other related factors.

The dataset used comes from a combination of **TMDB** (The Movie Database) and **IMDB** (Internet Movie Database), focusing on movies released in **2018**. Additionally, scraping from **doesthedogdie.com** will provide additional data to determine whether a movie has a trigger warning or not.

## **Objectives**
- **Sentiment Analysis**: Analyze user reviews of movies using Natural Language Processing (NLP) techniques such as VADER (Valence Aware Dictionary and sEntiment Reasoner) or TextBlob to determine the sentiment score.
- **Comparison of Sentiment**: Compare sentiment scores between different **genres** and between movies that contain **trigger warnings** versus those that do not.
- **Text Mining**: Visualize frequent words and phrases used in reviews with and without trigger warnings using **word clouds**.
- **Data Correlation**: Investigate the correlation between sentiment scores and other movie characteristics such as **ratings** (IMDB) and **box office earnings** (if available).

## **Data Sources**
1. **TMDB (The Movie Database)**: A comprehensive movie database providing movie metadata including genres, ratings, and reviews.
2. **IMDB**: Additional movie data, including user reviews, ratings, and movie details.
3. **doesthedogdie.com**: A website providing trigger warnings for movies, indicating whether the film contains content related to certain sensitive topics (e.g., death, violence, or other distressing themes).

## **Approach**
1. **Data Collection**:
   - Movies from **2018** will be scraped from **TMDB** and **IMDB**.
   - Additional data regarding trigger warnings will be scraped from **doesthedogdie.com**.
   - The data will be processed and cleaned to focus on key fields like **genres**, **reviews**, and **trigger warning information**.

2. **Sentiment Analysis**:
   - Using NLP libraries like **VADER** or **TextBlob**, user reviews will be processed to extract sentiment scores.
   - A comparison will be made between reviews from different **genres** and those that contain **trigger warnings**.

3. **Visualization**:
   - **Word clouds** will be generated for reviews with trigger warnings versus those without to observe frequent words and phrases.
   - **Bar charts** and other relevant visualizations will be created to show the distribution of sentiment across genres and trigger warning categories.

4. **Correlations**:
   - Investigate if there are any correlations between sentiment scores and other factors like **ratings** (from IMDB) and **box office earnings** (if available).
   - Compare sentiment differences for genres with higher or lower ratings or earnings.

## **Technologies Used**
- **Python** for data processing and analysis
  - Libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `wordcloud`
- **NLP Tools**: 
  - **VADER** (for sentiment analysis)
  - **TextBlob**
- **Web Scraping**:
  - **BeautifulSoup** and **Requests** for scraping data from **TMDB**, **IMDB**, and **doesthedogdie.com**.
- **Data Visualization**:
  - **Matplotlib** and **Seaborn** for plotting graphs and charts.
  - **WordCloud** for visualizing frequent words in reviews.
  
## **File Structure**


## **Installation**
To get started, clone this repository and install the required dependencies:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/sentiment-analysis-movie-reviews.git
    cd sentiment-analysis-movie-reviews
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. You may need to set up a TMDB API key to access the data. Follow the instructions on the [TMDB website](https://www.themoviedb.org/documentation/api) to obtain an API key.

## **Usage**
1. **Scraping Data**:
    - Run the `scraper.py` script to gather movie data from **TMDB**, **IMDB**, and **doesthedogdie.com**.
    ```bash
    python src/scraper.py
    ```

2. **Sentiment Analysis**:
    - After collecting the data, run the `sentiment_analysis.py` script to analyze the sentiment of the reviews.
    ```bash
    python src/sentiment_analysis.py
    ```

3. **Data Visualization**:
    - Generate visualizations by running the Jupyter notebooks located in the `notebooks/` directory.
    ```bash
    jupyter notebook
    ```

## **Expected Outcomes**
- Insights into how sentiment varies across movie **genres** and for movies with or without **trigger warnings**.
- Identification of common words or phrases associated with movies that have trigger warnings.
- Correlation between movie sentiment and other metrics like **ratings** and **box office earnings**.

## **Contributing**
Contributions to this project are welcome! Feel free to open an issue or submit a pull request if you'd like to contribute.

## **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
