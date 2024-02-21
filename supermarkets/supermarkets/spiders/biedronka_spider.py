import scrapy


class BiedronkaSpider(scrapy.Spider):
    name = 'biedronka'
    start_urls = [
        'https://www.biedronka.pl/pl/sklepy/lista,city,gdansk,page,1',
        'https://www.biedronka.pl/pl/sklepy/lista,city,gdansk,page,2',
        'https://www.biedronka.pl/pl/sklepy/lista,city,gdansk,page,3',
        'https://www.biedronka.pl/pl/sklepy/lista,city,gdansk,page,4'
    ]

    def parse(self, response):
        for shop in response.css('li.shopListElement'):
            name = 'Biedronka'
            city = shop.css('h4 a::text').get()
            address_parts = shop.css('.shopAddress::text').getall()
            address = ' '.join(map(str.strip, address_parts))
            opening_hours = {}
            for item in shop.css('p b'):
                day = item.css('::text').get().strip(':')
                hours = item.xpath('following-sibling::span/text()').get()
                opening_hours[day] = hours.strip() if hours else 'Closed'
            availability = bool(shop.css('ul.shops-sizes li img.isSpecial'))
            yield {
                'name': name,
                'city': city,
                'address': address,
            }

        # Follow pagination links
        next_page = response.css('ul.pagination li.active + li a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
