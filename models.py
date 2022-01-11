import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)


    # User authentication information.
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    pin_key = db.Column(db.String(100), nullable=False)

    # User activity information
    registered_on = db.Column(db.DateTime, nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)

    # User information
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')

    def __init__(self, email, firstname, lastname, phone, password, pin_key, role):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.password = generate_password_hash(password) # IS THIS HASH GOOD? IDK PROBABLY
        self.pin_key = pin_key
        self.role = role
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None

def init_db():
    db.drop_all()
    db.create_all()
    admin = User(email='admin@email.com',
                 password='Admin1!',
                 pin_key='BFB5S34STBLZCOB22K6PPYDCMZMH46OJ',
                 firstname='Alice',
                 lastname='Jones',
                 role='admin')
    db.session.add(admin)
    db.session.commit()
