import csv
import requests
from bs4 import BeautifulSoup

def scrape_links(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            found_links = soup.find_all('a', href=True)
            return [link['href'] for link in found_links if link.get('href')]
        else:
            print(f"Failed to fetch URL: {url}")
            return []
    except requests.RequestException as e:
        print(f"Request Exception for URL {url}: {e}")
        return []

def main():
   
    existing_links = []
    with open('normal.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            existing_links.extend(row)

 
    new_links = []
    for url in existing_links:
        links = scrape_links(url)
        new_links.extend(links)

    
    with open('onion.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for link in new_links:
            writer.writerow([link])

if __name__ == "__main__":
    main()
