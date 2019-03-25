import unittest
import os
from createDB import createDB
from getFromDatabase import getEmail, getUserID

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

    os.remove(databaseName)


if __name__ == '__main__':
    unittest.main()