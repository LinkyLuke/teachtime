from flask import abort
from werkzeug.routing import BaseConverter, ValidationError

class ViewConverter(BaseConverter):
    """Extracts a view string from the path and validates it"""

    def to_python(self, value):
        views = ('day', 'week')

        if value in views:
            return value

        return abort(404)

    def to_url(self, value):
        return value