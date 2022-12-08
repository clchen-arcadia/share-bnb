from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Email, Length, InputRequired, Optional, URL


class UserSignup(FlaskForm):
    """Form for signing up a new user"""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = StringField(
        "Password",
        validators=[Length(min=6)]
    )

    email = StringField(
        "Email",
        validators=[InputRequired()]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired()]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired()]
    )

#####################################################################


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


#####################################################################

class ListingForm(FlaskForm):
    """New or Edit Listing Form"""

    title = StringField('Title', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])


#####################################################################

class NewMessageForm(FlaskForm):
    """New Message Form"""

    to_username = StringField('To Username', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
