These Python web scrapers use HTTPX and selectolax to obtain product data such as the name, sku, price, ratings and savings from https://www.rei.com. 

It first gets the single product information then loops through the page to get all product details. They uses a pagination loop to go through every page to get all the details. This can of course be modified to work with other sites, but will need new XPath or CSS selectors.

HTTPX Scraper 2 also writes and saves a CSV file of the data that was scraped.

This is a great web scraper technique for small amounts of data and sites that are less likely to block scraping. Scrapy is ideal for large scale web scraping and bypassing web scraper detectors.
