import logging
from classes.download_manager import DownloadManager
from functions.downloadmanager_helper import load_results_df, save_results_df
from config.constants import DEFAULT_SAVE_DIRECTORY


def main():
    # Set up logging
    logging.basicConfig(filename='logs/download.log', level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

   
    # Load the results DataFrame
    results_df = load_results_df('input/results_df.csv')

    # Initialize DownloadManager with default save directory
    download_manager = DownloadManager(save_directory=DEFAULT_SAVE_DIRECTORY, delay=1)

    # Process the downloads and get the download links
    download_links = download_manager.process_downloads(results_df)

    # Add the download links to the DataFrame
    results_df['download_link'] = download_links

    # Save the updated DataFrame to output
    save_results_df(results_df, os.path.join(DEFAULT_SAVE_DIRECTORY, "filter_output_with_download_links.csv"))


    logging.info("DataFrame with download links saved to 'filter_output_with_download_links.csv'")

if __name__ == "__main__":
    main()
