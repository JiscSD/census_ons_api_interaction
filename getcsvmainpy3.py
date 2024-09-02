import pandas as pd
from Functions.api_download import process_filtermetadata

def main():
    # Load your metadata DataFrame from wherever it is stored
    metadata_df = pd.read_csv(r"input\filter_outputid.csv")

    # Process the metadata and get the results DataFrame
    results_df = process_filtermetadata (metadata_df)

    # Display the updated DataFrame with separate rows for each geography level
    print(results_df)

    # Save the updated DataFrame to a CSV file
    results_df.to_csv('output/metadata_with_filter_output_ids.csv', index=False)
    print("DataFrame with filter_output_id saved to 'output/metadata_with_filter_output_ids.csv'")

if __name__ == "__main__":
    main()
