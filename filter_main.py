import logging
from classes.filtermanager import FilterManager
from functions.filterhelpers import load_metadata_df, save_results_df
from config.constants import FILTER_ENDPOINT, SUBMIT_ENDPOINT_TEMPLATE

def main():
    # Set up logging
    logging.basicConfig(filename='logs/execution.log', level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Load input metadata
    metadata_df = load_metadata_df('input/metadata.csv')

    # Initialize FilterManager
    filter_manager = FilterManager(
        filter_endpoint=FILTER_ENDPOINT,
        submit_endpoint_template=SUBMIT_ENDPOINT_TEMPLATE,
        delay=1
    )

    # Process filters and get results
    results_df = filter_manager.process_filters(metadata_df)

    # Save results to output
    save_results_df(results_df, 'output/metadata_with_filter_output_ids.csv')

    logging.info("DataFrame with filter_output_id saved to 'output/metadata_with_filter_output_ids.csv'")

if __name__ == "__main__":
    main()
