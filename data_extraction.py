import requests
from bs4 import BeautifulSoup
import pandas as pd
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

# URLs of dawn.com and BBC.com
dawn_url = 'https://www.dawn.com/'
bbc_url = 'https://www.bbc.com/'

# Extract links from dawn.com and BBC.com
dawn_links = extract_links(dawn_url)
bbc_links = extract_links(bbc_url)

print("Dawn Links:", dawn_links)
print("BBC Links:", bbc_links)

df_dawn = pd.DataFrame({'Links': dawn_links})
df_bbc = pd.DataFrame({'Links': bbc_links})

# Save the DataFrames to CSV files
df_dawn.to_csv('dawn_links.csv', index=False)
df_bbc.to_csv('bbc_links.csv', index=False)

print("Links saved to CSV files.")
