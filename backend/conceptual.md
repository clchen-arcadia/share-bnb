DATABASES:
    share_bnb
    share_bnb_test

TABLES:

users
    id (autoincrement, primary_key)
    username
    email
    first_name
    last_name
    phone_number
    payment_info

listings
    id (autoincrement, primary_key)
    host_username (references users)
    price
    location

messages
    id (autoincrement, primary_key)
    sender_id (co unique)
    receiver_id (co unique)
    text
    timestamp

photos
    id (autoincrement, primary_key)
    listing_id (references listings)
    filepath (in AWS S3)
