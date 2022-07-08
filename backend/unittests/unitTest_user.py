import unittest
import os
import sys
import inspect

#  import a module from the parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from base import DATABASE
from user import User
from admin import Admin

class TestCalculator(unittest.TestCase):
    def setUp(self):
        try:
            if os.path.isfile("data/FASTFOOD.db"):
                os.remove("data/FASTFOOD.db")
        except:
            pass

        DATABASE(
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
        self.object_admin = Admin(
            "FASTFOOD",
             "400522148"
        )
        self.object_admin.NewFood(
            "Gheymet",
            "45500",
            "100",
            "2022-07-08",
            "PROFILE",
            "BREAKFAST",
            ["gheyme","gosht","lape","brenj"],
        )
        value , self.code = self.object_admin.NewCopon(
            20, # percent
            150 #count
        )

        self.object = User(
            "FASTFOOD",
             "400522148"
        )

    def test_1_use_copon(self):
        value = self.object.UseCopon(
            self.code
        )
        self.assertTrue(value)
        
    def test_2_add_new_order(self):
        value , message = self.object.NewOrder(
            "1",
            "2022-07-08",
            "1"
        )
        self.assertTrue(value)

    def test_3_add_delete_order(self):
        value , message = self.object.DeleteOrder(
            "1"
        )
        self.assertTrue(value)  

    def test_4_add_create_factor(self):
        value , message = self.object.NewOrder(
            "1",
            "2022-07-08",
            "1"
        )
        data , tracking_code = self.object.Factor()
        self.assertTrue(isinstance(data,list))

    def test_5_add_Pay(self):
        data , tracking_code = self.object.Factor()
        value , message = self.object.Pay(
            tracking_code,
            "2022-07-08",
            self.code
        )
        
        self.assertTrue(value)

    def test_6_add_Pay(self):
        value  = self.object.NewVote(
            "1",
            "Very Good."
        )
        
        self.assertTrue(value)

    def test_7_Person(self):
        value = self.object.Person()
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

if __name__ == "__main__":
    unittest.main()