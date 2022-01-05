import os
import sys
import pandas as pd
import pickle
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
    scaled_data = scaler.transform(df)
    prediction = model.predict(scaled_data)
    return prediction[0]


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