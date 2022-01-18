import logging
import pyotp
import pyqrcode
from io import BytesIO
from flask import render_template, flash, redirect, url_for, request, session, Blueprint
from forms import RegisterForm, LoginForm
from models import User, Security
from app import db
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])  # I DONT UNDERSTAND THE @users_blueprint.route
def register():
    # create signup form object
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user and user.otp_setup:
            flash('Sorry. An account for that email already exists')
            return render_template('register.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        phone=form.phone.data,
                        password=form.password.data,
                        role='user')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # sends user to login page
        # redirect to the two-factor auth page, passing username in session
        session['email'] = user.email
        return redirect(url_for('2fa_setup'))

    # if request method is GET or form not valid re-render signup page
    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])  # AGAIN DON'T UNDERSTAND @users_blueprint.route
def login():

    # if session attribute logins does not exist create attribute logins
    if not session.get('logins'):
        session['logins'] = 0

    form = LoginForm()
    if form.validate_on_submit():
        # to increase login attempts
        session['logins'] += 1
        logger = session['logins']

        user = User.query.filter_by(email=form.email.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            # if no match create appropriate error message based on login attempts
            if logger == 2:
                flash('Please check your login details and try again. 1 login attempt remaining')
            elif logger == 1:
                flash('Please check your login details and try again. 2 login attempts remaining')
            elif logger >= 3:
                flash('Number of incorrect logins exceeded')

            failed_login = Security(  # Adds failed login event to security_login_logout
                login='failed login',
                email=form.email,
                date=datetime.now())
            db.session.add(failed_login)
            return render_template('login.html', form=form)

        if pyotp.TOTP(user.pin_key).verify(form.pin.data):
            login_user(user)

            # if user is verified reset login attempts to 0
            session['logins'] = 0

            user.last_logged_in = user.current_logged_in
            user.current_logged_in = datetime.now()
            user.otp_setup = True

            new_login = Security(  # Adds login event to security_login_logout
                            login='login',
                            email=form.email,
                            date=datetime.now())
            db.session.add(new_login)
            db.session.add(user)
            db.session.commit()

            if current_user.role == 'user':
                return render_template('home.html')
            elif current_user.role == 'admin':
                return render_template('admin.html')


        else:
            flash("You have supplied an invalid 2FA token!", "danger")
    return render_template('login.html', form=form)


@users_blueprint.route('/twofactor')
def two_factor_setup():
    if 'email' not in session:
        return redirect(url_for('home'))
    user = User.query.filter_by(email=session['email']).first()
    if user is None:
        return redirect(url_for('home'))

    return render_template('2faSetup.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}  # Since the page includes sensitive information, this ensures sure the browser does not cache it and save the QR code


@users_blueprint.route('/qrcode')
def qrcode():
    if 'email' not in session:
        return render_template('404.html')
    user = User.query.filter_by(email=session['email']).first()
    if user is None:
        return render_template('404.html')

    del session['email']

    # render qrcode
    url = pyqrcode.create(user.get_uri())
    stream = BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@users_blueprint.route('/logout')
@login_required
def logout():
    new_logout = Security(  # Adds login event to security_login_logout
        login='logout',
        email=current_user.email,
        date=datetime.now())
    logout_user()
    db.session.add(new_logout)
    return redirect(url_for('index'))
