from datetime import datetime

from flask_login import UserMixin

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from teachtime.teachtime import db, login_manager

from teachtime.config import Config

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

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(Config.SECRET_KEY, expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(Config.SECRET_KEY)
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return user.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Timetable(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20), nullable=False)
	start_date = db.Column(db.Date, nullable=True, default=datetime.utcnow)
	events = db.relationship('Event', backref='timetable', lazy=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Timetable('{self.title}')"


class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20), nullable=False)
	start_time = db.Column(db.Time, nullable=False)
	end_time = db.Column(db.Time, nullable=False)
	description = db.Column(db.Text, nullable=True)
	timetable_id = db.Column(db.Integer, db.ForeignKey('timetable.id'), nullable=False)
	
	def __repr__(self):
		return f"Event('{self.title}', '{self.start_time}-{self.end_time}', '{self.description}')"