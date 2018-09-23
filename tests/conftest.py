import datetime
import os
import sys
import tempfile

import pytest

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from teachtime.teachtime import create_app, db
from teachtime.config import TestingConfig
from teachtime.models import User, Timetable, Event

pytest_plugins = ['helpers_namespace']

@pytest.fixture(scope='session')
def app(request):
    """Creates a testing instance of the application"""
    app = create_app(config=TestingConfig)

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app

@pytest.fixture(scope='session')
def client(app):
    client = app.test_client()
    return client

@pytest.fixture(scope='session')
def database(app, request):
    """Creates a testing database"""
    print(app.config)
    if os.path.exists(app.config.DATABASE):
        os.unlink(app.config.DATABASE)

    def teardown():
        db.drop_all()
        os.unlink(app.config.DATABASE)

    db.app = app
    db.create_all()

    request.addfinalizer(teardown)
    return db

@pytest.fixture(scope='function')
def session(database, request):
    """Creates a new database session for a test"""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = {
        'bind': connection,
        'binds': {}
    }

    session = db.create_scoped_session(options=options)
    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session

@pytest.fixture(scope='function')
def test_user(session):
    user = User(
        username='username', 
        email='username@example.com', 
        password='password'
    )

    session.add(user)
    session.commit()
    return user

@pytest.fixture(scope='function')
def test_timetable(session, test_user):
    timetable = Timetable(
        title='Test timetable',
        start_date=datetime.datetime.utcnow(),
        user_id=test_user.id
    )

    session.add(timetable)
    session.commit()
    return timetable

@pytest.fixture(scope='function')
def test_event(session, test_timetable):
    event = Event(
        title='Test event',
		start_time=datetime.time(), 
        end_time=datetime.time(),
        timetable_id=test_timetable.id
    )

    session.add(event)
    session.commit()
    return event

@pytest.helpers.register
def login(client, username, password):
    return client.post('/login', data={
        username: username,
        password: password
    }, follow_redirects=True)

@pytest.helpers.register
def logout(client):
    return client.get('/logout')