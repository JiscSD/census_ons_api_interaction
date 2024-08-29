import logging
from classes.filter_manager import FilterManager
from functions.helpers import load_metadata_df, save_results_df

def main():
    # Set up logging
    logging.basicConfig(filename='logs/execution.log', level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Load input metadata
    metadata_df = load_metadata_df('input/metadata.csv')

    # Initialize FilterManager
    filter_manager = FilterManager(
        filter_endpoint="https://api.beta.ons.gov.uk/v1/filters?submitted=true",
        submit_endpoint_template="https://api.beta.ons.gov.uk/v1/filters/{filter_id}/submit",
        delay=1
    )

    # Process filters and get results
    results_df = filter_manager.process_filters(metadata_df)

    # Save results to output
    save_results_df(results_df, 'output/metadata_with_filter_output_ids.csv')

    logging.info("DataFrame with filter_output_id saved to 'output/metadata_with_filter_output_ids.csv'")

if __name__ == "__main__":
    main()
