import scrapy
import re
import json

business_data = [
    {'url_part': 'lidl', 'name': 'Lidl'},
    {'url_part': 'polomarket', 'name': 'polomarket'},
    {'url_part': 'biedronka', 'name': 'Biedronka'},
    {'url_part': 'intermarche-super', 'name': 'Intermarche Super'},
    {'url_part': 'castorama', 'name': 'Castorama'},
    {'url_part': 'carrefour', 'name': 'Carrefour'},
    {'url_part': 'pepco', 'name': 'Pepco'},
    {'url_part': 'dino', 'name': 'Dino'},
    {'url_part': 'zabka', 'name': 'Żabka'},
    {'url_part': 'kaufland', 'name': 'Kaufland'},
    {'url_part': 'topmarket', 'name': 'Top Market'},
    {'url_part': 'carrefour-market', 'name': 'Carrefour Market'},
    {'url_part': 'stokrotka', 'name': 'Stokrotka'},
    {'url_part': 'eurospar', 'name': 'Eurospar'},
    {'url_part': 'stokrotka-express', 'name': 'Stokrotka Express'},
    {'url_part': 'lewiatan', 'name': 'Lewiatan'},
    {'url_part': 'spar', 'name': 'Spar'},
    {'url_part': 'stokrotka-market', 'name': 'Stokrotka Market'},
    {'url_part': 'auchan-supermarket', 'name': 'Auchan Supermarket'},
    {'url_part': 'carrefour-express', 'name': 'Carrefour Express'},
    {'url_part': 'auchan', 'name': 'Auchan'},
    {'url_part': 'netto', 'name': 'Netto'},
    {'url_part': 'aldi', 'name': 'Aldi'}
]

class StartURLSFromFile:
    def __init__(self):
        with open("start_urls.txt", "r") as f:
            base_urls = f.read().split("\n")
        self.start_urls = self.generate_urls(base_urls)

    def generate_urls(self, base_urls):
        generated_urls = []
        for business in business_data:
            generated_urls.append(f"https://{business['url_part']}.okazjum.pl/sklepy/gdansk/")
        return generated_urls

class SupermarketSpider(scrapy.Spider):
    name = 'okazjum'

    start_urls = StartURLSFromFile().start_urls
    
    def parse(self, response):
        for data in business_data:
            url_part = data['url_part']
            last_part_of_url = response.url.split('/')[2]
            last_part_of_url = last_part_of_url.split('.')[0]
            if last_part_of_url == url_part:
                yield from self.parse_business(response, business_data=data)
    def parse_business(self, response, business_data):
        for shop in response.css('div.stores.controller.show.shared table.striped.near-stores-table tbody tr'):
            opening_hours = shop.css('td:nth-child(1)::text').get().strip()
            full_address = shop.css('td:nth-child(2) a::text').get().strip()
            city, address = self.extract_city_and_address(full_address)
            map_link = shop.css('td:nth-child(3) a::attr(href)').get()

            yield {
                'business':business_data['name'],
                'opening_hours':opening_hours,
                'address':address,
                'city':city,
                'map_link':map_link,
                'url': response.url
            }


    def extract_city_and_address(self, full_address):
        match = re.match(r'([^,]+),(.+)', full_address)
        if match:
            city = match.group(1).strip()
            address = match.group(2).strip()
            return city, address
        else:
            return None, full_address
