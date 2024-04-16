'''
import csv

# Read the CSV file and modify the 'Price' column
with open('dataset.csv', mode='r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

for row in data:
    # Convert 'Price' column to integer without commas
    row['Price'] = int(row['Price'].replace(',', ''))

# Write the modified data back to the CSV file
with open('dataset.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(data)
'''
import re
from bs4 import BeautifulSoup
import requests
import csv

desired_fields = ['Price', 'Size (in meters)', 'Room', 'Baths', 'Type']

def getListings():
    base_url = 'https://aqarmap.com.eg/en/for-sale/property-type/cairo/new-cairo/madinaty/?default=1&page={}'
    all_data = []
    for page_number in range(0, 5):
        url = base_url.format(page_number)
        content = requests.get(url).text
        soup = BeautifulSoup(content, 'lxml')
        listings_cards = soup.find_all('div', class_='search-listing-card__wrapper')

        links = ["https://aqarmap.com.eg" + listing.a['href'] for listing in listings_cards]
        all_data.extend(getDetails(links))
    with open('dataset.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=desired_fields)
        writer.writeheader()

        for data in all_data:
            # Convert Price to integer and clean Size
            data['Price'] = int(data['Price'].replace(',', ''))
            data['Size (in meters)'] = int(re.search(r'\d+', data['Size (in meters)']).group())

            writer.writerow(data)

def getDetails(links):
    with requests.Session() as session:
        details_list = []
        for link in links:
            content = session.get(link).text
            soup = BeautifulSoup(content, 'lxml')

            price = soup.find('div', class_='listing-details-page__title-section__price').span.text.strip()
            property_type = soup.find('div', class_='listing-details-page__title-section__sub').span.text.strip()
            details = soup.find_all('li', class_='list-group-item d-flex')

            data = {
                'Type': property_type,
                'Price': price
            }
            for detail in details:
                name = detail.find('span', class_='col-md-3 col-5').text.strip()
                info = detail.find('span', class_='count badge badge-default').text
                if name in desired_fields:
                    if name == 'Price':
                        info = info.replace(',', '')
                    data[name] = info
            details_list.append(data)
    return details_list
getListings()
