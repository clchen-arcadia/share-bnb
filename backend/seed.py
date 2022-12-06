from models import db, User, Listing, Message

db.drop_all()
db.create_all()

u1 = User(
    username="u1",
    email="u1@u1.com",
    first_name="f_name_1",
    last_name="l_name_1",
)

u2 = User(
    username="u2",
    email="u2@u2.com",
    first_name="f_name_2",
    last_name="l_name_2",
)

u3 = User(
    username="u3",
    email="u3@u3.com",
    first_name="f_name_3",
    last_name="l_name_3",
)

l1 = Listing(
    host_username="u1",
    address="1234 Barton Creek Lane, Houston, TX 77096",
    price=100,
)

l2 = Listing(
    host_username="u2",
    address="1234 Avenue E, New York, NY 10025",
    price=200,
)

l3 = Listing(
    host_username="u3",
    address="1234 Sidney Drive, San Francisco, CA 94105",
    price=300,
)

m1 = Message(
    sender_username="u1",
    receiver_username="u2",
    text="Can I book this place?"
)

m2 = Message(
    sender_username="u2",
    receiver_username="u1",
    text="Is this place available?"
)

m3 = Message(
    sender_username="u3",
    receiver_username="u2",
    text="Is this available for this weekend?"
)


db.session.add_all([u1, u2, u3])
db.session.commit()
db.session.add_all([l1, l2, l3])
db.session.commit()
db.session.add_all([m1, m2, m3])
db.session.commit()
