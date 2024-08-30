import requests
import logging
import pandas as pd
from config.constants import FILTER_ENDPOINT, SUBMIT_ENDPOINT_TEMPLATE


class FilterManager:
    def __init__(self, delay=1):
        self.filter_endpoint = FILTER_ENDPOINT
        self.submit_endpoint_template = SUBMIT_ENDPOINT_TEMPLATE
        self.delay = delay
        self.logger = logging.getLogger(__name__)

    def create_filter(self, table_code, edition, version, population_type, dimensions, geography_level):
        filter_dimensions = [{"name": geography_level, "is_area_type": True}]
        for dimension in dimensions:
            filter_dimensions.append({"name": dimension["name"]})

        payload = {
            "dataset": {
                "id": table_code,
                "edition": edition,
                "version": version
            },
            "population_type": population_type,
            "dimensions": filter_dimensions
        }
        
        response = requests.post(self.filter_endpoint, json=payload)
        if response.status_code == 201:
            filter_id = response.json().get('filter_id')
            self.logger.info(f"Filter created successfully for {table_code} at geography level {geography_level}. Filter ID: {filter_id}")
            return filter_id
        else:
            self.logger.error(f"Failed to create filter for {table_code} at geography level {geography_level}. Status Code: {response.status_code} - {response.text}")
            return None

    def submit_filter(self, filter_id):
        submit_endpoint = self.submit_endpoint_template.format(filter_id=filter_id)
        response = requests.post(submit_endpoint)
        if response.status_code == 202:
            filter_output_id = response.json().get('filter_output_id')
            self.logger.info(f"Filter submitted successfully. Filter Output ID: {filter_output_id}")
            return filter_output_id
        else:
            self.logger.error(f"Failed to submit filter {filter_id}. Status Code: {response.status_code} - {response.text}")
            return None

    def process_filters(self, metadata_df):
        results_df = pd.DataFrame(columns=[
            'table_code', 'population_type', 'edition', 'version', 
            'unit_of_measure', 'dimensions', 'geography_level', 'filter_output_id'
        ])

        for index, row in metadata_df.iterrows():
            table_code = row['table_code']
            edition = row['edition']
            version = row['version']
            population_type = row['population_type']
            dimensions = row['dimensions']
            geography_combinations = row['geography_combinations']

            geography_combinations = self._process_geography_combinations(geography_combinations)
            
            for geography_level in geography_combinations:
                filter_id = self.create_filter(table_code, edition, version, population_type, dimensions, geography_level)
                if filter_id:
                    filter_output_id = self.submit_filter(filter_id)
                    if filter_output_id:
                        new_row = pd.DataFrame([{
                            'table_code': table_code,
                            'population_type': population_type,
                            'edition': edition,
                            'version': version,
                            'unit_of_measure': row['unit_of_measure'],
                            'dimensions': dimensions,
                            'geography_level': geography_level,
                            'filter_output_id': filter_output_id
                        }])
                        results_df = pd.concat([results_df, new_row], ignore_index=True)
                
                # Optionally, delay between requests to avoid overwhelming the server
                time.sleep(self.delay)
        
        return results_df

    def _process_geography_combinations(self, geography_combinations):
        if isinstance(geography_combinations, str):
            return geography_combinations.strip('{}').split(', ')
        elif isinstance(geography_combinations, set):
            return list(geography_combinations)
        return []

