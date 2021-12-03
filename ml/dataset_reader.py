import os
import zipfile
import pandas as pd


def read_dataset():
    csv_path = os.path.join("data", "gender-classifier-DFE-791531.csv")

    if not os.path.isfile(csv_path):
        # Load dataset
        dataset_zip = os.path.join("data", "dataset.zip")
        with zipfile.ZipFile(dataset_zip, 'r') as zip:
            zip.extractall("data")
    
    df = pd.read_csv(csv_path, sep=",", encoding="ISO-8859-1")
    return df
