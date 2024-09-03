import pandas as pd
from Functions.api_call import retrieve_metadata
from Functions.api_integration import process_metadata
from Functions.api_download import process_filtermetadata

def main():
    # Process 1: Retrieve metadata
    geography_df = pd.read_csv('Input/geocomb.csv')  # Load input DataFrame
    metadata_df = retrieve_metadata(geography_df)    # Retrieve metadata
    metadata_df.to_csv('Output/metadata_output.csv', index=False)  # Save output
    print("Step 1: Metadata retrieved and saved to 'Output/metadata_output.csv'.")
    print(metadata_df)  # Display DataFrame (optional)

    # Process 2: Process the retrieved metadata
    processed_metadata_df = process_metadata(metadata_df)  # Process metadata
    processed_metadata_df.to_csv('Output/metadata_with_filter_output_ids.csv', index=False)  # Save output
    print("Step 2: Metadata processed and saved to 'Output/metadata_with_filter_output_ids.csv'.")
    print(processed_metadata_df)  # Display updated DataFrame

    # Process 3: Process metadata with filter output IDs
    filteroutput_id = pd.read_csv(r"input\filter_outputid.csv")  # Load filter output ID DataFrame
    final_results_df = process_filtermetadata(filteroutput_id)   # Process filter metadata
    final_results_df.to_csv('output/final_metadata_output.csv', index=False)  # Save final output
    print("Step 3: Final metadata processed and saved to 'output/final_metadata_output.csv'.")
    print(final_results_df)  # Display final DataFrame

if __name__ == "__main__":
    main()
