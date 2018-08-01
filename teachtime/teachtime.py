from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from teachtime.config import Config

bcrypt = Bcrypt()
login_manager = LoginManager()
db = SQLAlchemy()

def create_app(config=Config):
	# Flask
	app = Flask(__name__)
	app.config.from_object(config)

	# SQLAlchemy
	from .models import User, Timetable
	db.init_app(app)
	with app.app_context():
		db.create_all()

	# Flask-Bcrypt
	bcrypt.init_app(app)

	# Flask-Login	
	login_manager.init_app(app)
	login_manager.login_view = Config.LOGIN_VIEW
	login_manager.login_message_category = Config.LOGIN_MESSAGE_CATEGORY

	# TeachTime blueprints
	from .routes import routes
	app.register_blueprint(routes)

	return app

if __name__ == '__main__':
	app = create_app()
	app.run()