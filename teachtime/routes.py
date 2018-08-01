from flask import Blueprint, request, url_for, flash, redirect, render_template
from flask_login import current_user, login_required, login_user, logout_user

from .teachtime import bcrypt, db
from .forms import RegistrationForm, LoginForm
from .models import User, Timetable

routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route("/")
@routes.route("/home")
def home():
	return render_template('index.html', title='Home')

@routes.route("/about")
def about():
	return render_template('about.html', title='Home')

@routes.route("/login", methods=['GET', 'POST'])
def login():

	if current_user.is_authenticated:
		return redirect(url_for('routes.home'))

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()

		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('routes.home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')

	return render_template('login.html', title='Login', form=form)

@routes.route("/register", methods=['GET', 'POST'])
def register():

	if current_user.is_authenticated:
		return redirect(url_for('routes.home'))

	form = RegistrationForm()

	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()

		flash('Your account has been created. You are now able to log in!', 'success')
		return redirect(url_for('routes.home'))

	return render_template('register.html', title='Register', form=form)

@routes.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('routes.home'))

@routes.route("/account")
@login_required
def account():
	return render_template('account.html', title='Account')

@routes.route("/timetable")
def timetable():
	return render_template('timetable.html', title="My Timetable")