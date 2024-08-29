import os
import pandas as pd

def load_results_df(file_path):
    return pd.read_csv(file_path)

def save_results_df(results_df, output_path):
    results_df.to_csv(output_path, index=False)

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
