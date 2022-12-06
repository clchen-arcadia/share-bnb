"""SQLAlchemy models for Share BnB."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User."""

    __tablename__ = "users"

    username = db.Column(db.Text, primary_key=True, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    isHost = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        """Serialize user to a dict of user info."""

        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


class Listing(db.Model):
    """Listing."""

    __tablename__ = "listings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    host_username = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
        nullable=False,
    )
    address = db.Column(
        db.Text,
        nullable=False
    )
    price = db.Column(
        db.Integer,
        nullable=False
    )


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


def connect_db(app):
    """
    Connect to the database to Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
