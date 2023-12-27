import requests as rq
from bs4 import BeautifulSoup
import csv

# Function to clean the links
def clean_links(links):
    cleaned_links = [link.split('=')[-1] for link in links if 'search_term=drugs&redirect_url=' in link]
    return cleaned_links

# Scraping links from the website
URL = "https://ahmia.fi/search/?q=drugs"
TOR_PROXY = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}

res = rq.get(url=URL, proxies=TOR_PROXY)

if res.status_code == 200:
    html = res.content.decode()
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all anchor tags
    all_links = soup.find_all('a', href=True)
    
    # Extract href attribute (links) from anchor tags
    extracted_links = [link.get('href') for link in all_links]

    # Clean the extracted links
    cleaned_links = clean_links(extracted_links)

    # Save cleaned links to a CSV file
    with open('cleaned_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Cleaned Links'])
        for link in cleaned_links:
            writer.writerow([link])
    
    print("Links extracted, cleaned, and saved to cleaned_links.csv")
else:
    print("Something went wrong. Status code:", res.status_code)
