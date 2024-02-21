import scrapy
import re

class ZabkaSpider(scrapy.Spider):
    name = 'stokrotkamarket'
    start_urls = [
        'https://stokrotka-market.okazjum.pl/sklepy/gdansk/',
    ]

    def parse(self, response):
        for shop in response.css('div.stores.controller.show.shared table.striped.near-stores-table tbody tr'):
            opening_hours = shop.css('td:nth-child(1)::text').get().strip()
            full_address = shop.css('td:nth-child(2) a::text').get().strip()
            city, address = self.extract_city_and_address(full_address)
            map_link = shop.css('td:nth-child(3) a::attr(href)').get()

            yield {
                'name': 'Stokrotka Market',
                'opening_hours': opening_hours,
                'address': address,
                'city': city,
                'map_link': map_link
            }

    def extract_city_and_address(self, full_address):
        match = re.match(r'([^,]+),(.+)', full_address)
        if match:
            city = match.group(1).strip()
            address = match.group(2).strip()
            return city, address
        else:
            return None, full_address
