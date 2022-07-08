import unittest
import os
import sys
import inspect

#  import a module from the parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from base import DATABASE

class TestCalculator(unittest.TestCase):
    def setUp(self):
        try:
            if os.path.isfile("data/FASTFOOD.db"):
                os.remove("data/FASTFOOD.db")
        except:
            pass

        self.object = DATABASE(
            "FASTFOOD",
            "Seyed Ali",
            "Kamali",
            "09361680099",
            "wwwwwq37@gmail.com",
            "400522148",
            "Ali@1324",
            "PROFILE",
            "FAST_FOOD",
            "Sell",
            "Iran - Tehran",
            "2022-07-08",
            "Tehran",
        )

    def test_1_Registery(self):
        value, message = self.object.Registery(
            "Ahmad Reza",
            "Zabihi",
            "09361234567",
            "ahmad@yahoo.com",
            "400522100",
            "Ahmad@123",
            "PROFILE",
        )
        self.assertTrue(value)

    def test_2_Registery_Error(self):
        value, message = self.object.Registery(
            "Ahmad Reza",
            "Zabihi",
            "09361234567",
            "ahmad@yahoo.com",
            "400522100",
            "Ahmad@123",
            "PROFILE",
        )
        self.assertFalse(value)

    def test_3_Login(self):
        value, message = self.object.Login("wwwwwq37@gmail.com", "Ali@1324")
        self.assertTrue(value)

    def test_4_Login_Error(self):
        value, message = self.object.Login("wwwwwq37@gmail.com", "00001324")
        self.assertFalse(value)

    def test_5_Person(self):
        value = self.object.Person("wwwwwq37@gmail.com")
        self.assertEqual(
            value,
            {
                "FIRST_NAME": "Seyed Ali",
                "LAST_NAME": "Kamali",
                "PHONE_NUMBER": "09361680099",
                "EMAIL": "wwwwwq37@gmail.com",
                "NATIONAL_CODE": "400522148",
                "PASSWORD": "Ali@1324",
                "PROFILE": "PROFILE",
                "FAILS": 0,
                "POSITION": "Admin",
            },
        )

    def test_6_Person_Error(self):
        value = self.object.Person("fakemail@gmail.com")
        self.assertEqual(value, None)


if __name__ == "__main__":
    unittest.main()
