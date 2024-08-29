from Functions.logger import  get_logger
import logging
from classes.metadata_fetcher import MetadataFetcher
from functions.helpers import load_geography_df, save_metadata_df, delay_execution

#Logging functionality
# https://docs.python.org/3/howto/logging.html#a-simple-example
logging = get_logger()

#Start of the script
def main():
    # Set up logging
    logging.basicConfig(filename='logs/execution.log', level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Load input data
    geography_df = load_geography_df('input/geography_combinations.csv')

    # Initialize MetadataFetcher
    fetcher = MetadataFetcher(edition="2021", delay=1)

    # Initialize a list to store metadata
    metadata_list = []

    # Loop through each table_code and retrieve metadata
    for index, row in geography_df.iterrows():
        table_code = row['table_code']
        metadata, latest_version = fetcher.fetch_metadata(table_code)
        
        if metadata:
            extracted_metadata = fetcher.extract_metadata(metadata, latest_version, row['geography_combinations'])
            metadata_list.append({
                "table_code": table_code,
                **extracted_metadata
            })
            logging.info(f"Metadata for {table_code} (version {latest_version}) retrieved successfully.")
        
        # Delay before the next request
        delay_execution(fetcher.delay)

    # Save metadata to output
    save_metadata_df(metadata_list, 'output/metadata.csv')

if __name__ == "__main__":
    main()
