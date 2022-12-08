import os

from dotenv import load_dotenv

# from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy.exc import (IntegrityError)
from forms import (UserSignup, LoginForm, ListingForm, NewMessageForm)
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
from models import db, connect_db, User, Listing, Message

from s3_helpers import upload_file, show_image, show_one_image
from middleware import (
    ensure_logged_in,
    ensure_admin,
    ensure_admin_or_correct_user,
    ensure_admin_or_correct_host,
    ensure_correct_user
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
    return jsonify({'test': 'you got here'})

##############################################################################
# Routes for Listings


@app.route('/listings')
def get_all_listing():
    """Get all listings"""
    listings_output = []
    for listing in Listing.query.all():
        listings_output.append(listing.to_dict())
    return jsonify({'listings': listings_output})


@app.route('/listings/<int:listing_id>', methods=['GET'])
def get_listing(listing_id):
    """Get one listing"""
    return jsonify({'listing': Listing.query.get_or_404(listing_id).to_dict()})


@app.route('/<username>/listings', methods=['POST'])
@ensure_logged_in
def post_new_listing(username):
    """Add a new listing"""

    data = MultiDict(mapping=request.json)
    form = ListingForm(data)

    if form.validate():
        title = data['title']
        address = data['address']
        description = data['description']
        price = data['price']

        try:
            Listing.create_new_listing(
                host_username=username,
                title=title,
                address=address,
                description=description,
                price=price
            )
            db.session.commit()

        except IntegrityError as e:
            print("ERR: ", e)
            return jsonify({'error': 'Problem creating listing'})
    return jsonify({'test': 'you got here'})


@app.route('/listings/<listing_id>', methods=['DELETE'])
@ensure_admin_or_correct_host
def delete_listing(listing_id):
    Listing.query.filter(Listing.id == listing_id).delete()
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
# Routes for Images


##############################################################################
# Routes for Messages
@app.route('/<username>/messages/<other_username>', methods=["GET"])
@ensure_admin_or_correct_user
def get_all_messages(username, other_username):
    user = User.query.get_or_404(username)
    sent_messages_to_other_username = user.filter_messages_sent_to_username(
        other_username)
    received_messages_from_other_username = user.filter_messages_from_username(
        other_username)

    sent_messages = []
    received_messages = []

    for message in sent_messages_to_other_username:
        sent_messages.append(message.to_dict())
    for message in received_messages_from_other_username:
        received_messages.append(message.to_dict())

    return jsonify({"sent_messages": sent_messages,
                    "received_messages": received_messages})


@app.route('/<username>/messages', methods=["POST"])
@ensure_correct_user
def send_new_message(username):
    data = MultiDict(mapping=request.json)
    form = NewMessageForm(data)

    to_username = data['to_username']
    text = data['text']

    if form.validate():
        try:
            message = Message.create_new_message(to_username, username, text)
            db.session.commit()
            return jsonify({"message": message.to_dict()}), 201
        except IntegrityError as e:
            print("ERR: ", e)
            return jsonify({"error": "Problem posting message."})

    else:
        return jsonify(errors=form.errors)

##############################################################################
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
    breakpoint()
    # file = request.get['file']
    files = request.files.getlist("file")
    # print(request.files["file[]"])
    # name = request.form.get('name')

    for x in files:
        print(x, "<------- x")

    print("files ------------------------------------>", type(files))
    print("files ------------------------------------>", files)

    for file in files:
        print(file, "<<<<<file")
    # file.save(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))
    # upload_file(f"uploads/{file.filename}", BUCKET)

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
