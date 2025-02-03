from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

academic_levels = [
    ('high_school', 'High School'),
    ('undergraduate', 'Undergraduate'),
    ('graduate', 'Graduate'),
    ('other', 'Other')
]

class SetupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    academic_level = SelectField('Academic Level', choices=academic_levels, validators=[DataRequired()])
    interests = TextAreaField('Interests/Career Goals', validators=[DataRequired()])
    submit = SubmitField('Start Chatting')