from app import app
from models import db, User, Listing, Photo, Message

db.drop_all()
db.create_all()

u1 = User(
    email="u1@u1.com",
    first_name="f_name_1",
    last_name="l_name_1",
)

u2 = User(
    email="u2@u2.com",
    first_name="f_name_2",
    last_name="l_name_2",
)

u3 = User(
    email="u3@u3.com",
    first_name="f_name_3",
    last_name="l_name_3",
)


db.session.add_all([u1, u2, u3])
db.session.commit()
