import os

class Config:
	DEBUG = False
	TESTING = False

	SECRET_KEY = os.environ.get('SECRET_KEY') or 'change_me'

	# TeachTime
	DATABASE = 'site.db'

	# Flask-SQLAlchemy
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE

	# Flask-Login
	LOGIN_VIEW = 'users.login'
	LOGIN_MESSAGE_CATEGORY = 'info'

	# Flask-Mail
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = '587'
	MAIL_USE_TLS = 'True'
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

class ProductionConfig(Config):
	pass

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True
	DATABASE = 'test.db'