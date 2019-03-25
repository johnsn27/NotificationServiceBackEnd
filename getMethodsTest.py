import unittest
import os
from createDB import createDB
from getFromDatabase import *

class TestUM(unittest.TestCase):

    databaseName = "BOOKINGTEST.db"
    createDB(databaseName)
    def setUp(self):
        pass

    def test_getEmailTest(self):
        userId = 1
        self.assertEqual(getEmail(userId), "johnsonn036@gmail.com")
    
    def test_getUserID(self):
        bookingId = 1
        self.assertEqual(getUserID(bookingId), 1)

    def test_getBookingStartTime(self):
        bookingId = 1
        self.assertEqual(getBookingStartTime(bookingId), datetime.datetime(2019, 2, 27, 10, 0))

    def test_getBookingEndTime(self):
        bookingId = 1
        self.assertEqual(getBookingEndTime(bookingId), datetime.datetime(2019, 2, 27, 11, 0))

    def test_getWatchedStartTime(self):
        roomId = 1
        userId = 1
        self.assertEqual(getWatchedStartTime(roomId, userId), datetime.datetime(2019, 2, 27, 10, 0))

    def test_getWatchedEndTime(self):
        roomId = 1
        userId = 1
        self.assertEqual(getWatchedEndTime(roomId, userId), datetime.datetime(2019, 2, 27, 11, 0))

    os.remove(databaseName)


if __name__ == '__main__':
    unittest.main()