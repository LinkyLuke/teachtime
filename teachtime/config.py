import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'change_me'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	LOGIN_VIEW = 'users.login'
	LOGIN_MESSAGE_CATEGORY = 'info'
	SECURITY_PASSWORD_SALT = 'my_precious_two'

	# Flask-Mail
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = '587'
	MAIL_USE_TLS = 'True'
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')