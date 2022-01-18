import datetime
import base64
import os
import onetimepass
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

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
    user_key = db.Column(db.String(100), nullable=False)

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

def init_db():
    db.drop_all()
    db.create_all()
    admin = User(email='admin@email.com',
                 password='Admin1!',
                 otp_secret='BFB5S34STBLZCOB22K6PPYDCMZMH46OJ',
                 firstname='Alice',
                 lastname='Jones',
                 role='admin',
                 phone='')
    db.session.add(admin)
    db.session.commit()
