import unittest
import os
import sys
import inspect

#  import a module from the parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from base import DATABASE
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

        self.object = Admin("FASTFOOD", "400522148")

    def test_1_add_new_food(self):
        value = self.object.NewFood(
            "Gheymet",
            "45500",
            "100",
            "2022-07-08",
            "PROFILE",
            "BREAKFAST",
            ["gheyme", "gosht", "lape", "brenj"],
        )
        self.assertTrue(value)

    def test_2_add_new_copon(self):
        value, code = self.object.NewCopon(20, 150)  # percent  # count
        self.assertTrue(value)

    def test_3_add_new_news(self):
        value, message = self.object.NewNews(
            "New Food added.",
            "New food added menu check them now with 20% discount.",
            "2022-07-08",
            "1",
        )
        self.assertTrue(value)

    def test_4_Change_Resturant_Date(self):
        value, message = self.object.ChangeResturantDate("2022-07-08")
        self.assertTrue(value)

    def test_5_Person(self):
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
