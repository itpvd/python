from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class loginForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	password = StringField('Password',validators=[DataRequired()])
	submit = SubmitField('login')
class registerForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	password = StringField('Password',validators=[DataRequired()])
	confilmpass = StringField('Confilm',validators=[DataRequired()])
	submit = SubmitField('sign up')