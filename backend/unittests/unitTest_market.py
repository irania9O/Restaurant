import unittest
import os
import sys
import inspect

#  import a module from the parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from admin import Admin
from market import Market

class TestCalculator(unittest.TestCase):
    def setUp(self):
        try:
            if os.path.isfile("data/FASTFOOD.db"):
                os.remove("data/FASTFOOD.db")
        except:
            pass

        self.object = Market(
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

    def test_1_vote_info(self):
        value , data = self.object.OneVote(
            "1"
        )
        self.assertTrue(value)
        
    def test_2_info_copon(self):
        value = self.object.InfoCopon(
            self.code
        )
        self.assertTrue(value)

    def test_3_add_all_votes(self):
        value , data = self.object.AllVotes(
            "2022-07-08"
        )
        self.assertTrue(value)  

    def test_4_add_food_menu(self):
        data = self.object.FoodMenu(
            "2022-07-08"
        )
        self.assertEqual(data, [{'ID': 1, 'NAME': 'Gheymet', 'PRICE': 45500.0, 'INVENTORY': 100, 'PROFILE': 'PROFILE', 'DATE': '2022-07-08', 'MEAL': 'BREAKFAST', 'MATERIAL': 'gheyme|gosht|lape|brenj'}] )

    def test_5_add_search_food(self):
        data = self.object.SearchFood(
            "gosht"
        )
        self.assertEqual(data, [{'ID': 1, 'NAME': 'Gheymet', 'PRICE': 45500.0, 'INVENTORY': 100, 'PROFILE': 'PROFILE', 'DATE': '2022-07-08', 'MEAL': 'BREAKFAST', 'MATERIAL': 'gheyme|gosht|lape|brenj'}])

    def test_6_resturant_info(self):
        data = self.object.ResturantInfo()
        self.assertEqual(data, {'MANAGER_FIRST_NAME': 'Seyed Ali', 'MANAGER_LAST_NAME': 'Kamali', 'PHONE_NUMBER': '09361680099', 'EMAIL': 'wwwwwq37@gmail.com', 'PERSON_ID': '400522148', 'PASSWORD': 'Ali@1324', 'PROFILE': 'PROFILE', 'NAME_RESTURANT': 'FAST_FOOD', 'LOCATION': 'Tehran', 'TYPE': 'Sell', 'ADDRESS': 'Iran - Tehran', 'DATE': '2022-07-08'} )


if __name__ == "__main__":
    unittest.main()