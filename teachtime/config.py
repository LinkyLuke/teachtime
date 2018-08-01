import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change_me'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    LOGIN_VIEW = 'login'
    LOGIN_MESSAGE_CATEGORY = 'info'