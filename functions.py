import pandas as pd
import datetime as dt
import regex as re
from emot.emo_unicode import UNICODE_EMOJI  # For emojis
from emot.emo_unicode import EMOTICONS_EMO
from textblob import TextBlob
import nltk
from emoji import demojize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from Sentiment_analysis import SentimentAnalyzer
import re




nltk.download('vader_lexicon')

def extract_emojis(column_name):
    emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                "]+", flags=re.UNICODE)
    return emoji_pattern.findall(column_name) if isinstance(column_name, str) else []

def emoji_list(df, column_name):
    df['emoji_list'] = df[column_name].apply(extract_emojis)
    df['emojis_num'] = df['emoji_list'].apply(len)
    return df

    # Function to add sentiment analysis
def add_sentiment_analysis(df, column_name):
    df['sentiment'] = df[column_name].apply(get_sentiment)
    return df




    # Placeholder function for sentiment analysis
def get_sentiment(column_name):
    if isinstance(column_name, str):
        sid = SentimentIntensityAnalyzer()
        sentiment_scores = sid.polarity_scores(column_name)
        if sentiment_scores['compound'] >= 0.05:
            return 'Positive'
        elif sentiment_scores['compound'] <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    else:
        return 'Neutral'

def profiler(main_file, user_name, network = 'all'):
    if network != 'all':
        profiler_df = main_file[(main_file['profile_username'] == user_name) & (main_file['Instagram/Facebook'] == network)]
    else:
        profiler_df = main_file[(main_file['profile_username'] == user_name) & (main_file['Instagram/Facebook'])]
    return profiler_df
