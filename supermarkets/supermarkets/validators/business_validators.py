import re
from pydantic import ValidationError, validator

def validate_fields(value):
    if not value:
        raise ValueError('Field cannot be empty')
    return value

def validate_opening_hours(value):
    pattern = r'^\d{2}:\d{2}-\d{2}:\d{2}$'
    if not re.match(pattern, value):
        raise ValueError('Invalid opening hours format. Use HH:MM-HH:MM')
    return value

def validate_address(address):
    pattern = r'^[\w\s\d.,\-/]+$'
    if not re.match(pattern, address):
        raise ValueError('Invalid address format')
    return address

def validate_city(city):
    pattern = r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s]+$'
    if not re.match(pattern, city):
        raise ValueError('Invalid city format')
    return city

def validate_map_link(map_link):
    pattern = r'^\/[a-zA-Z0-9.,_\-\/]+$'
    if not re.match(pattern, map_link):
        raise ValueError('Invalid map link format')
    return map_link