import datetime

import pytest

from teachtime.models import Event

def test_event_model(session, test_timetable):
	event = Event(
		title='Test event', 
		start_time=datetime.time(), 
        end_time=datetime.time(),
        timetable_id=test_timetable.id
	)

	session.add(event)
	session.commit()

	assert event.id > 0