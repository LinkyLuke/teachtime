from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

from teachtime.config import Config
from teachtime.calendars.utils import ViewConverter, DateConverter

import os

bcrypt = Bcrypt()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate(db=db)

def create_app(config=Config):
	# Flask
	app = Flask(__name__)
	app.config.from_object(config)

	# SQLAlchemy
	from teachtime.models import User, Timetable
	db.init_app(app)
	with app.app_context():
		db.create_all()

	# Flask-Migrate
	migrate.init_app(app, db)

	# Flask-Bcrypt
	bcrypt.init_app(app)

	# Flask-Login	
	login_manager.init_app(app)
	login_manager.login_view = Config.LOGIN_VIEW
	login_manager.login_message_category = Config.LOGIN_MESSAGE_CATEGORY

	#Flask-Mail
	app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
	app.config['MAIL_PORT'] = '587'
	app.config['MAIL_USE_TLS'] = 'True'
	app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
	app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

	mail = Mail(app)

	# Custom converters
	app.url_map.converters['view'] = ViewConverter
	app.url_map.converters['date'] = DateConverter

	# TeachTime blueprints
	from teachtime.main.routes import main
	app.register_blueprint(main)
	from teachtime.users.routes import users
	app.register_blueprint(users)
	from teachtime.calendars.routes import calendars
	app.register_blueprint(calendars)
	from teachtime.timetables.routes import timetables
	app.register_blueprint(timetables)
	from teachtime.errors.handlers import errors
	app.register_blueprint(errors)

	return app



if __name__ == '__main__':
	app = create_app()
	app.run()