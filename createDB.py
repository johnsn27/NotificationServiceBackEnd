import sqlite3

def createDB(databaseName):
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()

    c.execute('''CREATE TABLE BOOKINGS (
                [BookingId] int,
                [UserId] int,
                [RoomId] int,
                [Name] text,
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
                [Capacity] int,
                [Building] text
                )''')

    c.execute('''CREATE TABLE USERS(
                [id] int PRIMARY KEY,
                [Firstname] text,
                [Lastname] text,
                [Email] text
                )''')

    c.execute('''CREATE TABLE WATCHED (
                [WatchedId] int,
                [UserId] int,
                [RoomId] int,
                [Capacity] int,
                [StartTime] datetime,
                [EndTime] datetime,
                FOREIGN KEY (UserId) REFERENCES USERS (id)
                )''')

    conn.commit()

