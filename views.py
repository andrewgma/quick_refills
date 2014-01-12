from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from models import User, Rx
from forms import LoginForm, SignupForm, AddRxForm, StoreNumForm
from twilio.rest import TwilioRestClient
import time

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
	user = g.user
	rxs = None
	phone_formatted = None
	form = AddRxForm()
	form2 = StoreNumForm()

	if user is not None and user.is_authenticated():
		if form2.validate_on_submit():
			user.store_num = form2.store_num.data
			user.save()
			flash('Store number added')

	if user is not None and user.is_authenticated() and user.store_num is not None:
		phone_formatted = str(user.store_num)[0:3] + "." + \
			str(user.store_num)[3:6] + "." + \
			str(user.store_num)[6:10]

	if user is not None and user.is_authenticated():
		all_rxs = user.rxs
		rxs = [dict(rx_num=rx.rx_num, rx_name=rx.rx_name) for rx in all_rxs]
		if form.validate_on_submit():
			new_rx_num = form.rx_num.data
			if new_rx_num not in [rx.rx_num for rx in all_rxs]:
				new_rx = Rx(rx_num = form.rx_num.data, rx_name = form.rx_name.data)
				user.rxs.append(new_rx)
				user.save()
				flash('new Rx added')
				# forces form to refresh
				return redirect(url_for('index'))
			else:
				flash('this Rx already exists')

	return render_template('index.html', 
		title = 'Home', user = user, rxs = rxs, 
		form = form, form2 = form2, 
		phone_formatted = phone_formatted)

@app.route('/refill', methods = ['POST'])
def refill():
	if g.user.store_num:
		# Hidden to keep Twilio account private
	else:
		flash('Need to enter pharmacy phone number!')
	return redirect(url_for('index'))

@app.route('/delete', methods = ['POST'])
def delete_rx():
	user = g.user
	rx_num = request.form['rx_to_delete']
	User.objects(name = user.name).update_one(pull__rxs__rx_num=rx_num)
	flash('Rx # ' + rx_num + ' deleted')
	return redirect(url_for('index'))

@app.route('/delete_store_num')
def delete_store_num():
	user = g.user
	user.store_num = None
	user.save()
	flash('Store number removed')
	return redirect(url_for('index'))

@lm.user_loader
def load_user(name):
	user = User.objects(name=name)
	if len(user) > 0:
		return user[0]
	else:
		return None

@app.before_request
def before_request():
	g.user = current_user

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.objects(name = form.username.data)
		if len(user) == 0:
			flash ('No such user')
			return render_template('login.html', title = 'Log in', form=form)
		if user[0].check_password(form.password.data):
			login_user(user[0], remember = form.remember_me.data)
			flash('Logged in successfully')
			return redirect(url_for('index'))
		flash('Wrong password')
	return render_template('login.html', title = 'Log in', form=form)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = SignupForm()
	if form.validate_on_submit():
		check_user = User.objects(name = form.username.data)
		if len(check_user) == 0:
			new_user = User(name=form.username.data, 
				store_num=form.store_num.data)
			new_user.set_password(form.password.data)
			new_user.save()
			login_user(new_user, remember = form.remember_me.data)
			return redirect(url_for('index'))
		else:
			flash('Username taken. Pick a different one.')
			return render_template('signup.html', title = 'Sign up', form=form)
	return render_template('signup.html', title = 'Signup', form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()