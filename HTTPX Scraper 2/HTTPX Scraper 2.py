import httpx
from selectolax.parser import HTMLParser
import time
import csv


def get_html(baseurl, page):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"}
    resp = httpx.get(baseurl + str(page), headers= headers, follow_redirects = True)
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}. Page Limit Exceeded")
        return False
    html = HTMLParser(resp.text)
    return html


def extract_text(html, sel):
    try:
        return html.css_first(sel).text()
    except AttributeError:
        return None


def parse_page(html):
    products = html.css("li.VcGDfKKy_dvNbxUqm29K") #list items for all products
    for product in products:
        item = {
            "name" : extract_text(product, ".Xpx0MUGhB7jSm5UvK2EY"),
            "price" : extract_text(product, "span[data-ui = sale-price]"),
            "savings" : extract_text(product, "div[data-ui = savings-percent-variant2]"),
        }
        yield item


def save_csv(product_list):
    keys = product_list[0].keys()
    with open('ProductList.csv', 'w', newline = '') as myfile:
        dict_writer = csv.DictWriter(myfile, keys)
        dict_writer.writeheader()
        dict_writer.writerows(product_list)
    

def main():
    product_list = []
    baseurl = "https://www.rei.com/c/camping-and-hiking/f/scd-deals?page="
    for x in range(1,3):
        print(f"Gathering data from page: {x}")
        html = get_html(baseurl, x)
        if html is False:
            break
        data = parse_page(html)
        for item in data:
            print(item)
            product_list.append(item)
        time.sleep(1)
        save_csv(product_list)


if __name__ == "__main__":
    main()
    