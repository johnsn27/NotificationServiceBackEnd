import sqlite3
import pandas as pd
import datetime
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

def getBookingStartTime(BookingId):
    c.execute("SELECT StartTime FROM BOOKINGS WHERE BookingId='%s'" % BookingId)
    bookingStartTimeList = [item[0] for item in c.fetchall()]
    for bookingStartTimeString in bookingStartTimeList:
       f = '%Y-%m-%d %H:%M:%S'
       BookingStartTime = datetime.datetime.strptime(bookingStartTimeString, f)
       return BookingStartTime

def getBookingEndTime(BookingId):
    c.execute("SELECT EndTime FROM BOOKINGS WHERE BookingId='%s'" % BookingId)
    bookingEndTimeList = [item[0] for item in c.fetchall()]
    for bookingEndTimeString in bookingEndTimeList:
       f = '%Y-%m-%d %H:%M:%S'
       BookingEndTime = datetime.datetime.strptime(bookingEndTimeString, f)
       return BookingEndTime

def getWatchedStartTime(RoomId, UserId):
    c.execute("SELECT StartTime FROM WATCHED WHERE RoomId='%s' AND UserId='%s'" % (RoomId, UserId))
    WatchedStartTimeList = [item[0] for item in c.fetchall()]
    for WatchedStartTimeString in WatchedStartTimeList:
        f = '%Y-%m-%d %H:%M:%S'
        WatchedStartTime = datetime.datetime.strptime(WatchedStartTimeString, f)
        return WatchedStartTime

def getWatchedEndTime(RoomId, UserId):
    c.execute("SELECT EndTime FROM WATCHED WHERE RoomId='%s' AND UserId='%s'" % (RoomId, UserId))
    WatchedEndTimeList = [item[0] for item in c.fetchall()]
    for WatchedEndTimeString in WatchedEndTimeList:
        f = '%Y-%m-%d %H:%M:%S'
        WatchedEndTime = datetime.datetime.strptime(WatchedEndTimeString, f)
        return WatchedEndTime