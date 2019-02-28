import sqlite3
import pandas as pd
from pandas import DataFrame

conn = sqlite3.connect('BOOKING.db')
c = conn.cursor()

read_clients = pd.read_csv (r'/Users/johnsn27/Documents/Uni/NotificationServiceBackEnd/csvs/Bookings.csv')
read_clients.to_sql('BOOKINGS', conn, if_exists='append', index = False) # Insert the values from the csv file into the table 'BOOKING' 

read_clients = pd.read_csv (r'/Users/johnsn27/Documents/Uni/NotificationServiceBackEnd/csvs/Rooms.csv')
read_clients.to_sql('ROOMS', conn, if_exists='append', index = False) # Insert the values from the csv file into the table 'ROOMS' 

read_clients = pd.read_csv (r'/Users/johnsn27/Documents/Uni/NotificationServiceBackEnd/csvs/Users.csv')
read_clients.to_sql('USERS', conn, if_exists='append', index = False) # Insert the values from the csv file into the table 'USERS' 