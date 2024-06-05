import httpx  
from selectolax.parser import HTMLParser
from dataclasses import dataclass 
from urllib.parse import urljoin 
from rich import print
import pandas as pd 

#To store data of product name, SKU, price and rating. All strings for now
@dataclass
class Product:
    name: str
    sku: str
    price: str
    rating: str

#HTML and next page function stored as HTMLParser and dict to get attributes of the next page
@dataclass
class Response:
    body_html: HTMLParser
    next_page: dict

#Takes the client and URL
def get_page(client, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
        }
    resp = client.get(url, headers = headers)
    html = HTMLParser(resp.text)
    if html.css("a[data-id=pagination-test-link-next]"):
        next_page = html.css_first("a[data-id=pagination-test-link-next]").attributes #attribute of dict gives us href of next page
    else:
        next_page = {"href" : False} #if no next page, breaks out of the loop
    return Response(body_html = html, next_page = next_page)

#Extract text using try block in case of IndexError for missing text
def extract_text(html, selector, index):
    try:
        return html.css(selector)[index].text(strip = True)
    except IndexError:
        return "none"
    
#Returns all details of each product    
def parse_detail(html):
    product_list = []
    new_product = Product(
        name = extract_text(html, "h1#product-page-title", 0),
        sku = extract_text(html, "span.item-number", 0),
        price = extract_text(html, "span.price-value", 0),
        rating = extract_text(html, "span.cdr-rating__number_15-0-0", 0),
    )
    product_list.append(new_product)
    print(product_list)
    return product_list
    

#Loop function for detailed product function
def detail_page_loop(client, page):
    base_url = "https://www.rei.com"
    product_links = parse_links(page.body_html)
    for link in product_links:
        detail_page = get_page(client, urljoin(base_url, link))
        parse_detail(detail_page.body_html)

#Used to grab all the product links within the page
def parse_links(html):
    links = html.css("div#search-results > ul li > a")
    return {link.attrs["href"] for link in links} #Returns as set to remove duplicates compared to lists

#Loop through pages
def pagination_loop(client):
    url = "https://www.rei.com/c/backpacks"
    while True:
        page = get_page(client, url)
        detail_page_loop(client, page)
        if page.next_page["href"] is False:
            client.close()
            break
        else:
            url = urljoin(url, page.next_page["href"])
            print(url)

def save_csv(product_list):
    pass

def main():

    client = httpx.Client(timeout = 10.0)
    pagination_loop(client)
    
#Call the main function
if __name__ == '__main__':
    main()
