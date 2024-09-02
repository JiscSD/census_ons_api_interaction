import os
import requests
import time
import pandas as pd
from Classes.constants import SAVE_DIRECTORY

# Directory where files will be saved
SAVE_DIRECTORY = SAVE_DIRECTORY

def ensure_directory_exists(directory):
    """Ensure that the specified directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def process_filtermetadata(metadata_df):
    # Ensure the save directory exists
    ensure_directory_exists(SAVE_DIRECTORY)

    # Initialize a list to store the download links
    download_links = []

    # Loop through each row in the DataFrame
    for index, row in metadata_df.iterrows():
        table_code = row['table_code']
        geography_level = row['geography_level']
        filter_output_id = row['filter_output_id']

        # Fetch filter output details
        filter_output_details = fetch_filter_output_details(filter_output_id)
        
        if filter_output_details and 'csv' in filter_output_details['downloads']:
            csv_url = filter_output_details['downloads']['csv']['public']
            filename = f"{table_code}_{geography_level}_data.csv"
            download_path = download_csv(csv_url, SAVE_DIRECTORY, filename)
            download_links.append(download_path)
        else:
            download_links.append(None)
        
        # Delay for 3 seconds before processing the next row
        time.sleep(3)

    # Add the download links to the original DataFrame
    metadata_df['download_link'] = download_links

    # Return the updated DataFrame
    return metadata_df

def fetch_filter_output_details(filter_output_id):
    url = f"https://api.beta.ons.gov.uk/v1/filter-outputs/{filter_output_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve filter output details. Status Code: {response.status_code}")
        return None

def download_csv(url, save_directory, filename):
    csv_response = requests.get(url, stream=True)
    if csv_response.status_code == 200:
        file_path = os.path.join(save_directory, filename)
        with open(file_path, "wb") as file:
            for chunk in csv_response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Data downloaded successfully and saved to {file_path}.")
        return file_path
    else:
        print(f"Failed to download CSV. Status Code: {csv_response.status_code}")
        return None
