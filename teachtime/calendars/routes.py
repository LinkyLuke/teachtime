import datetime

from flask import Blueprint, render_template

from teachtime.calendars.format import CalendarFormatter

calendars = Blueprint('calendars', __name__)

@calendars.route('/calendar', defaults={'view': 'day', 'date': datetime.datetime.today()})
@calendars.route('/calendar/<view:view>/<date:date>')
def calendar(view, date):
	calendar = CalendarFormatter(view, date)

	template = {
		'day': '_day.html',
		'week': '_week.html',
		'month': '_month.html',
		'year': '_year.html'
	}.get(view)

	return render_template(template, title='Calendar', calendar=calendar)