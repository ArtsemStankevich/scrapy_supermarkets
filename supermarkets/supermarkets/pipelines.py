# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .validators.business_validators import validate_fields, validate_opening_hours, validate_address, validate_city, validate_map_link

class SupermarketsPipeline:
    def process_item(self, item, spider):
        return item

class ValidationPipeline:
    def process_item(self, item, spider):
        try:
            item['business'] = validate_fields(item['business'])
            item['address'] = validate_address(item['address'])
            item['city'] = validate_city(item['city'])
            item['map_link'] = validate_map_link(item['map_link'])
            item['opening_hours'] = validate_opening_hours(item['opening_hours'])
        except ValueError as e:
            print(f"Validation error: {e}")
            raise DropItem(f"Validation error: {e}")
        return item