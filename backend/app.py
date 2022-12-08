import os

from dotenv import load_dotenv

# from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy.exc import (IntegrityError)
from forms import (UserSignup, LoginForm, ListingForm)
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
from models import db, connect_db, User, Listing

from s3_helpers import upload_file, show_image, show_one_image
from middleware import (
    ensure_logged_in,
    ensure_admin,
    ensure_admin_or_correct_user,
    ensure_admin_or_correct_host
)
import jwt

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

    if 'token' in request.headers:
        token = request.headers['token']
        try:
            payload = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=['HS256'],
                options={"verify_signature": True})
            g.user = payload
        except jwt.exceptions.InvalidSignatureError as e:
            print("INVALID SIG, ERR IS", e)
            g.user = None

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
# Routes for authentication/authorization


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
            token = User.signup(username, email, password,
                                first_name, last_name)
            db.session.commit()

        except IntegrityError as e:
            print("ERR: ", e)
            return jsonify({'error': "Username/email already exists."})

        return jsonify({"token": token}), 201

    else:
        return jsonify(errors=form.errors)

@app.route('/login', methods=["POST"])
def login():
    """Handle user login
    Accepts username and password as JSON
    Returns JSON of {token} or {error}
    """

    data = MultiDict(mapping=request.json)
    form = LoginForm(data)

    if form.validate():
        username = data["username"]
        password = data["password"]

        token = User.authenticate(username, password)

        if token:
            return jsonify({'token': token})
        elif not token:
            return jsonify({'error': 'Invalid username/password'})
    return jsonify(errors=form.errors)

##############################################################################
# Routes for Users

@app.route('/users/')
@ensure_admin
def get_all_users():
    return

@app.route('/users/<username>')
@ensure_admin_or_correct_user
def get_user(username):
    print("TEST>>>>>> username=", username)
    return jsonify({'test':'you got here'})

##############################################################################
# Routes for Listings

@app.route('/listings')
def get_all_listing():
    print("LISTING>>>>>>", type(Listing.query.all()))
    listings_output = []
    for listing in Listing.query.all():
        listings_output.append(listing.to_dict())
    return jsonify({'listings': listings_output})

@app.route('/listings/<int:listing_id>', methods=['GET'])
def get_listing(listing_id):
    return jsonify({'listing': Listing.query.get_or_404(listing_id).to_dict()})

@app.route('/listings/', methods=['POST'])
@ensure_logged_in
def post_new_listing():
    try:
        Listing.create_new_listing()
        db.session.commit()
    except IntegrityError as e:
        print("ERR: ", e)
        return jsonify({'error': 'Problem creating listing'})
    return jsonify({'test': 'you got here'})

@app.route('/listings/<listing_id>', methods=['DELETE'])
@ensure_admin_or_correct_host
def delete_listing(listing_id):
    Listing.query.filter(Listing.id==listing_id).delete()
    db.session.commit()
    return jsonify({'Success': 'Listing deleted'})

@app.route('/listings/<listing_id>', methods=['PUT'])
@ensure_admin_or_correct_host
def update_listing(listing_id):

    listing = Listing.query.get_or_404(listing_id)
    data = MultiDict(mapping=request.json)
    form = ListingForm(data)

    if form.validate():
        listing.title = data['title']
        listing.address = data['address']
        listing.description = data['description']
        listing.price = data['price']

        db.session.commit()
        return jsonify({'Success': 'Listing updated'})

    return jsonify(errors=form.errors)


##############################################################################
# Routes for Images for Listings



##############################################################################
# Routes for Messages



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
@ensure_logged_in
def list_photos():
    contents = show_image(BUCKET)
    print("contents is>>>>>>>>>>>>>", type(contents), contents)
    return jsonify({'contents': contents})
