from flask import render_template, flash, redirect, url_for, request, session, Blueprint
from forms import RegisterForm, LoginForm
from models import User
from app import db
from werkzeug.security import check_password_hash

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')

@users_blueprint.route('/register', methods=['GET', 'POST']) # I DONT UNDERSTAND THE @users_blueprint.route
def register():
    # create signup form object
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('register.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        phone=form.phone.data,
                        password=form.password.data,
                        pin_key=form.pin_key.data,
                        role='user')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # sends user to login page
        return redirect(url_for('login'))
    # if request method is GET or form not valid re-render signup page
    return render_template('register.html', form=form)

@users_blueprint.route('/login', methods=['GET', 'POST']) # AGAIN DONT UNDERSTAND @users_blueprint.route
def login():

    # if session attribute logins does not exist create attribute logins
    if not session.get('logins'):
        session['logins'] = 0

    form = LoginForm()
    if form.validate_on_submit():
        #to increase login attempts
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

            return render_template('login.html', form=form)
            logging.warning('SECURITY - Failed login attempt [%s, %s]', form.email.data, request.remote_addr) # NEED TO FIX IP LOGGING THEN MAYBE SET UP LOCKOUTS BASED ON IP??

        if pyotp.TOTP(user.pin_key).verify(form.pin.data):
            login_user(user)

            # if user is verified reset login attempts to 0
            session['logins'] = 0

            user.last_logged_in = user.current_logged_in
            user.current_logged_in = datetime.now()
            db.session.add(user)
            db.session.commit()
            logging.warning('SECURITY - Log in [%s, %s, %s]', current_user.id, current_user.email,
                            request.remote_addr)
            if current_user.role == 'user':
                return profile()
            elif current_user.role == 'admin':
                return render_template('admin.html', name=current_user.firstname + ' ' + current_user.lastname)


        else:
            flash("You have supplied an invalid 2FA token!", "danger")
    return render_template('login.html', form=form)
