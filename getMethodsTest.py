import unittest
import sys
sys.path.insert(0, '/Users/johnsn27/Documents/Uni/NotificationServiceBackEnd')
from getFromDatabase import getEmail, getUserID

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_getEmailTest(self):
        userId = 1
        self.assertEqual(getEmail(userId), "johnsonn036@gmail.com")
    
    def test_getUserID(self):
        bookingId = 1
        self.assertEqual(getUserID(bookingId), 1)



if __name__ == '__main__':
    unittest.main()