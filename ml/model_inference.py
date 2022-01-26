import os
import sys
import pandas as pd
import pickle
from treeinterpreter import treeinterpreter as ti
from ml.feature_extractor import extract_all_features


DIR_PATH = os.path.dirname(os.path.abspath(__file__))


def query_model(query_data):
    """
    query_data - A dictionary containing Twitter profile data from Twitter API
    """
    try:
        features = extract_all_features(query_data)
    except Exception as e:
        print(f"Feature extraction failed: {e}")
        return None

    del features['id']

    model = pickle.load(open(os.path.join(DIR_PATH, "model", "model.pkl"), 'rb'))
    scaler = pickle.load(open(os.path.join(DIR_PATH, "model", "scaler.pkl"), 'rb'))

    df = pd.DataFrame(data=[features])
    scaled_data = scaler.transform(df)
    prediction, explanations = get_prediction(model, scaled_data)
    return prediction, explanations

def get_prediction(model, df):
    prediction, bias, contributions = ti.predict(model, df)
    score = round(prediction[0][0], 2)
    feature_names = model.feature_names_in_
    feature_contrs = zip(contributions[0], feature_names)
    feature_contrs = sorted(feature_contrs, key=lambda x: -abs(x[0]))

    print("Full contributions list\n-------------------")
    for contr, feature in feature_contrs:
        print(f"{feature}: {contr:.3f}")
    print("-------------------")

    return score, select_explanations(feature_contrs)


def select_explanations(feature_contrs, count_per_type=3):
    positive_features = []
    negative_features = []
    all_selected_features = []
    for i in range(len(feature_contrs)):
        contr, feature = feature_contrs[i]
        contr = round(contr, 2)
        feature_name = get_feature_human_name(feature)
        if not feature_name or feature_name in all_selected_features:
            continue
        if contr > 0 and len(positive_features) < count_per_type:
            positive_features.append({
                "name": feature_name,
                "contribution": contr
            })
            if len(positive_features) == count_per_type and len(negative_features) == count_per_type:
                break
        elif contr < 0 and len(negative_features) < count_per_type:
            negative_features.append({
                "name": feature_name,
                "contribution": contr
            })
            if len(positive_features) == count_per_type and len(negative_features) == count_per_type:
                break

    return {
        "positives": positive_features,
        "negatives": negative_features
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
    elif feature_name.startswith("tweet.sentiment."):
        return "Sentiment of tweets"


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