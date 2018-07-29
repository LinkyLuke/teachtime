from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'dansucksomgdansucksseriouslydansucks'

@app.route("/")
@app.route("/home")
def home():
	return render_template('index.html', title='Home')

@app.route("/about")
def about():
	return render_template('about.html', title='Home')

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == "admin@teachtime.com" and form.password.data == 'dansucks':
			flash('You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)


@app.route("/timetable")
def timetable():
	return render_template('timetable.html', title="My Timetable")

if __name__ == '__main__':
	app.run(debug=True)

