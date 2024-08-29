import os
import requests
import time
import logging

class DownloadManager:
    def __init__(self, save_directory, delay=1):
        self.save_directory = save_directory
        self.delay = delay
        self.logger = logging.getLogger(__name__)
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
            self.logger.info(f"Created directory: {self.save_directory}")

    def download_csv(self, table_code, geography_level, filter_output_id):
        filter_output_url = f"https://api.beta.ons.gov.uk/v1/filter-outputs/{filter_output_id}"
        response = requests.get(filter_output_url)

        if response.status_code == 200:
            filter_output_details = response.json()
            if 'csv' in filter_output_details['downloads']:
                csv_url = filter_output_details['downloads']['csv']['public']
                file_path = self._save_csv_file(table_code, geography_level, csv_url)
                if file_path:
                    self.logger.info(f"Data for {table_code} ({geography_level}) downloaded successfully and saved to {file_path}.")
                    return csv_url
                else:
                    self.logger.error(f"Failed to download CSV for {table_code} ({geography_level}).")
                    return None
            else:
                self.logger.warning(f"CSV format not available for {table_code} ({geography_level}).")
                return None
        else:
            self.logger.error(f"Failed to retrieve filter output details for {table_code} ({geography_level}). Status Code: {response.status_code}")
            return None

    def _save_csv_file(self, table_code, geography_level, csv_url):
        csv_response = requests.get(csv_url, stream=True)
        if csv_response.status_code == 200:
            file_path = os.path.join(self.save_directory, f"{table_code}_{geography_level}_data.csv")
            with open(file_path, "wb") as file:
                for chunk in csv_response.iter_content(chunk_size=128):
                    file.write(chunk)
            return file_path
        return None

    def process_downloads(self, results_df):
        download_links = []
        for index, row in results_df.iterrows():
            csv_url = self.download_csv(row['table_code'], row['geography_level'], row['filter_output_id'])
            download_links.append(csv_url)
            time.sleep(self.delay)
        return download_links
