import os
import pandas as pd
import json
import random
import py7zr
import csv
from feature_extractor import extract_all_features, validate_profiles
from common.logger import logger

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def get_dataset():
    df = pd.DataFrame()
    df_data = []
    profiles = read_all_profile_jsons()
    for profile in profiles:
        features = extract_all_features(profile)
        if features:
            df_data.append(features)

    df_data = add_labels(df_data)
    df = pd.DataFrame(data=df_data)
    return df


def add_labels(df_data):
    labels_dir = os.path.join(DIR_PATH, "data", "labels")
    scores_by_profile = {}

    for label_file_name in os.listdir(labels_dir):
        label_file_path = os.path.join(labels_dir, label_file_name)
        with open(label_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            header_found = False
            for row in csv_reader:
                if not header_found and row[0] == 'profile_id':
                    header_found = True
                elif header_found:
                    profile_id = row[0]
                    try:
                        credibility_score = int(row[2])
                    except ValueError:
                        continue
                    if profile_id not in scores_by_profile:
                        scores_by_profile[profile_id] = [credibility_score]
                    else:
                        scores_by_profile[profile_id].append(credibility_score)

    labeled_data = []
    for profile in df_data:
        scores = scores_by_profile.get(profile['id'])
        if scores:
            score_mean = sum(scores) / len(scores)
            profile['credibility_score'] = score_mean
            labeled_data.append(profile)
    logger.info(f"Labeled dataset size: {len(labeled_data)}")
    return labeled_data

def read_all_profile_jsons():
    logger.info("Reading profile JSONs")
    jsons_path = unzip_profile_jsons()
    profiles = []
    for filename in os.listdir(jsons_path):
        path = os.path.join(jsons_path, filename)
        with open(path, 'r') as json_file:
            profiles.append(json.load(json_file))
    profiles = validate_profiles(profiles)
    return profiles


def get_random_profiles(num=50):
    all_profiles = read_all_profile_jsons()
    logger.info(f"Choosing {num} profiles from total of {len(all_profiles)} profiles")
    selected_profiles = random.sample(all_profiles, num)

    csv_data = [["profile_id", "profile_url", "credibility"]]
    for profile in selected_profiles:
        profile_url = f"https://twitter.com/{profile['username']}"
        csv_data.append([profile["id"], profile_url, ""])
    csv_path = os.path.join(DIR_PATH, "data", "random-profiles.csv")
    with open(csv_path, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=",", quotechar="'", quoting=csv.QUOTE_MINIMAL)
        for csv_row in csv_data:
            writer.writerow(csv_row)
    logger.info("Done")

def unzip_profile_jsons():
    jsons_path = os.path.join(DIR_PATH, "data", "twitter_profiles")

    if not os.path.isdir(jsons_path):
        dataset_7z = os.path.join(DIR_PATH, "data", "Twitter Profiles data.7z")
        os.mkdir(jsons_path)
        with py7zr.SevenZipFile(dataset_7z, mode='r') as zip:
            zip.extractall(jsons_path)
    return jsons_path


if __name__ == "__main__":
    #get_random_profiles()
    get_dataset()
