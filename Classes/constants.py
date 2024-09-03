# constants

class Config:
    BASE_URL = "https://api.beta.ons.gov.uk/v1/datasets/"
    EDITION = "2021"
    TIME_DELAY = 1  # seconds
    BASE_URL2 = "https://api.beta.ons.gov.uk/v1/"
    FILTER_ENDPOINT = f"{BASE_URL2}filters?submitted=true"
    SUBMIT_ENDPOINT_TEMPLATE = f"{BASE_URL2}filters/{{filter_id}}/submit"
    SAVE_DIRECTORY = "C:\Users"
    BASE_URL3 = "https://api.beta.ons.gov.uk/v1/filter-outputs/"
    CHUNK_SIZE = 128  # Chunk size for downloading files
