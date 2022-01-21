import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from user.billing import valid_payment


# Character check to check for special characters (prevents security exploits)
def character_check(form,field):
    excluded_chars = "*?!'^+%&/()=}][{$#@<>"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    firstname = StringField(validators=[InputRequired(), character_check])
    lastname = StringField(validators=[InputRequired(), character_check])

    # MAYBE INCLUDE PREFIX FOR INTERNATIONAL NUMBERS? (Can be done jankily very easily)
    phone = StringField(validators=[Length(min=0, max=12, message='This is not a valid phone number')])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20, message='Password must be between 8 and 20 characters in length.')])
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo('password', message='Both password fields must be equal!')])
    submit = SubmitField()

    # Password validator
    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[^\w\s])')
        if not p.match(self.password.data):
            raise ValidationError("Password must contain at least 1 digit, 1 uppercase letter and 1 special character.")


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired()])
    otp = StringField(validators=[InputRequired()])
    submit = SubmitField()


class DonateForm(FlaskForm):

    donation = IntegerField(validators=[InputRequired()])
    cardnum = StringField(validators=[InputRequired(), Length(min=16, max=16, message='Card number must be 16 digits in length')])

    # TODO add CVC to
    # cvc = StringField(validators=[InputRequired(), Length(min=2, max=3, message='CVV must be 3 digits long')])

    submit = SubmitField()

    # Donation bank validator
    def validate_cardnum(self, cardnum):
        donation = self.donation.data
        card_number = self.cardnum.data
        if valid_payment(donation, card_number):  # forward data to billing.py
            raise ValidationError("Unable to make this donation, please check with your bank")


class BillingForm(FlaskForm):

    address_1 = StringField(validators=[InputRequired(), Length(min=3, max=100, message="This field doesn't look right")])
    address_2 = StringField(validators=[Length(min=3, max=100, message="This field doesn't look right")])
    city_town = StringField(validators=[InputRequired(), Length(min=3, max=100, message="This field doesn't look right")])
    county = StringField(validators=[InputRequired(), Length(min=3, max=100, message="This field doesn't look right")])
    cardnum = StringField(validators=[InputRequired(), Length(min=16, max=16, message='Card number must be 16 digits in length')])

    # TODO add CVC
    # cvc = StringField(validators=[InputRequired(), Length(min=2, max=3, message='CVV must be 3 digits long')])

    submit = SubmitField()

    # Donation bank validator
    def validate_cardnum(self, cardnum):
        cost = 10  # TODO get shirt price here
        card_number = self.cardnum.data
        if valid_payment(cost, card_number):  # forward data to billing.py
            raise ValidationError("Unable to make this payment, please check with your bank")
