import re
from pydantic import ValidationError, validator

# Validator functions
def validate_fields(value):
    if not value:
        raise ValueError('Field cannot be empty')
    return value

def validate_opening_hours(value):
    pattern = r'^\d{2}:\d{2}-\d{2}:\d{2}$'
    if not re.match(pattern, value):
        raise ValueError('Invalid opening hours format. Use HH:MM-HH:MM')
    return value