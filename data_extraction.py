import requests
from bs4 import BeautifulSoup
import pandas as pd
def extract_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    return links

dawn_url = 'https://www.dawn.com/'
bbc_url = 'https://www.bbc.com/'

dawn_links = extract_links(dawn_url)
bbc_links = extract_links(bbc_url)

print("Dawn Links:", dawn_links)
print("BBC Links:", bbc_links)

df_dawn = pd.DataFrame({'Links': dawn_links})
df_bbc = pd.DataFrame({'Links': bbc_links})

df_dawn.to_csv('dawn_links.csv', index=False)
df_bbc.to_csv('bbc_links.csv', index=False)

print("Links saved to CSV files.")
