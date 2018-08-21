from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class CreateTimetableForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Submit')

class EditTimetableForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    time = DateTimeField('Start time')
    submit = SubmitField('Submit')

class CreateEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    description = StringField('Description')
    time = DateTimeField('Time', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    description = StringField('Description')
    time = DateTimeField('Time', validators=[DataRequired()])
    submit = SubmitField('Submit')