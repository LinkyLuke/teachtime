from flask import Flask, render_template, url_for, flash, redirect
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
	return render_template('index.html', title='Home')

@app.route("/about")
def about():
	return render_template('about.html', title='Home')

@app.route("/login")
def login():
	form = LoginForm()

@app.route("/register")
def register():
	form = RegisterForm()

if __name__ == '__main__':
	app.run(debug=True)