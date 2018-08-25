from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_required

from teachtime.timetables.forms import (
    CreateTimetableForm,
    EditTimetableForm,
    CreateEventForm,
    EditEventForm,
)
from teachtime.models import Timetable, Event
from teachtime.teachtime import db

timetables = Blueprint('timetables', __name__)

@timetables.route('/timetables/dropdown')
@login_required
def timetable_dropdown():
    timetables = Timetable.query.filter_by(user_id=current_user.id)
    return render_template('timetables/_dropdown.html', timetables=timetables)

# TODO: These routes should filter by user
@timetables.route('/timetables')
@login_required
def list_timetables():
    """GET /timetables
    
    Show all timetables
    """
    timetables = Timetable.query.filter_by(user_id=current_user.id)
    return render_template('timetables/index.html', title="Timetables", timetables=timetables)

@timetables.route('/timetables/create')
@login_required
def create_timetable():
    """GET /timetables/create
    
    Show the form to create a new timetable
    """
    form = CreateTimetableForm()
    return render_template('timetables/create.html', title="Create a timetable", form=form)

@timetables.route('/timetables', methods=['POST'])
@login_required
def store_timetable():
    """POST /timetables

    Create a new timetable in the database
    """
    form = CreateTimetableForm()

    if form.validate_on_submit():
        timetable = Timetable(
            title=form.title.data,
            user_id=current_user.id
        )

        db.session.add(timetable)
        db.session.commit()

        return redirect(url_for('timetables.show_timetable', timetable_id=timetable.id))

@timetables.route('/timetables/<int:timetable_id>', methods=['GET'])
@login_required
def show_timetable(timetable_id):
    """GET /timetables/<timetable_id>

    Show a timetable from the database
    """
    timetable = Timetable.query.get_or_404(timetable_id)
    return render_template('timetables/show.html', title=f"Timetable {timetable.title}", timetable=timetable)

@timetables.route('/timetables/<int:timetable_id>/edit', methods=['GET'])
@login_required
def edit_timetable(timetable_id):
    """GET /timetables/<timetable_id>/edit

    Show the form for editing a timetable
    """
    timetable = Timetable.query.get_or_404(timetable_id)
    form = EditTimetableForm()
    return render_template('timetables/edit.html', title=f"Timetable {timetable.title}", timetable=timetable, form=form)

@timetables.route('/timetables/<int:timetable_id>', methods=['PUT'])
@login_required
def update_timetable(timetable_id):
    """PUT /timetables/<timetable_id>

    Updates the timetable in the database
    """
    timetable = Timetable.query.get_or_404(timetable_id)
    form = EditTimetableForm()

    if form.validate_on_submit():
        timetable.title = form.title.data
        timetable.start_date = form.start_date.data

        db.session.commit()

    return redirect(url_for('timetables.show_timetable', timetable_id=timetable.id))

# TODO: Below routes need validation to stop users from creating
# events on timetables that don't exist but I don't know how to
# do it and I can't look it up because I don't have internet SEND HELP
@timetables.route('/timetables/<int:timetable_id>/events/create')
@login_required
def create_event(timetable_id):
    """GET /timetables/<timetable_id>/events/create

    Show the form to create a new event
    """
    form = CreateEventForm()
    return render_template('events/create.html', title="Create an event", timetable_id=timetable_id, form=form)

@timetables.route('/timetables/<int:timetable_id>/events', methods=['POST'])
@login_required
def store_event(timetable_id):
    """POST /timetables/<timetable_id>/events

    Create a new event in the database
    """
    timetable = Timetable.query.get_or_404(timetable_id)
    form = CreateEventForm()

    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            offset=form.time.data,
            timetable = timetable
        )

        db.session.add(event)
        db.session.commit()

    return redirect(url_for('timetables.show_timetable', timetable_id=timetable.id))

# NOTE: This route is used when a user is viewing an event in the context of 
# a timetable, not a calendar
@timetables.route('/timetables/<int:timetable_id>/events/<int:event_id>')
@login_required
def show_event(event_id):
    """GET /timetables/<timetable_id/events/<event_id>

    Show an event from the database
    """
    event = Event.query.get(event_id)
    return render_template('events/show.html', title=f"Event {event.title}", event=event)

@timetables.route('/timetables/<int:timetable_id>/events/<int:event_id>/edit')
@login_required
def edit_event(event_id):
    """GET /timetables/<timetable_id>/events/<event_id>/edit

    Show the form for editing an event
    """
    event = Event.query.get_or_404(event_id)
    form = EditEventForm()
    return render_template('events/edit.html', title=f"Event {event.title}", event=event, form=form)

@timetables.route('/timetables/<int:timetable_id>/events/')
@login_required
def update_event(event_id):
    """PUT /timetables/<timetable_id>/events/<event_id>

    Updates the event in the database
    """
    event = Event.query.get_or_404(event_id)
    form = EditEventForm()

    if form.validate_on_submit():
        event.title = form.title.data
        event.start_date = form.start_date.data

        db.session.commit()

    return redirect(url_for('timetables.show_event', event_id=event.id))