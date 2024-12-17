# **Sentiment Analysis of Movie Reviews by Genre and Trigger Warning**

## **Overview**
This project investigates the sentiment of movie reviews by analyzing the differences between genres and movies with or without trigger warnings. The goal is to explore if there are noticeable patterns in sentiment scores based on genre or trigger warning content. Additionally, we will analyze the relationship between sentiment scores and movie ratings, box office earnings, and other related factors.

The dataset used comes from a combination of **TMDB** (The Movie Database), **IMDB** (Internet Movie Database), and **Letterboxd**, focusing on movies released in **2018**. Additionally, data from **doesthedogdie.com** provides information to determine whether a movie has a trigger warning or not.

## **Objectives**
- **Sentiment Analysis**: Analyze user reviews of movies using Natural Language Processing (NLP) techniques, particularly **VADER** (Valence Aware Dictionary and sEntiment Reasoner), to determine sentiment scores.
- **Comparison of Sentiment**: Compare sentiment scores between different **genres** and between movies that contain **trigger warnings** versus those that do not.
- **Text Mining**: Visualize frequent words and phrases used in reviews with and without trigger warnings using **word clouds**.
- **Data Correlation**: Investigate the correlation between sentiment scores and other movie characteristics such as **ratings** (IMDB, Letterboxd) and **box office earnings** (if available).

## **Data Sources**
1. **TMDB (The Movie Database)**: A comprehensive movie database providing movie metadata including genres, ratings, and reviews.
2. **IMDB**: Additional movie data, including user reviews, ratings, and movie details.
3. **Letterboxd**: A movie review and social networking site providing user ratings and reviews.
4. **doesthedogdie.com**: A website providing trigger warnings for movies, indicating whether the film contains content related to certain sensitive topics (e.g., death, violence, or other distressing themes).

## **Approach**
1. **Data Collection**:
   - Movies data is collected using the open APIs of **TMDB**, **IMDB**, **Letterboxd**, and **doesthedogdie.com**.
   - The data is processed and cleaned to focus on key fields like **genres**, **reviews**, and **trigger warning information**.

2. **Sentiment Analysis**:
   - Using NLP techniques and the **VADER** sentiment analysis tool, user reviews are processed to extract sentiment scores.
   - A comparison is made between reviews from different **genres** and those that contain **trigger warnings**.

3. **Visualization**:
   - **Word clouds** are generated for reviews with trigger warnings versus those without to observe frequent words and phrases.
   - **Bar charts** and other relevant visualizations are created to show the distribution of sentiment across genres and trigger warning categories.

4. **Correlations**:
   - Investigate if there are any correlations between sentiment scores and other factors like **ratings** (from IMDB and Letterboxd) and **box office earnings** (if available).
   - Compare sentiment differences for genres with higher or lower ratings or earnings.

## **Technologies Used**
- **Python** for data processing and analysis
  - Libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`
- **NLP Tools**: 
  - **VADER** (for sentiment analysis)
- **APIs**:
  - **[TMDB API](https://developer.themoviedb.org/reference/configuration-details)**: For movie metadata and reviews.
  - **[Letterboxd API](https://api-docs.letterboxd.com/)**: For movie ratings and reviews.
  - **[doesthedogdie.com API](https://www.doesthedogdie.com/api)**: For trigger warning data.
- **Tools**:
  - **Postman**: Used for testing and handling API requests and responses, as well as working with JSON data.

## **Expected Outcomes**
- Insights into how sentiment varies across movie **genres** and for movies with or without **trigger warnings**.
- Identification of common words or phrases associated with movies that have trigger warnings.
- Correlation between movie sentiment and other metrics like **ratings** and **box office earnings**.
