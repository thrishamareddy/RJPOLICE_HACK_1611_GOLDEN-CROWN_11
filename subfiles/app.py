from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import os
import time

def create_extracted_folder():
    folder_name = 'extracted'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def save_links_to_csv(keyword, extracted_links):
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    extracted_folder = os.path.join(script_directory, 'extracted')

    if not os.path.exists(extracted_folder):
        os.makedirs(extracted_folder)

    filename = os.path.join(extracted_folder, f'{keyword}_links.csv')

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Extracted Links'])
        writer.writerows([[link] for link in extracted_links])

    print(f"Links extracted for '{keyword}' and saved to {filename}")
def main():
    tor_browser_path = '/home/deepak/Downloads/tor-browser/'
    geckodriver_path = '/usr/local/bin/geckodriver'
    firefox_binary_path = '/usr/bin/firefox115'

    options = Options()
    options.set_preference("profile", tor_browser_path + "/Browser/TorBrowser/Data/Browser/profile.default")
    options.binary_location = firefox_binary_path 
    service = webdriver.firefox.service.Service(geckodriver_path)
    service.start()
    driver = webdriver.Firefox(service=service, options=options)

    create_extracted_folder()

    with open('subfiles/keywords.csv', 'r') as keywords_file:
        keywords_reader = csv.reader(keywords_file)
        keywords = [row[0] for row in keywords_reader]

    for keyword in keywords:
        try:
            driver.get('https://ahmia.fi/') 

            search_input = driver.find_element("id", "id_q")
            search_input.clear()
            search_input.send_keys(keyword)
            search_input.send_keys(Keys.RETURN)

            time.sleep(10)  
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            all_links = soup.find_all('a', href=True)
            extracted_links = [link.get('href') for link in all_links]

            save_links_to_csv(keyword, extracted_links)

        except Exception as e:
            print(f"Error processing keyword '{keyword}': {e}")

    driver.quit()

if __name__ == "__main__":
    main()

