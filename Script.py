import sqlite3
from lateBookings import checkLateBooking
from getFromDatabase import getUserID, getEmail
from sendEmail import sendEmail

def main():
    conn = sqlite3.connect('BOOKING.db')
    c = conn.cursor()

    lateBookings = checkLateBooking()
    for BookingId in lateBookings:
        UserId = getUserID(BookingId)
        email = getEmail(UserId)
        sendEmail(email)
    


if __name__ == '__main__':
    main()
