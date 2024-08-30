# Create a new file: config/constants.py

# Base URL for the API
BASE_API_URL = "https://api.beta.ons.gov.uk/v1"

# API Endpoints
FILTER_ENDPOINT = f"{BASE_API_URL}/filters?submitted=true"
SUBMIT_ENDPOINT_TEMPLATE = f"{BASE_API_URL}/filters/{{filter_id}}/submit"
FILTER_OUTPUT_URL_TEMPLATE = f"{BASE_API_URL}/filter-outputs/{{filter_output_id}}"

# Other constants
DEFAULT_SAVE_DIRECTORY = r"C:\Users\olajuwon.yakub\Downloads\New folder (3)"

