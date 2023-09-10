import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt


class SentimentAnalyzer:
    def __init__(self, consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str) -> None:
        self.api = self.authenticate(
            consumer_key, consumer_secret, access_token, access_token_secret)

    def authenticate(self, consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str) -> tweepy.API:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)

    def collect_tweets(self, hashtag: str, num_tweets: int) -> list:
        tweets = []
        for tweet in tweepy.Cursor(self.api.search, q=hashtag, lang="en").items(num_tweets):
            tweets.append(tweet.text)
        return tweets

    def perform_sentiment_analysis(self, tweets: list) -> list:
        polarity_scores = []
        for tweet in tweets:
            analysis = TextBlob(tweet)
            polarity_scores.append(analysis.sentiment.polarity)
        return polarity_scores

    def visualize_sentiment_analysis(self, polarity_scores: list) -> None:
        plt.plot(polarity_scores)
        plt.xlabel('Tweet')
        plt.ylabel('Polarity Score')
        plt.title('Sentiment Analysis')
        plt.show()

    def run(self) -> None:
        hashtag = input("Enter a topic or hashtag to analyze: ")
        num_tweets = int(input("Enter the number of tweets to collect: "))

        tweets = self.collect_tweets(hashtag, num_tweets)
        if not tweets:
            print("No tweets found for the given hashtag. Please try again.")
            return

        polarity_scores = self.perform_sentiment_analysis(tweets)
        self.visualize_sentiment_analysis(polarity_scores)


if __name__ == "__main__":
    consumer_key = input("Enter your consumer key: ")
    consumer_secret = input("Enter your consumer secret: ")
    access_token = input("Enter your access token: ")
    access_token_secret = input("Enter your access token secret: ")

    sentiment_analyzer = SentimentAnalyzer(
        consumer_key, consumer_secret, access_token, access_token_secret)
    sentiment_analyzer.run()
