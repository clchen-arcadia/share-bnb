from models import db, User, Listing, Message
from app import db

db.drop_all()
db.create_all()

u1 = User(
    username="u1",
    password='$2b$12$4AUULel4F2ZWq5jb2Jkv4Or6/mpBa.2w2PDOgv/ZYXZ4GxcXRQmyG',
    email="u1@u1.com",
    first_name="f_name_1",
    last_name="l_name_1",
)

u2 = User(
    username="u2",
    password='$2b$12$4AUULel4F2ZWq5jb2Jkv4Or6/mpBa.2w2PDOgv/ZYXZ4GxcXRQmyG',
    email="u2@u2.com",
    first_name="f_name_2",
    last_name="l_name_2",
)

u3 = User(
    username="u3",
    password='$2b$12$4AUULel4F2ZWq5jb2Jkv4Or6/mpBa.2w2PDOgv/ZYXZ4GxcXRQmyG',
    email="u3@u3.com",
    first_name="f_name_3",
    last_name="l_name_3",
)

l1 = Listing(
    host_username="u1",
    title="Treehouse Loft",
    address="1234 Barton Creek Lane, Houston, TX 77096",
    description="""A beautiful treehouse for a wonderful  experience in nature,
    perfect for an individual or family (max 2 adults 1 child) looking for a
    night or more away.  Surrounded by towering trees and set back in a 3 acre
    domain, this trehouse offers you an intimate and relaxing stay. Minutes
    from historic churches and village museums.""",
    price=100,
)

l2 = Listing(
    host_username="u2",
    title="Cozy Loft w/ Downtown Views",
    address="1234 Avenue E, New York, NY 10025",
    description="""The apartment is located downtown Manhattan, this renovated
    artist loft offers over 2,000 sq ft of chic living. Steps from Battery Park,
    Wall St, the Seaport, Tribeca and all major subways. The space offers a
    unique opportunity to live out your NYC dream vacation.""",
    price=200,
)

l3 = Listing(
    host_username="u3",
    title="Overpriced Studio",
    address="1234 Sidney Drive, San Francisco, CA 94105",
    description="""This modern unit is located on the border of North Beach,
    Nob Hill and Russian Hill. It's near the Ferry Building Marketplace, Coit
    Tower and is a few minutes walking to impressive dining, shopping, and San
    Francisco Landmarks""",
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
