import os

from dotenv import load_dotenv
from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy.exc import (IntegrityError)

from forms import (
    UserAddForm, UserEditForm, LoginForm, MessageForm, UserSignup
)

from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    session,
    g,
    jsonify
)

from werkzeug.datastructures import MultiDict

from models import db, connect_db, User

app = Flask(__name__)

load_dotenv()

CURR_USER_KEY = "curr_user"




# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

app.config['WTF_CSRF_ENABLED'] = False

connect_db(app)

##############################################################################
# app.before_requests---these run before every request!

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


# @app.before_request
# def add_csrf_to_g():
#     """Add a csrf form to g"""

#     g.csrf_form = CSRFProtectForm()

##############################################################################
# Helper functions

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Log out user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

##############################################################################
# Routes

@app.route('/signup', methods=["POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    data = MultiDict(mapping=request.json)
    form = UserSignup(data)

    # ..., meta={'csrf': False}


    if form.validate():

        username = data["username"]
        password = data["password"]
        email = data["email"]
        first_name = data["first_name"]
        last_name = data["last_name"]

        try:
            user = User.signup(username, email, password, first_name, last_name)
            db.session.commit()

        except IntegrityError:
            return jsonify(errors=IntegrityError)


        print("TEST>>>>>>>>>>>>>>>>> user.to_dict", user.to_dict)
        return jsonify(user.to_dict())

    else:
        return jsonify(errors=form.errors)
