import pandas as pd
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Function to extract title and description from a URL with retries and timeouts
def extract_info_from_url(url):
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,  # Optional: backoff factor for exponential backoff
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    try:
        response = http.get(url, timeout=10)  # Adjust timeout as needed
        response.raise_for_status()  # Check for any HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title = soup.find('title').get_text() if soup.find('title') else ''

        # Extract description (if available)
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description.get('content') if meta_description else ''

        return title, description
    except requests.RequestException as e:
        print(f"Error processing URL {url}: {e}")
        return None, None

# Load the CSV files containing links
bbc_links_df = pd.read_csv('bbc_links.csv')
dawn_links_df = pd.read_csv('dawn_links.csv')

# Apply the function to extract info from each URL and create new columns
bbc_links_df[['Title', 'Description']] = bbc_links_df['Links'].apply(lambda x: pd.Series(extract_info_from_url(x)))
dawn_links_df[['Title', 'Description']] = dawn_links_df['Links'].apply(lambda x: pd.Series(extract_info_from_url(x)))

# Save the transformed data to new CSV files
bbc_links_df.to_csv('bbc_links_transformed.csv', index=False)
dawn_links_df.to_csv('dawn_links_transformed.csv', index=False)
