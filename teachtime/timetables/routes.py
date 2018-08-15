from flask import Blueprint, render_template

timetables = Blueprint('timetables', __name__)

@timetables.route('/timetable')
def timetable():
	return render_template('new_timetable.html', title='Timetable')