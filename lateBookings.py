import sqlite3
import pandas as pd
from pandas import DataFrame
import datetime

def checkLateBooking():
    conn = sqlite3.connect('BOOKING.db')
    c = conn.cursor()

    c.execute('''SELECT StartTime FROM BOOKINGS''')
    startTimeList = [item[0] for item in c.fetchall()]
    BookingIdList = []
    for startTimeString in startTimeList:
        f = '%Y-%m-%d %H:%M:%S'
        startTime = datetime.datetime.strptime(startTimeString, f)
        lateHour = startTime.hour
        lateMinute = startTime.minute+15
        if(startTime.minute > 44):
            lateHour = lateHour+1
            lateMinute=lateMinute-60
        lateTime = startTime.replace(hour=lateHour, minute=lateMinute, microsecond=0)
        currentTime = datetime.datetime.now()
        if (currentTime > lateTime):
            c.execute('''SELECT BookingId FROM BOOKINGS''')
            BookingId = [item[0] for item in c.fetchall()]
            if(not BookingIdList.__contains__(1)):
                BookingIdList = BookingIdList + BookingId
    return BookingIdList
