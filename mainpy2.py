import pandas as pd
from Functions.api_integration import process_metadata

def main():
    # Load your metadata DataFrame from wherever it is stored
    metadata_df = pd.read_csv("input\metadata.csv")  # 

    # Process the metadata and get the results DataFrame
    results_df = process_metadata(metadata_df)

    # Display the updated DataFrame with separate rows for each geography level
    print(results_df)

    # Save the updated DataFrame to a CSV file
    results_df.to_csv('metadata_with_filter_output_ids.csv', index=False)
    print("DataFrame with filter_output_id saved to 'metadata_with_filter_output_ids.csv'")

if __name__ == "__main__":
    main()
