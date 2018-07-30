from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from teachtime.config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfajksbhgvikhjeuradhgbfiejrwbf4347y84784e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from teachtime.routes import routes

app.register_blueprint(routes)