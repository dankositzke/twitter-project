"""Getting tweets and users from the Twitter DB"""
from os import getenv
import tweepy
import spacy
from twitoff.models import User, db, Tweet

TWITTER_AUTH = tweepy.OAuthHandler(
    getenv("TWITTER_API_KEY"), getenv("TWITTER_API_KEY_SECRET")
)
TWITTER = tweepy.API(TWITTER_AUTH)


# loads word2vect Model
nlp = spacy.load("en_core_web_sm")


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    """
    Gets twitter user and tweets from twitter DB
    Gets user by "username" parameter.
    """
    try:
        # gets back twitter user object
        twitter_user = TWITTER.get_user(screen_name=username)
        # Either updates or adds user to our DB
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, name=username
        )
        db.session.add(db_user)  # Add user if don't exist

        # Grabbing tweets from "twitter_user"
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False, tweet_mode="extended"
        )

        # tweets is a list of tweet objects
        for tweet in tweets:
            # type(tweet) == object
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=tweet_vector)
            db_user.tweets.append(db_tweet)
            db.session.add(db_tweet)

    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e

    else:
        db.session.commit()
