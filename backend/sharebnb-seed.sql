INSERT INTO users (username, password, email, first_name, last_name, is_admin, is_host)
VALUES
('u1', '$2b$12$4AUULel4F2ZWq5jb2Jkv4Or6/mpBa.2w2PDOgv/ZYXZ4GxcXRQmyG', 'u1@u1.com', 'f_name_1',
'l_name_1', False, False),
('u2', '$2b$12$4AUULel4F2ZWq5jb2Jkv4Or6/mpBa.2w2PDOgv/ZYXZ4GxcXRQmyG', 'u2@u2.com', 'f_name_2',
'l_name_2', False, False),
('u3', '$2b$12$4AUULel4F2ZWq5jb2Jkv4Or6/mpBa.2w2PDOgv/ZYXZ4GxcXRQmyG', 'u3@u3.com', 'f_name_3',
'l_name_3', True, True);


INSERT INTO listings (id, host_username, title, address, description, price)
VALUES
(1, 'u1', 'Treehouse Loft', '1234 Barton Creek Lane, Houston, TX 77096',
'A beautiful treehouse for a wonderful experience in nature, perfect for an individual or family (max 2 adults 1 child) looking for a night or more away. Surrounded by towering trees and set back in a 3 acre domain, this treehouse offers you an intimate and relaxing stay. Minutes from historic churches and village museums.', 100),
(2, 'u2', 'Cozy Loft w/ Downtown Views', '1234 Avenue E, New York, NY 10025',
'The apartment is located downtown Manhattan, this renovated artist loft offers over 2,000 sq ft of chic living. Steps from Battery Park, Wall St, the Seaport, Tribeca and all major subways. The space offers a unique opportunity to live out your NYC dream vacation.', 200),
(3, 'u3', 'Overpriced Studio', '1234 Sidney Drive, San Francisco, CA 94105',
'This modern unit is located on the border of North Beach, Nob Hill and Russian Hill. It is near the Ferry Building Marketplace, Coit Tower and is a few minutes walking to impressive dining, shopping, and San Francisco Landmarks', 300);


INSERT INTO photos (id, listing_id, filepath)
VALUES
(1, 1, 'uploads/treehouse_1.jpeg'),
(2, 1, 'uploads/treehouse_2.jpeg'),
(3, 2, 'uploads/bungalow_1.jpeg'),
(4, 2, 'uploads/bungalow_2.jpeg'),
(5, 2, 'uploads/bungalow_3.jpeg'),
(6, 3, 'uploads/studio_1.jpeg'),
(7, 3, 'uploads/studio_2.jpeg'),
(8, 3, 'uploads/studio_3.jpeg');

INSERT INTO messages (id, sender_username, receiver_username, text, timestamp)
VALUES
(1, 'u1', 'u2', 'Can I book this place?', '2022-12-09 23:26:04.472063'),
(2, 'u2', 'u1', 'Is this place available?', '2022-12-09 23:26:04.472074'),
(3, 'u3', 'u2', 'Is this available for this weekend?', '2022-12-09 23:26:04.472078'),
(4, 'u1', 'u3', 'Is this available for this weekend!?!??!?!?', '2022-12-09 23:26:04.472082');
