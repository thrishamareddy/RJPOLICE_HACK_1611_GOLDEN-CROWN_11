import os
import csv
import re

def clean_links(links):
    cleaned_links = []
    for link in links:
        match = re.search(r'search_term=[^&]+&redirect_url=(.+)', link)
        if match:
            cleaned_links.append(match.group(1))
    return cleaned_links[:5]

def clean_csv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as extracted_file:
        reader = csv.reader(extracted_file)
        header = next(reader)  
        links = [row[0] for row in reader]

    cleaned_links = clean_links(links)

    
    cleaned_folder = os.path.join('subfiles', 'cleaned')

    if not os.path.exists(cleaned_folder):
        os.makedirs(cleaned_folder)

    cleaned_filename = os.path.join(cleaned_folder, f'{os.path.splitext(os.path.basename(file_path))[0]}_cleaned.csv')

    with open(cleaned_filename, 'w', newline='', encoding='utf-8') as cleaned_csvfile:
        cleaned_writer = csv.writer(cleaned_csvfile)
        cleaned_writer.writerows([[link] for link in cleaned_links])

    print(f"Cleaned links from '{file_path}' saved to {cleaned_filename}")

def main():
    extracted_folder = 'subfiles/extracted'

    for filename in os.listdir(extracted_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(extracted_folder, filename)
            clean_csv(file_path)

if __name__ == "__main__":
    main()
