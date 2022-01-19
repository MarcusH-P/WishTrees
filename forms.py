import re
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError

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
    phone = StringField(validators=[Length(min=10, max=11, message='This is not a valid phone number')])
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
