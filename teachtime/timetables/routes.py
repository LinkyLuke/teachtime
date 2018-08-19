from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user

from teachtime.timetables.forms import CreateTimetableForm, EditTimetableForm
from teachtime.models import Timetable
from teachtime.teachtime import db

timetables = Blueprint('timetables', __name__)

@timetables.route('/timetable')
def index():
    timetables = Timetable.query.all()
    return render_template('timetables/index.html', title="Timetables", timetables=timetables)

@timetables.route('/timetable/create')
def create():
    form = CreateTimetableForm()
    return render_template('timetables/create.html', title="Create a timetable", form=form)

@timetables.route('/timetable', methods=['POST'])
def store():
    form = CreateTimetableForm()

    if form.validate_on_submit():
        timetable = Timetable(
            title=form.title.data,
            user_id=current_user.id
        )

        db.session.add(timetable)
        db.session.commit()

        return redirect(url_for('timetables.index'))

@timetables.route('/timetable/<int:id>')
def show(id):
    timetable = Timetable.query.get(id)
    return render_template('timetables/show.html', title=f"Timetable {timetable.title}", timetable=timetable)

@timetables.route('/timetable/<int:id>')
def edit(id):
    timetable = Timetable.query.get_or_404(id)
    form = EditTimetableForm()

    if form.validate_on_submit():
        timetable.title = form.title.data
        timetable.start_date = form.start_date.data

        db.session.commit()

    return render_template('timetables/edit.html', title=f"Timetable {timetable.title}", timetable=timetable, form=form)

@timetables.route('/timetable/<int:id>/events/create')
def create_event(id):
    pass