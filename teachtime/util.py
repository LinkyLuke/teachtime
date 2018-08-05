from datetime import datetime

from flask import abort
from werkzeug.routing import BaseConverter, ValidationError

def ordinal_strftime(format, date):
    return date.strftime(format.replace('%o', {1: 'st', 2: 'nd', 3: 'rd'}.get(date.day if (date.day < 20) else (date.day % 10), 'th')))

class ViewConverter(BaseConverter):
    """Extracts a view string from the path and validates it""" # Questionable whether this belongs as a converter...
    
    def to_python(self, value):
        views = ('day', 'month', 'year')

        if value in views:
            return value

        return abort(404)

    def to_url(self, value):
        return value

class DateConverter(BaseConverter):
    """Extracts a ISO8601 date from the path and validates it"""

    def to_python(self, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError()

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')