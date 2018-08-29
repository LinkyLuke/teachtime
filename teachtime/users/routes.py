import os
import secrets

from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from PIL import Image

from teachtime.teachtime import bcrypt, db, mail
from teachtime.models import User
from teachtime.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm

users = Blueprint('users', __name__)

@users.route("/login", methods=['GET', 'POST'])
def login():

	if current_user.is_authenticated:
		return redirect(url_for('main.index'))

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()

		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.index'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')

	return render_template('users/login.html', title='Login', form=form)

@users.route("/register", methods=['GET', 'POST'])
def register():

	if current_user.is_authenticated:
		return redirect(url_for('main.index'))

	form = RegistrationForm()

	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()

		flash('Your account has been created. You are now able to log in!', 'success')
		return redirect(url_for('main.index'))

	return render_template('users/register.html', title='Register', form=form)

@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.index'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static\\profile_pics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('users/account.html', title='Account', image_file=image_file, form=form)


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', 
					sender='noreply@teachtime.com', recipients=[user.email])
	msg.body = f'''To reset your password visit the following link:
{url_for('users.reset_token', token=token, _external = True)}
If you did not make this request, simply ignore this email. No changes will be made.
'''
	mail.send(msg)

	
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password', 'info')
		return redirect(url_for('users.login'))
	return render_template('users/reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Password has been successfully reset!', 'success')
		return redirect(url_for('main.index'))
	return render_template('users/reset_token.html', title='Reset Password', form=form)
