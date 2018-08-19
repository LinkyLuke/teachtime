import datetime

from flask import Blueprint, render_template

from teachtime.calendars.format import CalendarFormatter

calendars = Blueprint('calendars', __name__)

@calendars.route('/calendar', defaults={'view': 'day', 'date': datetime.datetime.today()})
@calendars.route('/calendar/<view:view>/<date:date>')
def calendar(view, date):
	calendar = CalendarFormatter(view, date)

	return render_template(f"calendars/{view}.html", title='Calendar', calendar=calendar)