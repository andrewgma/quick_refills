from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, IntegerField
from wtforms.validators import Required, Optional, Length

class LoginForm(Form):
	username = TextField('username', validators = [Required()])
	password = PasswordField('password', validators = [Required()])
	remember_me = BooleanField('remember_me', default=False)

class SignupForm(Form):
	username = TextField('username', validators = [Required()])
	password = PasswordField('password', validators = [Required()])
	store_num = IntegerField('store_num', validators = [Optional()])
	remember_me = BooleanField('remember_me', default=False)

class AddRxForm(Form):
	rx_num = IntegerField('rx_num', validators = [Required()])
	rx_name = TextField('rx_name', validators = [Optional()])

class StoreNumForm(Form):
	store_num = TextField('store_num', validators=[Required(), 
		Length(min=10,max=10, message='errorrr')])