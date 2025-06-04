import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def display_stars(num_stars):
    return '*' * num_stars

def analyze_sentiment(review):
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(review)['compound']

    if sentiment_score >= 0.7:
        sentiment_label = "Good :)"
        stars = display_stars(5)
    elif sentiment_score >= 0.3:
        sentiment_label = "Very Good :)"
        stars = display_stars(4)
    elif -0.1 <= sentiment_score <= 0.1:
        sentiment_label = "Neutral ._."
        stars = display_stars(3)
    elif sentiment_score <= -0.3:
        sentiment_label = "Bad :("
        stars = display_stars(2)
    elif sentiment_score <= -0.7:
        sentiment_label = "Very Bad :("
        stars = display_stars(1)
    else:
        sentiment_label = "Neutral"
        stars = display_stars(3)

    return sentiment_label, stars

# Take user input for review
review = input("Enter your review: ")

# Analyze sentiment based on user input
sentiment_label, stars = analyze_sentiment(review)

# Print the review, sentiment label, and stars
print(f"Review: {review}")
print(f"Sentiment: {sentiment_label}")
print(f"Stars: {stars}")