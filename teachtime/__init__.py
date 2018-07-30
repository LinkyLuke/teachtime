from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from teachtime.config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfajksbhgvikhjeuradhgbfiejrwbf4347y84784e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from teachtime.routes import routes

app.register_blueprint(routes)