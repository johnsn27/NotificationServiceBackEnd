import sqlite3

conn = sqlite3.connect('BOOKING.db')  # You can create a new database by changing the name within the quotations
c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

# Create table - CLIENTS
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

# Note that the syntax to create new tables should only be used once in the code (unless you dropped the table at the end of the code). 
# The [generated_id] column is used to set an auto-increment ID for each record
# When creating a new table, you can add both the field names as well as the field formats (e.g., Text)