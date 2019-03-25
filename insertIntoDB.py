import sqlite3
import pandas as pd
from pandas import DataFrame

def insertIntoDB(databaseName):
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()

    read_clients = pd.read_csv (r'csvs/Bookings.csv')
    read_clients.to_sql('BOOKINGS', conn, if_exists='append', index = False)

    read_clients = pd.read_csv (r'csvs/Rooms.csv')
    read_clients.to_sql('ROOMS', conn, if_exists='append', index = False)

    read_clients = pd.read_csv (r'csvs/Users.csv')
    read_clients.to_sql('USERS', conn, if_exists='append', index = False)

    read_clients = pd.read_csv (r'csvs/Watched.csv')
    read_clients.to_sql('WATCHED', conn, if_exists='append', index = False)