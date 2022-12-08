"""SQLAlchemy models for Share BnB."""

from token_helpers import create_token
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User."""

    __tablename__ = "users"

    username = db.Column(db.Text, primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    isHost = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        """Serialize user to a dict of user info."""

        return {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "isAdmin": self.isAdmin,
            "isHost": self.isHost
        }

    messages_from = db.relationship(
        'Message',
        foreign_keys='Message.sender_username',
        backref="user_from")

    messages_to = db.relationship(
        'Message',
        foreign_keys='Message.receiver_username',
        backref="user_to")

    listings = db.relationship('Listing', backref="user")

    def __repr__(self):
        return f"""<User: {self.username}, {self.email}, {self.first_name} {self.last_name}>"""

    @classmethod
    def signup(cls, username, email, password, first_name, last_name):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
        )

        db.session.add(user)
        token = create_token(user)

        return token

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        # user = cls.query.get(username)
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Listing(db.Model):
    """Listing."""

    __tablename__ = "listings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    host_username = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
        nullable=False,
    )
    title = db.Column(
        db.Text,
        nullable=False,
    )
    address = db.Column(
        db.Text,
        nullable=False
    )
    description = db.Column(
        db.Text,
        nullable=False
    )
    price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    def __repr__(self):
        return f"""<Listing
        Host_username: {self.host_username},
        Address: {self.address},
        Price: {self.price}>"""


class Photo(db.Model):
    """Photo."""

    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    listing_id = db.Column(
        db.Integer,
        db.ForeignKey('listings.id', ondelete="cascade"),
        nullable=False,
    )
    filepath = db.Column(
        db.Text,
        nullable=False
    )

    def __repr__(self):
        return f"""<Photo
        id: {self.id},
        listing_id: {self.listing_id},
        filepath: {self.filepath}"""


class Message(db.Model):
    """Message."""

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_username = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
        nullable=False,
    )
    receiver_username = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
        nullable=False,
    )
    text = db.Column(
        db.Text,
        nullable=False
    )
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    def __repr__(self):
        return f"""<Message:
        Sender_username: {self.sender_username},
        Receiver_username: {self.receiver_username},
        Id: {self.id}>"""


def connect_db(app):
    """
    Connect to the database to Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
