import pyotp
import pyqrcode
from io import BytesIO
from flask import render_template, flash, redirect, url_for, request, session, Blueprint
from user.emails import email_users
from user.forms import RegisterForm, LoginForm, DonateForm
from models import User, Security, Donation, new_security_event, new_security_error
from app import db, db_add_commit
from user.forms import RegisterForm, LoginForm, DonateForm, BillingForm
from models import User, Security, Donation, Order
from app import db
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import smtplib
from email.message import EmailMessage
import random
from flask import render_template, redirect, url_for

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

            if current_user.role == 'user' or current_user.role == 'charity':
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
    logout_user()
    return redirect(url_for('home'))


@users_blueprint.route("/profile")
@login_required
def profile():
    return render_template('profile.html',
                           email=current_user.email,
                           firstname=current_user.firstname,
                           lastname=current_user.lastname,
                           phone=current_user.phone,
                           points=current_user.points)


@users_blueprint.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    # create donate form object
    form = DonateForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():

        # create a new user with the form data
        new_donation = Donation(
            user_key=current_user.user_key,
            donation_amount=form.donation.data)

        # add the new donation to the database
        db_add_commit(new_donation)

        return render_template('home.html')

    # if request method is GET or form not valid re-render donate page
    return render_template('donate.html', form=form)


@users_blueprint.route('/billing/<string:product>', methods=['GET', 'POST'])
@users_blueprint.route('/billing', methods=['GET', 'POST'])
@login_required
def billing(product):

    # create billing form object
    form = BillingForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():

        # create a new order with the form data
        new_order = Order(
            product_number=product,
            user_key=current_user.user_key,
            address_line_1=form.address_1.data,
            address_line_2=form.address_2.data,
            city_town=form.city_town.data,
            county=form.county.data,
            date=datetime.now())

        # add the new order to the database
        db.session.add(new_order)
        db.session.commit()

        return render_template('bought.html')

    # if request method is GET or form not valid re-render billing page
    return render_template('billing.html', form=form)


def get_cpu_image():
    cpu_list = [  # List of CPU images here
        "https://lh3.googleusercontent.com/pw/AM-JKLW06QsLA3Fjor8GZSFgLV4VpBa8c6iPHgLfY_mTcNMObz-zO38jooA9PXcPvRIoDOyxzvAHL0nupR5JLsb6zWa0RmG0qoVo3UgoauHEgGf8saF2Q5O00F2CiKQPSHspFXMqVOTXN-eSgkotfB-nQg=w338-h451-no",
        "https://lh3.googleusercontent.com/pw/AM-JKLV8kUOmG8C_ngoJpn1VGLgiqI_60oV7P1kA3Ld2Y8GfT7rVn2xlRr-RcBHDaVaf1fQKrtUx3RFzF-5R-eKUCqP2iLd2HfSHynlaHDCaKip3yJW2Wpbv1ApMAWazGfhLYf2BihJdg4x0RTPbWfs-HA=w338-h451-no",
        "https://lh3.googleusercontent.com/pw/AM-JKLWEdTc8alhDpleJnd7160WxRxLZBDlduOILR47fntpKq5KJ9t5Xx8d8SoOvMOAA4LVtrBOegurFLVAq9rDHVJ3gdNxLexhPCC9a1iHfp1hX5TCzkrviI7rQ8GqPOoxZcISMbf6GAFnPwufl6SjMLQ=w338-h451-no"
    ]

    return random.choice(cpu_list)


@users_blueprint.route('/email_user', methods=['POST'])
def email_user():

    recipient = current_user.email
    user_points = current_user.points

    html_content = ("""
    <!DOCTYPE html>
    <html>

    <head>

    <style>
    img {
      display: block;
      margin-left: auto;
      margin-right: auto;
    }
    </style>

    </head>

    <body style="background-color: #fff8cd;">
        <! WishTrees Logo >
        <img src="https://lh3.googleusercontent.com/pw/AM-JKLW4VYOR4dU9h4JzJsuNtnrqv2mktXIPtxyobM1uqXIrmN_ylHNYbgbmJ4toX0UCJFkomt_8aHYzdbcmVmFQdveCa8s-I5507xo5cjgscqCtV4XnLzWR9HJcfOas2CDmEEuXbzipnUjlMItej0ojzg=w3360-h946-no" alt="WishTrees Logo" width="90%">
        <br><br><h1 style="color: #c993dc; text-align:center">Here's your point summary</h1>
        <h2 style="color: #c993dc; text-align:center">""" + str(user_points) + """</h2>
        <br><br>
        
        <br><h1 style="color: #c993dc; text-align:center">How about a random charity to donate to?</h1>

        <div class="column">
            <img src=' """ + get_cpu_image() + """ ' alt='email_img'>
            <h1 style="color: #c993dc; text-align:center">Charities will always need your help!</h1>            
        </div>
        
        
    </body>
    </html>
    """)

    email_contents = EmailMessage()  # Sets email parameters

    # Login credentials for sender's email
    email_address = "WishTrees.Send@gmail.com"
    email_password = "hykbi5-hucwer-gabzyK"
    # If I had more time the program could
    # get a login token rather then storing
    # the password here

    email_contents['Subject'] = 'Your WishTrees Update is Here!'
    email_contents['From'] = email_address  # Senders email address
    email_contents['To'] = recipient

    # If the user blocks HTML emails this text will show
    email_contents.set_content("Please turn on HTML emails")

    # If HTML are allowed the predefined HTML parameter will show
    email_contents.add_alternative(html_content, subtype='html')

    # Logs into Gmail servers and sends an email with SMTP, Port 465
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(email_contents)

    return redirect(url_for('users.profile'))