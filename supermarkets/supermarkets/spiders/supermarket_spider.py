import scrapy
import re
import json
from pydantic import BaseModel, ValidationError, validator

class StartURLSFromFile:
    def __init__(self):
        with open("start_urls.txt", "r") as f:
            self.start_urls = f.read().split("\n")
class BusinessRecord(BaseModel):
    business: str
    opening_hours: str
    address: str
    city: str
    map_link: str

    @validator('business', 'address', 'city', 'map_link')
    def validate_fields(cls, value):
        if not value:
            raise ValueError('Field cannot be empty')
        return value

    @validator('opening_hours')
    def validate_opening_hours(cls, value):
        pattern = r'^\d{2}:\d{2}-\d{2}:\d{2}$'
        if not re.match(pattern, value):
            raise ValueError('Invalid opening hours format. Use HH:MM-HH:MM')
        return value

class SupermarketSpider(scrapy.Spider):
    name = 'okazjum'
    start_urls = StartURLSFromFile().start_urls

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

    def parse(self, response):
        for data in self.business_data:
            url_part = data['url_part']
            last_part_of_url = response.url.split('/')[2]
            last_part_of_url = last_part_of_url.split('.')[0]
            if last_part_of_url == url_part:
                yield from self.parse_business(response, business_data=data)

    def parse_business(self, response, business_data):
        print(response.css, "AA")
        for shop in response.css('div.stores.controller.show.shared table.striped.near-stores-table tbody tr'):
            opening_hours = shop.css('td:nth-child(1)::text').get().strip()
            full_address = shop.css('td:nth-child(2) a::text').get().strip()
            city, address = self.extract_city_and_address(full_address)
            map_link = shop.css('td:nth-child(3) a::attr(href)').get()

            yield {
                'business': business_data['name'],
                'opening_hours': opening_hours,
                'address': address,
                'city': city,
                'map_link': map_link
            }

    # Format z słownikami
    '''
        def parse_business(self, response, business_data):
            items = []
            for shop in response.css('div.stores.controller.show.shared table.striped.near-stores-table tbody tr'):
                opening_hours = shop.css('td:nth-child(1)::text').get().strip()
                full_address = shop.css('td:nth-child(2) a::text').get().strip()
                city, address = self.extract_city_and_address(full_address)
                map_link = shop.css('td:nth-child(3) a::attr(href)').get()

                item = {
                    'opening_hours': opening_hours,
                    'address': address,
                    'city': city,
                    'map_link': map_link
                }
                items.append(item)

            # Utwórz słownik, gdzie nazwa biznesu jest kluczem, a zestaw słowników jest wartością
            result = {business_data['name']: items}
            yield result
    '''

    def extract_city_and_address(self, full_address):
        match = re.match(r'([^,]+),(.+)', full_address)
        if match:
            city = match.group(1).strip()
            address = match.group(2).strip()
            return city, address
        else:
            return None, full_address
