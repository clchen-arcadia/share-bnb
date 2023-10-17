import os
from dotenv import load_dotenv
from flask import (
    Flask,
    request,
    g,
    jsonify
)
from flask_cors import CORS
from sqlalchemy.exc import (IntegrityError)
from forms import (UserSignup, LoginForm, ListingForm, NewMessageForm)
from werkzeug.utils import secure_filename
from werkzeug.datastructures import MultiDict
import jwt

from models import db, connect_db, User, Listing, Message, Photo
from s3_helpers import upload_file, get_image_url
from middleware import (
    ensure_logged_in,
    ensure_admin,
    ensure_admin_or_correct_user,
    ensure_admin_or_correct_host,
    ensure_correct_user
)

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
BUCKET = "rithm-share-bnb"
CURR_USER_KEY = "curr_user"

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

load_dotenv()

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
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
        first_name = data["firstName"]
        last_name = data["lastName"]

        try:
            token = User.signup(username, email, password,
                                first_name, last_name)
            db.session.commit()

        except IntegrityError as e:
            print("ERR: ", e)
            return jsonify({'error': "Username/email already exists."}), 400

        return jsonify({"token": token}), 201

    else:
        messages = []
        for err in form.errors:
            joined_messages = " ".join(form.errors[err])
            messages.append(f"{err}: {joined_messages}")
        return jsonify({'errors': messages}), 400


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
            return jsonify({'error': 'Invalid username/password'}), 400
    return jsonify(errors=form.errors)

##############################################################################
# Routes for Users


# TODO: write this
@app.route('/users/', methods=["GET"])
@ensure_admin
def get_all_users():
    return


@app.route('/users/<username>', methods=["GET"])
@ensure_admin_or_correct_user
def get_user(username):
    user = User.query.get_or_404(username)
    return jsonify({'user': user.to_dict()})

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
    """Get one listing (WITH PHOTOS?? no)"""
    # listing = Listing.query.get_or_404(listing_id)
    # photos = listing.photos
    # listing_with_photos = listing.to_dict()
    # listing_with_photos['photos'] = photos
    # return jsonify({'listing': listing_with_photos})
    return jsonify({'listing': Listing.query.get_or_404(listing_id).to_dict()})


@app.route('/<username>/listings', methods=['POST'])
@ensure_logged_in
@ensure_correct_user
def post_new_listing(username):
    """Add a new listing, consumes request.files for photos
    and consumes request.form for the rest of the form
    """

    files = request.files.getlist("file")

    form_data = MultiDict(mapping=request.form)
    form = ListingForm(form_data)

    # data = MultiDict(mapping=request.json)
    # form = ListingForm(data)

    if form.validate():
        title = form_data['title']
        address = form_data['address']
        description = form_data['description']
        price = form_data['price']

        # Create new Listing
        new_listing = None
        try:
            new_listing = Listing.create_new_listing(
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

        # Upload all photos to AWS and submit Photo instance to database
        try:
            for idx, file in enumerate(files):
                file.save(os.path.join(UPLOAD_FOLDER,
                          secure_filename(file.filename)))

                # NOTE: stretch goal to set filenames ourselves like f"username_listingId_photo_#"
                # new_filename = f"{new_listing.host_username}_{new_listing.id}_photo_{idx}"
                # os.rename(f"{UPLOAD_FOLDER}/{file.filename}", new_filename)

                upload_file(f"uploads/{file.filename}", BUCKET)

                try:
                    Photo.create_new_photo(
                        listing_id=new_listing.id,
                        filepath=f"uploads/{file.filename}"
                    )
                except IntegrityError as e:
                    return jsonify({
                        'error': 'Problem entering photo to database',
                        'message': e.__repr__()
                    })

        except Exception as e:
            return jsonify({
                'error': 'Problem uploading images to AWS',
                'message': e.__repr__()
            })

        db.session.commit()
        return jsonify({'success': 'created new listing'}), 201

    return jsonify(errors=form.errors)


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


@app.route('/listings/<listing_id>/photos', methods=['GET'])
def get_photos_for_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    photo_urls = []
    for photo in listing.photos:
        photo_urls.append(get_image_url(BUCKET, photo.filepath))

    return jsonify({'photos': photo_urls})

@app.route('/listings/<listing_id>/first_photo', methods=['GET'])
def get_first_photo_for_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    photo = Photo.query.filter(Photo.listing_id == listing.id).first_or_404()
    photo_url = get_image_url(BUCKET, photo.filepath)

    return jsonify({'photo': photo_url})

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
