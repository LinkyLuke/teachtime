import calendar
import datetime

from teachtime.calendars.utils import ordinal_strftime, get_start_date_of_week_given_date_in_that_week

class CalendarFormatter:
    """Given a user's timetable, formats it at a certain date with a certain view"""

    @staticmethod
    def day_name(day):
        """Return a day name"""
        return f'{calendar.day_name[day]}'

    @staticmethod
    def month_name(month):
        """Return a month name"""
        return f'{calendar.month_name[month]}'

    view_days = {
        'day': 1,
        'week': 7,
        'month': 31,
        'year': 365
    }

    def __init__(self, view, date):
        self.cal = calendar.Calendar()

        self.view = view
        self.date = date

    @property
    def title(self):
        """Return the title of the calendar"""
        week_start_date = get_start_date_of_week_given_date_in_that_week(self.date)
        return {
            'day': ordinal_strftime('%A %#d%o %B %Y', self.date), # NOTE: Not portable
            'week': ordinal_strftime('W/C %A %#d%o %B %Y', week_start_date),
            'month': self.date.strftime('%B %Y'),
            'year': self.date.strftime('%Y')
        }.get(self.view)

    @property
    def next_date(self):
        """Return the next calendar view date"""
        return self.date + datetime.timedelta(days=CalendarFormatter.view_days[self.view])

    @property
    def previous_date(self):
        """Return the previous calendar view date"""
        return self.date + datetime.timedelta(days=-CalendarFormatter.view_days[self.view])

    # Month properties
    @property
    def weeks(self):
        return self.cal.monthdays2calendar(self.date.year, self.date.month)

    @property
    def weekdays(self):
        return self.cal.iterweekdays()

    # Year properties
    @property
    def months(self):
        return self.cal.yeardays2calendar(self.date.year)