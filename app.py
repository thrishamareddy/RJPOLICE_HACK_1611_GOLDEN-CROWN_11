from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import time

def clean_links(links):
    cleaned_links = []
    for link in links:
        if 'search_term=drugs&redirect_url=' in link:
            cleaned_links.append(link.split('=')[-1])
    return cleaned_links

tor_browser_path = '/home/deepak/Downloads/tor-browser/'
geckodriver_path = '/usr/local/bin/geckodriver'
firefox_binary_path = '/usr/bin/firefox115'

options = Options()
options.set_preference("profile", tor_browser_path + "/Browser/TorBrowser/Data/Browser/profile.default")
options.binary_location = firefox_binary_path 
service = webdriver.firefox.service.Service(geckodriver_path)
service.start()
driver = webdriver.Firefox(service=service, options=options)

keywords = ['drugs', 'guns','murder']  

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

        filename = f'extracted_links_{keyword}.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Extracted Links'])
            writer.writerows([[link] for link in extracted_links])
            
           
            cleaned_links = clean_links(extracted_links)
            cleaned_filename = f'cleaned_links_{keyword}.csv'
            with open(cleaned_filename, 'w', newline='', encoding='utf-8') as cleaned_csvfile:
                cleaned_writer = csv.writer(cleaned_csvfile)
                cleaned_writer.writerow(['Cleaned Links'])
                cleaned_writer.writerows([[link] for link in cleaned_links])

        print(f"Links extracted for '{keyword}' and saved to {filename}")
        print(f"Cleaned links for '{keyword}' saved to {cleaned_filename}")

    except Exception as e:
        print(e)

driver.quit()
