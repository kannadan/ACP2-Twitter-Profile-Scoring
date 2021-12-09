import os
import zipfile
import pandas as pd
import json
import random
import py7zr
import csv
from feature_extractor import extract_all_features, validate_profiles

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

def read_dataset():
    csv_path = os.path.join(os.getcwd(), "data", "gender-classifier-DFE-791531.csv")

    if not os.path.isfile(csv_path):
        # Load dataset
        dataset_zip = os.path.join(os.getcwd(), "data", "dataset.zip")
        with zipfile.ZipFile(dataset_zip, 'r') as zip:
            zip.extractall("data")
    
    df = pd.read_csv(csv_path, sep=",", encoding="ISO-8859-1")
    return df


def get_validated_dataset():
    df = pd.DataFrame()
    df_data = []
    profiles = read_all_profile_jsons()
    for profile in profiles:
        features = extract_all_features(profile)
        if features:
            df_data.append(features)

    df = pd.DataFrame(data=df_data)
    return df


def read_all_profile_jsons():
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
    print(f"Choosing {num} profiles from total of {len(all_profiles)} profiles")
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
    print("Done")

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
    get_validated_dataset()
