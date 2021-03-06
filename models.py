import datetime
import base64
import os
import onetimepass
from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


# Reference to CSC2031 lottery web app
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # User authentication information.
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    otp_secret = db.Column(db.String(100), nullable=False)

    # User activity information
    registered_on = db.Column(db.DateTime, nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)

    # User information
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(100), nullable=False, default='user')
    user_key = db.Column(db.Integer, nullable=False, primary_key=True)
    points = db.Column(db.Integer, nullable=False, default=int(0))

    def get_id(self):
        return self.user_key

    def __init__(self, email, firstname, lastname, phone, password, role):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.password = generate_password_hash(password)
        self.role = role
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None
        if self.otp_secret is None:
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')  # Creates One Time Password secret

    def get_uri(self):  # Generates Uri for 2FA QR Code
        return 'otpauth://totp/WishTrees:{0}?secret={1}&issuer=WishTrees' \
            .format(self.email, self.otp_secret)

    def verify_otp(self, token):
        return onetimepass.valid_totp(self.otp_secret, token)


class Product(UserMixin, db.Model):
    __tablename__ = 'products'

    product_number = db.Column(db.String(100), nullable=False, primary_key=True)
    product_type = db.Column(db.String(100), nullable=False)
    product_colour = db.Column(db.String(100), nullable=False)
    charity_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False)

    def __init__(self, product_number, product_type, product_colour, charity_name, price):
        self.product_number = product_number
        self.product_type = product_type
        self.product_colour = product_colour
        self.charity_name = charity_name
        self.price = price


class Order(UserMixin, db.Model):
    __tablename__ = 'order_history'

    order_id = db.Column(db.Integer, primary_key=True)
    product_number = db.Column(db.String(100), nullable=False)
    user_key = db.Column(db.String(100), nullable=False)
    address_line_1 = db.Column(db.String(100), nullable=False)
    address_line_2 = db.Column(db.String(100), nullable=False)
    city_town = db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)

    def __init__(self, product_number, user_key, address_line_1, address_line_2, city_town, county, date):
        self.product_number = product_number
        self.user_key = user_key
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city_town = city_town
        self.county = county
        self.date = date


class QuizHistory(UserMixin, db.Model):
    __tablename__ = 'quiz_history'

    quiz_event_id = db.Column(db.Integer, primary_key=True)
    quiz_key = db.Column(db.String(100), nullable=False)
    user_key = db.Column(db.String(100), nullable=False)
    score = db.Column(db.String(100), nullable=False)

    def __init__(self, quiz_key, user_key, score):
        self.quiz_key = quiz_key
        self.user_key = user_key
        self.score = score


class Security(UserMixin, db.Model):
    __tablename__ = 'security_login_logout'

    event_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, login, email, date):
        self.login = login
        self.email = email
        self.date = date


def new_security_event(login, email):  # Creates security event to make logging more compact
    return Security(
        login=login,
        email=email,
        date=datetime.now()
    )


class SecurityError(UserMixin, db.Model):
    __tablename__ = 'security_page_error'

    error_id = db.Column(db.Integer, primary_key=True)
    error = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, error, date):
        self.error = error
        self.date = date


def new_security_error(error):  # Creates security error to make logging more compact
    return SecurityError(
        error=error,
        date=datetime.now()
    )


class Donation(UserMixin, db.Model):
    __tablename__ = 'donations'

    donation_id = db.Column(db.Integer, primary_key=True)
    user_key = db.Column(db.String(100), nullable=False)
    donation_amount = db.Column(db.Integer, nullable=False)

    def __init__(self, user_key, donation_amount):
        self.user_key = user_key
        self.donation_amount = donation_amount


def init_db():
    db.drop_all()
    db.create_all()

    admin = User(email='admin@gmail.com',
                 password='Passw0rd!',
                 firstname='Alex',
                 lastname='Smith',
                 role='admin',
                 phone=None)
    db.session.add(admin)

    user = User(email='stevebell@gmail.com',
                password='Pass1ng!t',
                firstname='Steve',
                lastname='Bell',
                role='user',
                phone='07546924889')
    db.session.add(user)

    charity = User(email='powerplanters@gmail.com',
                   password='Power2Tree$',
                   firstname='PowerPlanters',
                   lastname='org',
                   role='charity',
                   phone='07248854699')
    db.session.add(charity)

    # Adding all current products to the DB
    product_1 = Product(product_number="pp_tshirt_black_20",
                        product_type="T Shirt",
                        product_colour="Black",
                        charity_name="Power Planters",
                        price="20")

    product_2 = Product(product_number="wt_tshirt_black_20",
                        product_type="T Shirt",
                        product_colour="Black",
                        charity_name="WishTrees",
                        price="20")

    product_3 = Product(product_number="pp_tshirt_white_20",
                        product_type="T Shirt",
                        product_colour="White",
                        charity_name="Power Planters",
                        price="20")

    product_4 = Product(product_number="tru_tshirt_white_20",
                        product_type="T Shirt",
                        product_colour="White",
                        charity_name="Trees R Us",
                        price="20")

    product_5 = Product(product_number="tru_hoodie_black_40",
                        product_type="Hoodie",
                        product_colour="Black",
                        charity_name="Trees R Us",
                        price="40")

    product_6 = Product(product_number="wt_tshirt_grey_25",
                        product_type="T Shirt",
                        product_colour="Grey",
                        charity_name="WishTrees",
                        price="25")

    db.session.add(product_1)
    db.session.add(product_2)
    db.session.add(product_3)
    db.session.add(product_4)
    db.session.add(product_5)
    db.session.add(product_6)

    db.session.commit()
