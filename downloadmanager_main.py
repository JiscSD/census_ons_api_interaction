import logging
from classes.download_manager import downloadmanager
from functions.downloadmanager_helper import load_results_df, save_results_df

def main():
    # Set up logging
    logging.basicConfig(filename='logs/download.log', level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Define the directory to save CSV files
    save_directory = r"C:\Users\directoryname"

    # Load the results DataFrame
    results_df = load_results_df('input/results_df.csv')

    # Initialize DownloadManager
    download_manager = DownloadManager(save_directory, delay=1)

    # Process the downloads and get the download links
    download_links = download_manager.process_downloads(results_df)

    # Add the download links to the DataFrame
    results_df['download_link'] = download_links

    # Save the updated DataFrame to output
    save_results_df(results_df, os.path.join(save_directory, "filter_output_with_download_links.csv"))

    logging.info("DataFrame with download links saved to 'filter_output_with_download_links.csv'")

if __name__ == "__main__":
    main()
