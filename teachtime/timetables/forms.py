from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, Length, ValidationError

class CreateTimetableForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Submit')

class EditTimetableForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    start_date = DateField('Start date')
    submit = SubmitField('Submit')

class CreateEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    description = StringField('Description')
    start_time = TimeField('Start time', validators=[DataRequired()])
    end_time = TimeField('End time', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    description = StringField('Description')
    start_time = TimeField('Start time', validators=[DataRequired()])
    end_time = TimeField('End time', validators=[DataRequired()])
    submit = SubmitField('Submit')