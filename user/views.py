import pyotp
import pyqrcode
from io import BytesIO
from flask import render_template, flash, redirect, url_for, request, session, Blueprint
from user.forms import RegisterForm, LoginForm, DonateForm
from models import User, Security, Donation, new_security_event, new_security_error
from app import db, db_add_commit
from user.forms import RegisterForm, LoginForm, DonateForm, BillingForm
from models import User, Security, Donation, Order
from app import db
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:  # I WANNA ADD A FUNCTION SO THAT IF THE USER HASNT LOGGED IN THEN THEY CAN REGISTER AGAIN !!DELETING THEIR OLD ACCOUNT FIRST!!!!!
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
        db.session.add(new_security_event('user registered', form.email.data))
        db.session.commit()

        # sends user to 2fa
        session['email'] = new_user.email
        return render_template('otp-setup.html')

    # if request method is GET or form not valid re-render signup page
    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
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

            db_add_commit(new_security_event('failed login', form.email.data))
            return render_template('login.html', form=form)

        if pyotp.TOTP(user.otp_secret).verify(form.otp.data):
            login_user(user)

            # if user is verified reset login attempts to 0
            session['logins'] = 0

            user.last_logged_in = user.current_logged_in
            user.current_logged_in = datetime.now()
            user.otp_setup = True

            db.session.add(new_security_event('login', current_user.email))
            db.session.add(user)
            db.session.commit()

            if current_user.role == 'user':
                return render_template('home.html')
            elif current_user.role == 'admin':
                return render_template('admin.html')


        else:
            flash("You have supplied an invalid 2FA token!", "danger")
    return render_template('login.html', form=form)


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
    db_add_commit(new_security_event('logout', current_user.email))
    return redirect(url_for('index'))


@users_blueprint.route("/profile")
def profile():
    return render_template('profile.html',
                           email=current_user.email,
                           firstname=current_user.firstname,
                           lastname=current_user.lastname,
                           phone=current_user.phone,
                           points=current_user.points)


@users_blueprint.route('/donate', methods=['GET', 'POST'])
def donate():
    # create signup form object
    form = DonateForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():

        # create a new user with the form data
        new_donation = Donation(
            user_key=current_user.user_key,
            donation_amount=form.donation.data)

        # add the new user to the database
        db_add_commit(new_donation)

        # TODO session['email'] = new_donation.email
        return render_template('home.html')

    # if request method is GET or form not valid re-render signup page
    return render_template('donate.html', form=form)


@users_blueprint.route('/billing', methods=['GET', 'POST'])
def billing():

    # create signup form object
    form = BillingForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():

        # create a new user with the form data
        new_order = Order(
            product_number="Product number",
            user_key=current_user.user_key,
            address_line_1=form.address_1.data,
            address_line_2=form.address_2.data,
            city_town=form.city_town.data,
            county=form.county.data,
            date=datetime.now())

        # add the new user to the database
        db.session.add(new_order)
        db.session.commit()

        # session['email'] = new_donation.email
        return render_template('home.html')

    # if request method is GET or form not valid re-render signup page
    return render_template('donate.html', form=form)
