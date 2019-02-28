import sqlite3
import pandas as pd
from pandas import DataFrame

conn = sqlite3.connect('BOOKING.db')  
c = conn.cursor()

# c.execute('''SELECT * FROM USERS WHERE USERS.id=1''')
def getEmail():
    c.execute('''SELECT Email FROM USERS,BOOKINGS
    WHERE USERS.id == BOOKINGS.UserId''')
    emailList = [item[0] for item in c.fetchall()]
    email = ''.join(emailList)
    return email