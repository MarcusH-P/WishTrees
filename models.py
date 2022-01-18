import datetime
import base64
import os
import onetimepass
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # User authentication information.
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    otp_secret = db.Column(db.String(100), nullable=False)

    # User activity information
    registered_on = db.Column(db.DateTime, nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)
    otp_setup = db.Column(db.Boolean, nullable=True)

    # User information
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')
    user_key = db.Column(db.String(100), nullable=False, primary_key=True)

    def __init__(self, email, firstname, lastname, phone, password, role):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.password = generate_password_hash(password)  # IS THIS HASH GOOD? IDK PROBABLY
        self.role = role
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None
        if self.otp_secret is None:
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')  # Creates One Time Password secret
        self.otp_setup = None

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

    def __init__(self, product_number, product_type, product_colour, charity_name):
        self.product_number = product_number
        self.product_type = product_type
        self.product_colour = product_colour
        self.charity_name = charity_name


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


class Quiz(UserMixin, db.Model):
    __tablename__ = 'quiz_game'

    quiz_key = db.Column(db.String(100), nullable=False, primary_key=True)
    question_number = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String(100), nullable=False)

    def __init__(self, quiz_key, question_number, question):
        self.quiz_key = quiz_key
        self.question_number = question_number
        self.question = question


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


class SecurityError(UserMixin, db.Model):
    __tablename__ = 'security_page_error'

    error_id = db.Column(db.Integer, primary_key=True)
    error = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, error, date):
        self.error = error
        self.date = date


def init_db():
    db.drop_all()
    db.create_all()
    admin = User(email='admin@email.com',
                 password='Admin1!',
                 firstname='Alice',
                 lastname='Jones',
                 role='admin',
                 phone=None)
    db.session.add(admin)
    db.session.commit()
