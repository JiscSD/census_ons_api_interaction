from Functions.api_call import retrieve_metadata
import pandas as pd

# Assuming you have a DataFrame `geography_df` ready to use
geography_df = pd.read_csv('Input/your_input_file.csv')  # Example loading of input

# Call the function to retrieve metadata
metadata_df = retrieve_metadata(geography_df)

# Save the output to a file
metadata_df.to_csv('Output/metadata_output.csv', index=False)

# If you want to display the DataFrame (optional)
print(metadata_df)
