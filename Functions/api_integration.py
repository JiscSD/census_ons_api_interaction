import requests
import pandas as pd
import time
from Classes.constants import Config

def process_metadata(metadata_df):
    """Main function to process metadata and interact with the ONS API."""
    results_df = pd.DataFrame(columns=[
        'table_code', 'population_type', 'edition', 'version', 
        'unit_of_measure', 'dimensions', 'geography_level', 'filter_output_id'
    ])

    for index, row in metadata_df.iterrows():
        table_code, edition, version, population_type, dimensions, geography_combinations = extract_metadata(row)
        geography_combinations = parse_geography_combinations(geography_combinations)

        for geography_level in geography_combinations:
            filter_dimensions = build_filter_dimensions(dimensions, geography_level)

            # Construct the payload for the POST request
            payload = build_payload(table_code, edition, version, population_type, filter_dimensions)
            
            # Make the POST request to create the filter and handle the response
            handle_filter_creation(payload, table_code, geography_level, results_df, row)

            # Optionally, delay between requests to avoid overwhelming the server
            time.sleep(Config.SLEEP_INTERVAL)

    return results_df

def extract_metadata(row):
    """Extract metadata from a DataFrame row."""
    table_code = row['table_code']
    edition = str(row['edition'])  # Ensure edition is treated as a string
    version = row['version']
    population_type = row['population_type']
    dimensions = eval(row['dimensions'])  # Convert the string representation to a list of dictionaries
    geography_combinations = eval(row['geography_combinations'])  # Convert the string representation to a set
    return table_code, edition, version, population_type, dimensions, geography_combinations

def parse_geography_combinations(geography_combinations):
    """Parse and clean up geography combinations."""
    return {g.strip("' ") for g in geography_combinations}

def build_filter_dimensions(dimensions, geography_level):
    """Build filter dimensions, ensuring no duplicates."""
    filter_dimensions = []
    for dimension in dimensions:
        if isinstance(dimension, dict) and "name" in dimension:
            filter_dimensions.append(dimension)
    
    # Ensure we don't already have a geography level included
    if not any(d.get("is_area_type", False) for d in filter_dimensions):
        filter_dimensions.insert(0, {"name": geography_level, "is_area_type": True})

    return filter_dimensions

def build_payload(table_code, edition, version, population_type, filter_dimensions):
    """Build the payload for the API request."""
    return {
        "dataset": {
            "id": table_code,
            "edition": edition,
            "version": version
        },
        "population_type": population_type,
        "dimensions": filter_dimensions
    }

def handle_filter_creation(payload, table_code, geography_level, results_df, row):
    """Handle the filter creation process and response."""
    response = create_filter(payload)
    
    if response and response.status_code == 201:  # 201 Created is the success status code
        filter_id = response.json()['filter_id']
        print(f"Filter created successfully for {table_code} at geography level {geography_level}. Filter ID: {filter_id}")
        
        # Now submit the filter to get the filter_output_id
        filter_output_id = submit_filter(filter_id)
        
        if filter_output_id:
            append_result(results_df, row, table_code, geography_level, filter_output_id)
        else:
            print(f"Failed to submit filter {filter_id}.")
    else:
        print(f"Failed to create filter for {table_code} at geography level {geography_level}. Status Code: {response.status_code} - {response.text}")

def append_result(results_df, row, table_code, geography_level, filter_output_id):
    """Append the result to the DataFrame."""
    new_row = pd.DataFrame([{
        'table_code': table_code,
        'population_type': row['population_type'],
        'edition': row['edition'],
        'version': row['version'],
        'unit_of_measure': row['unit_of_measure'],
        'dimensions': row['dimensions'],
        'geography_level': geography_level,
        'filter_output_id': filter_output_id
    }])
    results_df = pd.concat([results_df, new_row], ignore_index=True)

def create_filter(payload):
    """Function to create a filter using the ONS API."""
    response = requests.post(Config.FILTER_ENDPOINT, json=payload)
    return response

def submit_filter(filter_id):
    """Function to submit a filter and return the filter_output_id."""
    submit_endpoint = Config.SUBMIT_ENDPOINT_TEMPLATE.format(filter_id=filter_id)
    submit_response = requests.post(submit_endpoint)
    
    if submit_response.status_code == 202:  # 202 Accepted for asynchronous processing
        filter_output_id = submit_response.json()['filter_output_id']
        print(f"Filter submitted successfully. Filter Output ID: {filter_output_id}")
        return filter_output_id
    else:
        print(f"Failed to submit filter {filter_id}. Status Code: {submit_response.status_code} - {submit_response.text}")
        return None
