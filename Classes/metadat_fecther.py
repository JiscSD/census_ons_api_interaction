import requests
import logging

class MetadataFetcher:
    def __init__(self, edition="2021", delay=1):
        self.edition = edition
        self.delay = delay
        self.logger = logging.getLogger(__name__)

    def fetch_metadata(self, table_code):
        versions_url = f"https://api.beta.ons.gov.uk/v1/datasets/{table_code}/editions/{self.edition}/versions"
        versions_response = requests.get(versions_url)

        if versions_response.status_code == 200:
            versions_data = versions_response.json()
            if len(versions_data["items"]) > 0:
                latest_version = versions_data["items"][0]["version"]
                metadata_url = f"https://api.beta.ons.gov.uk/v1/datasets/{table_code}/editions/{self.edition}/versions/{latest_version}/metadata"
                response = requests.get(metadata_url)

                if response.status_code == 200:
                    return response.json(), latest_version
                else:
                    self.logger.error(f"Failed to retrieve metadata for {table_code}. Status Code: {response.status_code}")
            else:
                self.logger.warning(f"No versions available for {table_code}. Skipping this dataset.")
        else:
            self.logger.error(f"Failed to retrieve versions for {table_code}. Status Code: {versions_response.status_code}")
        return None, None

    def extract_metadata(self, metadata, latest_version, geography_combinations):
        population_type = metadata["is_based_on"]["@id"]
        unit = metadata.get('unit_of_measure', 'N/A')
        dimensions = [
            {"name": dimension["name"], "is_area_type": dimension.get("is_area_type", False)}
            for dimension in metadata["dimensions"]
            if not dimension.get("is_area_type", False)
        ]
        return {
            "population_type": population_type,
            "edition": self.edition,
            "version": latest_version,
            "unit_of_measure": unit,
            "dimensions": dimensions,
            "geography_combinations": geography_combinations
        }
