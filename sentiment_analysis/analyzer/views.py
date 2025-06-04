from django.shortcuts import render
from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_sentiment(review):
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(review)['compound']

    if sentiment_score >= 0.7:
        return "Positive", 5
    elif sentiment_score >= 0.3:
        return "Slightly Positive", 4
    elif -0.1 <= sentiment_score <= 0.1:
        return "Neutral", 3
    elif sentiment_score <= -0.3:
        return "Negative", 2
    elif sentiment_score <= -0.7:
        return "Very Negative", 1
    else:
        return "Neutral", 3

def index(request):
    return render(request, 'index.html')

def analyze(request):
    if request.method == 'POST':
        review = request.POST.get('review')
        sentiment, stars = analyze_sentiment(review)

        # Create a list of stars
        stars_list = range(stars)

        return render(request, 'result.html', {'review': review, 'sentiment': sentiment, 'stars_list': stars_list})
    else:
        return render(request, 'index.html')
