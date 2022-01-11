import os
import sys
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from treeinterpreter import treeinterpreter as ti
from feature_extractor import extract_all_features


DIR_PATH = os.path.dirname(os.path.abspath(__file__))


def query_model(query_data):
    """
    query_data - A dictionary containing Twitter profile data from Twitter API
    """
    features = extract_all_features(query_data)
    del features['id']

    model = pickle.load(open(os.path.join(DIR_PATH, "model", "model.pkl"), 'rb'))
    scaler = pickle.load(open(os.path.join(DIR_PATH, "model", "scaler.pkl"), 'rb'))

    df = pd.DataFrame(data=[features])
    explanations = get_explanations(model, df)
    scaled_data = scaler.transform(df)
    prediction = model.predict(scaled_data)
    return prediction[0], explanations

def get_explanations(model, df, count=6):
    prediction, bias, contributions = ti.predict(model, df)

    feature_names = model.feature_names_in_
    positives = []
    negatives = []

    for i in range(len(df)):
        feature_contrs = zip(contributions[i], feature_names)
        feature_contrs = sorted(feature_contrs, key=lambda x: -abs(x[0]))
        used_feature_count = min(count, len(feature_contrs))
        feature_contrs = feature_contrs[0:used_feature_count]
        for contr, feature in feature_contrs:
            feature_name = get_feature_human_name(feature)
            if contr > 0:
                positives.append(feature_name)
            else:
                negatives.append(feature_name)
    return {
        "positives": positives,
        "negatives": negatives
    }


def get_feature_human_name(feature_name):
    if feature_name == "tweet.replies_mean":
        return "Amount of replies to tweets"
    elif feature_name == "tweet.mentions_mean":
        return "Amount of mentions in tweets"
    elif feature_name == "created_at":
        return "Profile age"
    elif feature_name == "name_len":
        return "Profile name"
    elif feature_name == "tweet_count":
        return "Amount of tweets posted"
    elif feature_name == "following_followers_ratio":
        return "Followers"
    elif feature_name == "tweet.length_mean":
        return "Tweet length"
    elif feature_name == "desc_words":
        return "Profile description"
    elif feature_name == "verified":
        return "Verified profile status"
    elif feature_name == "listed_count":
        return "Appearance of profile in public lists"
    else:
        return feature_name


if __name__ == '__main__':
    import json
    if len(sys.argv) > 1:
        profile_id = sys.argv[1]
    else:
        profile_id = "32193"
    test_json_path = os.path.join(DIR_PATH, "data", "twitter_profiles", profile_id)
    with open(test_json_path, 'r') as json_file:
        query_data = json.load(json_file)
        result = query_model(query_data)
        print(f"Credibility for profile {profile_id}: {result}")