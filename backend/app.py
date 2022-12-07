import os

from dotenv import load_dotenv

# from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy.exc import (IntegrityError)
from forms import (UserSignup)
from flask import (
    Flask,
    request,
    session,
    g,
    jsonify
)

from flask_cors import CORS, cross_origin

from werkzeug.utils import secure_filename
from werkzeug.datastructures import MultiDict
from models import db, connect_db, User
from middleware import test_decorator

from s3_helpers import upload_file, show_image, show_one_image


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
BUCKET = "rithm-share-bnb"

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


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


# toolbar = DebugToolbarExtension(app)

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

    If form valid: Create new user and add to DB. Return user (JSON)

    If form not valid: return error(JSON).

    If the there already is a user with that username: return error message (JSON)
    """
    data = MultiDict(mapping=request.json)
    form = UserSignup(data)

    if form.validate():

        username = data["username"]
        password = data["password"]
        email = data["email"]
        first_name = data["first_name"]
        last_name = data["last_name"]

        try:
            user = User.signup(username, email, password,
                               first_name, last_name)
            db.session.commit()

        except IntegrityError:
            return jsonify(errors=IntegrityError)

        return jsonify(user.to_dict())
        # TODO: NEED TO RETURN TOKEN

    else:
        return jsonify(errors=form.errors)


# @app.route('/test', methods=["GET"])
# @test_decorator
# def hello():
#     return jsonify("hello")


# @test_decorator  # going to call test_decorator and pass the joel fxn
# def joel(a, b):
#     return a + b


# joel = test_decorator(joel)

@app.route('/upload', methods=['POST'])
@cross_origin()
def handle_file_upload():
    # TODO: validate this incoming data

    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))
    upload_file(f"uploads/{file.filename}", BUCKET)

    return jsonify("success")



@app.route("/pics/1", methods=['GET'])
@cross_origin()
def list_one_photo():
    content = show_one_image(BUCKET, 'uploads/cute-dog-headshot.jpeg')
    print("contents is>>>>>>>>>>>>>", type(content), content)
    return jsonify({'content': content})

@app.route("/pics", methods=['GET'])
@cross_origin()
def list():
    contents = show_image(BUCKET)
    print("contents is>>>>>>>>>>>>>", type(contents), contents)
    return jsonify({'contents': contents})
