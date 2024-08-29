import pandas as pd
import time

def load_geography_df(file_path):
    return pd.read_csv(file_path)

def save_metadata_df(metadata_list, output_path):
    metadata_df = pd.DataFrame(metadata_list)
    metadata_df.to_csv(output_path, index=False)

def delay_execution(seconds):
    time.sleep(seconds)
