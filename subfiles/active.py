import requests
from bs4 import BeautifulSoup
import csv
import os

def is_link_active(onion_url):
    try:
        proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
        response = requests.get(onion_url, proxies=proxies, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def filter_active_links(input_file_path, output_file_path):
    with open(input_file_path, 'r', newline='', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        links = [row[0] for row in reader]

    active_links = [link for link in links if is_link_active(link)]


    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(script_directory, 'active_links')


    os.makedirs(output_folder, exist_ok=True)

    output_file_path = os.path.join(output_folder, f'active_{os.path.basename(input_file_path)}')

    with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file)
        writer.writerows([[link] for link in active_links])

if __name__ == "__main__":
    input_folder = 'subfiles/cleaned'

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):
            input_file_path = os.path.join(input_folder, file_name)
            filter_active_links(input_file_path, '')

    print(f"Active links filtered and saved in the 'active_links' folder in the same directory as 'cleaned'.")
