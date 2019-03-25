import sqlite3
from lateBookings import checkLateBooking
from createDB import createDB
from getFromDatabase import getUserID, getEmail
from sendEmail import sendEmail

def main():
        databaseName = "BOOKING.db"
        createDB(databaseName)
    


if __name__ == '__main__':
    main()
