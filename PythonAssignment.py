import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_product_listings(url, num_pages):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    product_list = []
    
    for page in range(1, num_pages + 1):
        print(f"Scraping page {page}")
        params = {'k': 'bags', 'crid': '2M096C61O4MLT', 'qid': '1653308124', 'sprefix': 'ba', 'ref': f'sr_pg_{page}'}
        response = requests.get(url, headers=headers, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for result in results:
            product_data = {}
            
            product_link = result.find('a', {'class': 'a-link-normal s-no-outline'})
            if product_link:
                product_data['URL'] = urljoin(url, product_link['href'])
            
            product_name = result.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
            if product_name:
                product_data['Name'] = product_name.text
            
            product_price = result.find('span', {'class': 'a-offscreen'})
            if product_price:
                product_data['Price'] = product_price.text
            
            rating = result.find('span', {'class': 'a-icon-alt'})
            if rating:
                product_data['Rating'] = rating.text
            
            num_reviews = result.find('span', {'class': 'a-size-base'})
            if num_reviews:
                product_data['Reviews'] = num_reviews.text
            
            product_list.append(product_data)
    
    return product_list

def get_product_details(product_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    for product in product_list:
        product_url = product['URL']
        print(f"Scraping product: {product_url}")
        
        response = requests.get(product_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        description = soup.find('div', {'id': 'productDescription'})
        if description:
            product['Description'] = description.text.strip()
        
        asin = soup.find('th', text='ASIN')
        if asin:
            product['ASIN'] = asin.find_next('td').text.strip()
        
        product_desc = soup.find('h2', text='Product description')
        if product_desc:
            product['Product Description'] = product_desc.find_next('div').text.strip()
        
        manufacturer = soup.find('th', text='Manufacturer')
        if manufacturer:
            product['Manufacturer'] = manufacturer.find_next('td').text.strip()

def export_to_csv(data, filename):
    keys = data[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

url = 'https://www.amazon.in/s'
num_pages = 20
product_listings = get_product_listings(url, num_pages)

get_product_details(product_listings)

filename = 'amazon_products.csv'
export_to_csv(product_listings, filename)
print(f"Data exported to {filename} successfully.")

