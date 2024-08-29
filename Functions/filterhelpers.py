import pandas as pd
import time

def load_metadata_df(file_path):
    return pd.read_csv(file_path)

def save_results_df(results_df, output_path):
    results_df.to_csv(output_path, index=False)

def delay_execution(seconds):
    time.sleep(seconds)
