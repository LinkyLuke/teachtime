from datetime import datetime
from teachtime import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable = False)
	timetables = db.relationship('Timetable', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Timetable(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	#file = db.File?()
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Quiz('{self.title}', '{self.date}', '{self.time}', '{self.content}')"