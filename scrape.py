from flask import Flask, jsonify, request
import tweepy

# Set up Twitter API credentials
consumer_key = 'your_consumer_key_here'
consumer_secret = 'your_consumer_secret_here'
access_token = 'your_access_token_here'
access_token_secret = 'your_access_token_secret_here'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up Tweepy API client
api = tweepy.API(auth)

app = Flask(__name__)

@app.route('/tweets', methods=['GET'])
def get_tweets():
    """
    This script defines a REST API using Flask to scrape tweets based on a specific query.

    To use this API, start the Flask app by running this script, and then make GET requests to the
    /tweets endpoint with a 'q' query parameter to search for tweets.

    Example usage:
        http://localhost:5000/tweets?q=python

    The API returns a list of tweets in JSON format, with the following information for each tweet:
        - id: The tweet ID as a string
        - text: The text of the tweet
        - created_at: The timestamp of when the tweet was created, formatted as 'YYYY-MM-DD HH:MM:SS'
        - user: A dictionary containing information about the tweet's user, including:
            - id: The user ID as a string
            - name: The user's display name
            - screen_name: The user's Twitter handle
        - retweet_count: The number of times the tweet has been retweeted
        - favorite_count: The number of times the tweet has been favorited

    Dependencies:
        - Flask
        - Tweepy

    Credentials:
        To use this script, you need to set up Twitter API credentials and replace the placeholders with your own
        credentials. You can create a Twitter developer account and obtain API keys and access tokens from the
        Twitter Developer Portal: https://developer.twitter.com/en/portal/dashboard
    """
    
    # Get query parameter from request URL
    query = request.args.get('q')

    # Use Tweepy to search for tweets based on the query
    tweets = api.search(q=query)

    # Extract relevant information from each tweet and store in a list
    tweet_data = []
    for tweet in tweets:
        tweet_info = {
            'id': tweet.id_str,
            'text': tweet.text,
            'created_at': tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user': {
                'id': tweet.user.id_str,
                'name': tweet.user.name,
                'screen_name': tweet.user.screen_name,
            },
            'retweet_count': tweet.retweet_count,
            'favorite_count': tweet.favorite_count,
        }
        tweet_data.append(tweet_info)

    # Return the list of tweets in JSON format
    return jsonify(tweet_data)

if __name__ == '__main__':
    app.run()
