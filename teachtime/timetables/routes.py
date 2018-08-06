import datetime

from flask import Blueprint, render_template

from teachtime.timetables.format import TimetableFormatter

timetables = Blueprint('timetables', __name__)

@timetables.route('/timetable', defaults={'view': 'day', 'date': datetime.datetime.today()})
@timetables.route('/timetable/<view:view>/<date:date>')
def timetable(view, date):
	timetable = TimetableFormatter(view, date)

	template = {
		'day': '_day.html',
		'month': '_month.html',
		'year': '_year.html'
	}.get(view)

	return render_template(template, title='Timetable', timetable=timetable)