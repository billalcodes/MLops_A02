from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Function to extract links from a webpage
def extract_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    return links

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

# URLs of dawn.com and BBC.com
dawn_url = 'https://www.dawn.com/'
bbc_url = 'https://www.bbc.com/'

# DAG definition
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_extraction_transformation',
    default_args=default_args,
    description='A DAG to automate data extraction and transformation',
    schedule_interval='@daily',  # Run daily, adjust as needed
)

# Task to extract data and save links to CSV files
def extract_data_and_save():
    dawn_links = extract_links(dawn_url)
    bbc_links = extract_links(bbc_url)
    df_dawn = pd.DataFrame({'Links': dawn_links})
    df_bbc = pd.DataFrame({'Links': bbc_links})
    df_dawn.to_csv('dawn_links.csv', index=False)
    df_bbc.to_csv('bbc_links.csv', index=False)

extract_task = PythonOperator(
    task_id='extract_data_task',
    python_callable=extract_data_and_save,
    dag=dag,
)

# Task to transform data and save transformed data to CSV files
def transform_data_and_save():
    bbc_links_df = pd.read_csv('bbc_links.csv')
    dawn_links_df = pd.read_csv('dawn_links.csv')
    bbc_links_df[['Title', 'Description']] = bbc_links_df['Links'].apply(lambda x: pd.Series(extract_info_from_url(x)))
    dawn_links_df[['Title', 'Description']] = dawn_links_df['Links'].apply(lambda x: pd.Series(extract_info_from_url(x)))
    bbc_links_df.to_csv('bbc_links_transformed.csv', index=False)
    dawn_links_df.to_csv('dawn_links_transformed.csv', index=False)

transform_task = PythonOperator(
    task_id='transform_data_task',
    python_callable=transform_data_and_save,
    dag=dag,
)

# Define task dependencies
extract_task >> transform_task
