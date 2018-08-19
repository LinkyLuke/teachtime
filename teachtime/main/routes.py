from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def index():
	return render_template('main/index.html', title='Home')

@main.route("/about")
def about():
	return render_template('main/about.html', title='About')