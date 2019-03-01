import sqlite3

conn = sqlite3.connect('BOOKING.db')
c = conn.cursor()

c.execute('''CREATE TABLE BOOKINGS (
            [BookingId] int,
            [UserId] int,
            [RoomId] int,
            [StartTime] datetime,
            [EndTime] datetime,
            FOREIGN KEY (UserId) REFERENCES USERS (id)
            FOREIGN KEY (RoomId) REFERENCES RoomId (id)
             )''')

c.execute('''CREATE TABLE ROOMS (
            [id] int,
            [Name] text,
            [Location] text,
            [Floor] text,
            [Capacity] int
            )''')

c.execute('''CREATE TABLE USERS(
             [id] int PRIMARY KEY,
             [Name] text,
             [Email] text
             )''')

c.execute('''CREATE TABLE WATCHED (
            [WatchedId] int,
            [UserId] int,
            [Capacity] int,
            [StartTime] datetime,
            [EndTime] datetime,
            FOREIGN KEY (UserId) REFERENCES USERS (id)
             )''')

conn.commit()
