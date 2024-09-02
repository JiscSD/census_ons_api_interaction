import requests
import time
import pandas as pd
from Classes.constants import Config

def get_versions(table_code):
    versions_url = f"{Config.BASE_URL}/{table_code}/editions/{Config.EDITION}/versions"
    response = requests.get(versions_url)
    
    if response.status_code == 200:
        versions_data = response.json()
        return versions_data["items"] if len(versions_data["items"]) > 0 else None
    else:
        print(f"Failed to retrieve versions for {table_code}. Status Code: {response.status_code}")
        return None

def get_metadata(table_code, version):
    metadata_url = f"{Config.BASE_URL}/{table_code}/editions/{Config.EDITION}/versions/{version}/metadata"
    response = requests.get(metadata_url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve metadata for {table_code}. Status Code: {response.status_code}")
        return None

def extract_metadata(metadata, table_code, version, geography_combinations):
    population_type = metadata["is_based_on"]["@id"]
    unit = metadata.get('unit_of_measure', 'N/A')
    
    dimensions = []
    for dimension in metadata["dimensions"]:
        if not dimension.get("is_area_type", False):
            dimensions.append({
                "name": dimension["name"],
                "is_area_type": dimension.get("is_area_type", False)
            })
    
    return {
        "table_code": table_code,
        "population_type": population_type,
        "edition": Config.EDITION,
        "version": version,
        "unit_of_measure": unit,
        "dimensions": dimensions,
        "geography_combinations": geography_combinations
    }

def retrieve_metadata(geography_df):
    metadata_list = []

    for index, row in geography_df.iterrows():
        table_code = row['table_code']
        
        # Retrieve versions for the given table_code and edition
        versions = get_versions(table_code)
        
        if versions:
            latest_version = versions[0]["version"]
            
            # Retrieve metadata for the latest version
            metadata = get_metadata(table_code, latest_version)
            
            if metadata:
                # Extract relevant fields from the metadata
                metadata_entry = extract_metadata(metadata, table_code, latest_version, row['geography_combinations'])
                metadata_list.append(metadata_entry)
                
                print(f"Metadata for {table_code} (version {latest_version}) retrieved successfully.")
        else:
            print(f"No versions available for {table_code}. Skipping this dataset.")
        
        time.sleep(Config.TIME_DELAY)

    metadata_df = pd.DataFrame(metadata_list)
    return metadata_df
