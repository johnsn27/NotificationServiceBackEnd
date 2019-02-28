import sqlite3
import pandas as pd
from pandas import DataFrame

conn = sqlite3.connect('BOOKING.db')  
c = conn.cursor()

def getUserID(BookingId):
    c.execute("SELECT UserId FROM BOOKINGS WHERE BookingId='%s'" % BookingId)
    UserIdList = [item[0] for item in c.fetchall()]
    for UserId in UserIdList:
        UserIdInt = int(UserId)
    return UserIdInt

def getEmail(UserId):
    c.execute("SELECT Email FROM USERS WHERE id='%s'" % UserId)
    emailList = [item[0] for item in c.fetchall()]
    email = ''.join(emailList)
    return email