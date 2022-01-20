import datetime
import nltk
nltk.download([
    "vader_lexicon"
])
from nltk.sentiment import SentimentIntensityAnalyzer

def extract_all_features(profile):
    metrics = profile["public_metrics"]
    features = {
        #"location": profile_data["location"],
        "id": profile["id"],
        "verified": int(profile["verified"]),
        "name_len": len(profile["name"]),
        "followers_count": metrics["followers_count"],
        "following_count": metrics["following_count"],
        "tweet_count": metrics["tweet_count"],
        "listed_count": metrics["listed_count"],
        "has_url": int(bool(profile.get("url"))),
        "created_at": datetime.datetime.fromisoformat(profile["created_at"].split('.')[0]).timestamp()
    }
    description = profile["description"]
    if description:
        features["desc_len"] = len(description)
        features["desc_words"] = len(profile["description"].split(" ")) + 1
    else:
        features["desc_len"] = 0
        features["desc_words"] = 0

    if features['followers_count'] > 0:
        features["following_followers_ratio"] = features['following_count'] / features['followers_count']
    else:
        features["following_followers_ratio"] = 999999


    tweet_features = get_tweet_features(profile)
    if not tweet_features:
        return None
    features.update(tweet_features)
    return features


def get_tweet_features(profile):
    tweets = profile["tweets"]
    retweet_count = 0
    own_tweet_count = 0

    total_tweet_len = 0
    total_tweet_words = 0
    total_retweet_count = 0
    total_reply_count = 0
    total_like_count = 0
    total_quote_count = 0
    total_mentions_count = 0

    sia = SentimentIntensityAnalyzer()
    sentiments = {
        "compound": 0,
        "pos": 0,
        "neg": 0,
        "neu": 0
    }

    for tweet in tweets:
        ref_tweets = tweet.get("referenced_tweets", [])
        if ref_tweets and ref_tweets[0]["type"] == "retweeted":
            retweet_count += 1
            continue
        own_tweet_count += 1
        tweet_metrics = tweet["public_metrics"]
        tweet_text = tweet["text"]
        total_tweet_len += len(tweet_text)
        total_tweet_words += len(tweet_text.split(" "))

        polarity_scores = sia.polarity_scores(tweet_text)
        sentiments["compound"] += polarity_scores["compound"]
        sentiments["pos"] += polarity_scores["pos"]
        sentiments["neg"] += polarity_scores["neg"]
        sentiments["neu"] += polarity_scores["neu"]
        total_retweet_count += tweet_metrics["retweet_count"]
        total_reply_count += tweet_metrics["reply_count"]
        total_like_count += tweet_metrics["like_count"]
        total_quote_count += tweet_metrics["quote_count"]
        total_mentions_count += len(tweet.get("entities", {}).get("mentions", []))
 
    if own_tweet_count == 0:
        return False
    tweet_count = len(tweets)
    return {
        "tweet.length_mean": total_tweet_len / own_tweet_count,
        "tweet.words_mean": total_tweet_words / own_tweet_count,
        "tweet.retweets_mean": total_retweet_count / own_tweet_count,
        "tweet.replies_mean": total_reply_count / own_tweet_count,
        "tweet.likes_mean": total_like_count / own_tweet_count,
        "tweet.quotes_mean": total_quote_count / own_tweet_count,
        "tweet.mentions_mean": total_mentions_count / own_tweet_count,
        "tweet.retweets_percentage": retweet_count / tweet_count,
        "tweet.sentiment.total": sentiments["compound"] / tweet_count,
        "tweet.sentiment.pos": sentiments["pos"] / tweet_count,
        "tweet.sentiment.neg": sentiments["neg"] / tweet_count,
        "tweet.sentiment.neu": sentiments["neu"] / tweet_count
    }


def validate_profile(profile):
    tweets = profile.get("tweets")
    if not tweets or len(tweets) < 5:
        return False, "Not enough tweets"
    
    is_english = False
    for tweet in tweets:
        if tweet.get("referenced_tweets"):
            continue
        if tweet.get("lang") == "en":
            is_english = True
    if not is_english:
        return False, "Not english"
    
    if profile.get("protected"):
        return False, "Protected profile"

    return True, ""


def validate_profiles(profiles):
    validated_profiles = []
    for profile in profiles:
        validation_result, validation_reason = validate_profile(profile)
        if validation_result:
            validated_profiles.append(profile)
    print(f"Filtered out {len(profiles) - len(validated_profiles)} profiles")
    return validated_profiles


