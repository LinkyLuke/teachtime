from datetime import datetime

from flask_login import UserMixin

from teachtime.teachtime import db, login_manager

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable = False)
	timetables = db.relationship('Timetable', backref='user', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Timetable(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20), nullable=False)
	start_date = db.Column(db.Date, nullable=True, default=datetime.utcnow)
	events = db.relationship('Event', backref='timetable', lazy=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Timetable('{self.title}',  '{self.content}')"


class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20), nullable=False)
	description = db.Column(db.Text, nullable=False)
	offset_timedelta = db.Column(db.Interval, nullable=False)
	timetable_id = db.Column(db.Integer, db.ForeignKey('timetable.id'), nullable=False)
	
	def __repr__(self):
		return f"Event('{self.title}', '{self.time}', '{self.description}')"