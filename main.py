import requests
from bs4 import BeautifulSoup
import pandas as pd

from urllib.parse import urljoin

from format_helpers import *

BASE_URL = "http://books.toscrape.com/"


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print("Error: Cannot access page" + url)
        return None


# Scrapes information from a given book url
def get_book_data(url):
    soup = get_html(url)
    
    if soup is None:
        print("Error: Book not found")
        return None

    try:
        category = soup.find('li', class_='active').find_previous_sibling('li').a.text
    except AttributeError:
        category = None

    try:
        image_partial = soup.find('div', class_='thumbnail').find('img')['src']
        image = urljoin(BASE_URL, image_partial)
    except AttributeError:
        image = None

    try:
        title = soup.find('div', class_='product_main').h1.text
    except AttributeError:
        title = None

    try:
        rating = word_to_int(soup.find('p', class_='star-rating').get('class')[1])
    except AttributeError:
        rating = None

    try:
        description = soup.find('div', id='product_description').find_next_sibling('p').text
    except AttributeError:
        description = None

    try:
        upc = soup.find('th', text='UPC').find_next_sibling('td').text
    except AttributeError:
        upc = None

    try:
        product_type = soup.find('th', text='Product Type').find_next_sibling('td').text
    except AttributeError:
        product_type = None

    try: 
        price_excl_tax = price_to_decimal(soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text)
    except AttributeError:
        price_excl_tax = None

    try:
        price_incl_tax = price_to_decimal(soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text) 
    except AttributeError:
        price_incl_tax = None
    
    try:
        tax = price_to_decimal(soup.find('th', text='Tax').find_next_sibling('td').text) 
    except AttributeError:
        tax = None

    try:
        in_stock, num_available = availability_breakdown(soup.find('th', text='Availability').find_next_sibling('td').text)
    except AttributeError:
        in_stock = None
        num_available = None

    try:
        num_reviews = int(soup.find('th', text='Number of reviews').find_next_sibling('td').text) 
    except AttributeError:
        num_reviews = None
        
    return {
        'Title': title,
        'UPC': upc,
        'Product Type': product_type,
        'Category': category,
        'Image': image,
        'Rating': rating,
        'Num of Reviews': num_reviews,
        'Price excl Tax': price_excl_tax,
        'Price incl Tax': price_incl_tax,
        'Tax': tax,
        'In Stock': in_stock,
        'Num Available': num_available,
        'Description': description
    }


# Iterates through the webpage and scrapes all books
def scrape_all_books():
    print("Start Scraping")
    
    data_books = []
    page = 1

    while True:
        url = f"{BASE_URL}catalogue/page-{page}.html"
        print("Scraping " + url)
        
        soup = get_html(url)

        # Breaks loop when no more pages can be found
        if soup is None:
            print("No more pages found. End Scraping")
            break

        # Each book item is stored as an article with class="product_pod" in html
        books = soup.find_all('article', class_='product_pod')
        for book in books:
            book_url = BASE_URL + "catalogue/" + book.h3.a['href']
            book_data = get_book_data(book_url)
            data_books.append(book_data)
        
        page += 1

    return data_books


def save_to_csv(data, filename="books.csv"):
    print("Saving and exporting data")
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


save_to_csv(scrape_all_books())

