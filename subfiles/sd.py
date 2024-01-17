import requests
from bs4 import BeautifulSoup
import csv
import os
import re

def get_onion_page_info(onion_url):
    try:
        proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
        response = requests.get(onion_url, proxies=proxies)
        soup = BeautifulSoup(response.content, 'html.parser')
        page_title = soup.title.string if soup.title else "Title not found"
        hostname = response.url
        status_code = response.status_code

        telegram_ids = re.findall(r'@(\w+)', soup.get_text())
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text())
        contact_info = re.findall(r'\b(?:contact|info|support)[:\s]*([^\n\r]+)', soup.get_text())

        crypto_info = extract_crypto_info(soup)

        bitcoin_addresses = extract_bitcoin_addresses(soup)

        return hostname, page_title, status_code, ', '.join(telegram_ids) or "None", ', '.join(emails) or "None", ', '.join(contact_info) or "None", crypto_info, ', '.join(bitcoin_addresses) or "None"
    except requests.exceptions.RequestException as e:
        return onion_url, str(e), None, None, None, None, None, None

def extract_crypto_info(soup):
    crypto_info = "Crypto information not implemented"
    return crypto_info

def extract_bitcoin_addresses(soup):
    bitcoin_regex = re.compile(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b')
    bitcoin_addresses = bitcoin_regex.findall(soup.get_text())
    return bitcoin_addresses

def process_links_from_csv(input_file_path, output_file_path):
    with open(input_file_path, 'r', newline='', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        links = [row[0] for row in reader]

    output_filename = os.path.basename(input_file_path).replace('active_', 'onion_page_info_')

    with open(output_file_path + '/' + output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Hostname', 'Page Title', 'HTTP Status Code', 'Telegram IDs', 'Emails', 'Contact Info', 'Crypto Info', 'Bitcoin Addresses'])

        for link in links:
            hostname, title, status_code, telegram_ids, emails, contact_info, crypto_info, bitcoin_addresses = get_onion_page_info(link)
            writer.writerow([hostname, title, status_code, telegram_ids, emails, contact_info, crypto_info, bitcoin_addresses])

if __name__ == "__main__":
    input_folder = 'subfiles/active_links'
    output_folder = 'onion_page_info'

    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):
            input_file_path = os.path.join(input_folder, file_name)
            process_links_from_csv(input_file_path, output_folder)

    print(f"Data stored in {output_folder} folder.")
