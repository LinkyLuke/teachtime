from flask import Blueprint, render_template, url_for, flash, redirect
from teachtime import app, db
from teachtime.forms import RegistrationForm, LoginForm

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
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == "admin@teachtime.com" and form.password.data == 'dansucks':
			flash('You have been logged in!', 'success')
			return redirect(url_for('routes.home'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@routes.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('routes.home'))
	return render_template('register.html', title='Register', form=form)


@routes.route("/timetable")
def timetable():
	return render_template('timetable.html', title="My Timetable")