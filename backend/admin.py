from backend.base import DATABASE
import random


class Admin(DATABASE):
    def __init__(self, returant_name, national_code):
        super().__init__(returant_name)
        self.national_code = national_code

    # -------------------------------------------------------------------------
    def NewFood(self, NAME, PRICE, INVENTORY, DATE, PROFILE, MEAL, MATERIAL):
        """
        Task:
            Insert new food into database.

        Arguments:
            NAME                 -- Food name                                             -- type : str        -- default : not null
            PRICE                -- Food price to sell                                    -- type : int        -- default : not null
            INVENTORY            -- Food inventory                                        -- type : int        -- default : not null
            DATE                 -- Food date YYYY-MM-DD                                  -- type : str        -- default : not null
            PROFILE              -- Food picture                                          -- type : str        -- default : not null
            MEAL                 -- FOOD, DRINK                                           -- type : str        -- default : not null
            MATERIAL             -- Cheese|Yogurt,....                                    -- type : list       -- default : not null

        Return :
            HAS PROBLEM          --Error                                                  -- type : tuple       -- value   : False , Message
            NO  PROBLEM          --Successfully Update or insert                          -- type : tuple       -- value   : True  , Message
        """
        STRING_MEAL = "|".join(MATERIAL)
        try:
            # Insert new food into database
            self.c.execute(
                f"INSERT INTO FOOD ( 'NAME', 'PROFILE',   'PRICE' , 'INVENTORY' , 'DATE', 'MEAL' , 'MATERIAL') VALUES ('{NAME}','{PROFILE}' , {PRICE} , {INVENTORY} , '{DATE}', '{MEAL}','{STRING_MEAL}' )"
            )
        except Exception as e:
            print(e)
            return False


        self.conn.commit()
        return True
    # -------------------------------------------------------------------------
    def UpdateFood(self, ID, NAME, PRICE, INVENTORY, MATERIAL):
        """
        Task:
            Insert new food into database if dosn't exist and Update price or inventory if exists.

        Arguments:
            ID                   -- Food ID                                               -- type : int        -- default : not null
            NAME                 -- Food name                                             -- type : str        -- default : not null
            PRICE                -- Food price to sell                                    -- type : int        -- default : not null
            INVENTORY            -- Food inventory                                        -- type : int        -- default : not null
            PROFILE              -- Food picture                                          -- type : str        -- default : not null
            MATERIAL             -- Cheese|Yogurt,....                                    -- type : list       -- default : not null

        Return :
            HAS PROBLEM          --Error                                                  -- type : tuple       -- value   : False , Message
            NO  PROBLEM          --Successfully Update or insert                          -- type : tuple       -- value   : True  , Message
        """
        STRING_MEAL = "|".join(MATERIAL)
        try:
            # Update price or inventory
            self.c.execute(
                f"UPDATE FOOD SET NAME = '{NAME}', INVENTORY = {INVENTORY}, PRICE = {PRICE}, MATERIAL='{STRING_MEAL}' WHERE ID = '{ID}'"
            )
        except Exception as e:
            return False, e

        self.conn.commit()
        return True
    # -------------------------------------------------------------------------
    def DeleteFoodDrink(self, ID):
        """
        Task:
            Delete food or drink.

        Arguments:
            ID                      -- Food ID                                            -- type : int         -- default : not null

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully Update ot insert                       -- type : tuple       -- value   : True  , Message
        """
        try:
            self.c.execute(f"DELETE FROM `FOOD` WHERE ID = {ID}")
        except Exception as e:
            return False, e

        self.conn.commit()
        return True, "Successfully deleted"
        
    # -------------------------------------------------------------------------
    def NewCopon(self, PERCENT, COUNT):
        """
        Task:
            Generate new copon.

        Arguments:
            PERCENT              -- Discount percent                                      -- type : str        -- default : not null
            COUNT                -- How many times can use code                           -- type : int        -- default : not null

        Return :
            HAS PROBLEM          --Error                                                  -- type : tuple       -- value   : False , Message
            NO  PROBLEM          --Successfully generate                                  -- type : tuple       -- value   : True  , Code
        """
        CODE = "".join(
            random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
            for x in range(5)
        )
        try:
            # insert
            self.c.execute(
                "INSERT INTO `DISCOUNT` ('CODE', 'PERCENT' , 'COUNT') VALUES (?,?,?)",
                (CODE, PERCENT, COUNT),
            )
        except Exception as e:
            return False, e

        self.conn.commit()
        return True, CODE

    # -------------------------------------------------------------------------
    def NewNews(self, SUBJECT, CONTENT, DATE, STATUS = "PUBLISH"):
        """
        Task:
            Add new news to database.

        Arguments:
            SUBJECT              -- News subject                                          -- type : str        -- default : not null
            CONTENT              -- News content                                          -- type : str        -- default : not null
            DATE                 -- Food date YYYY-MM-DD                                  -- type : str        -- default : not null
            STATUS               -- PUBLISH , DRAFT                                       -- type : int        -- default : not null

        Return :
            HAS PROBLEM          --Error                                                  -- type : tuple       -- value   : False , Message
            NO  PROBLEM          --Successfully insert                                    -- type : tuple       -- value   : True  , Message
        """
        try:
            # insert
            self.c.execute(
                "INSERT INTO NEWS ('SUBJECT', 'CONTENT', 'DATE','STATUS') VALUES (?,?,?,?)",
                (SUBJECT, CONTENT, DATE, STATUS),
            )
        except Exception as e:
            return False, e

        self.conn.commit()
        return True, "Successfully added"

    # -------------------------------------------------------------------------
    def ChangeInfo(self, *arg, **kwargs):
        """
        Task:
            Change Resturant info.

        Arguments:
            arg                  -- positionals arguments                                 -- type : ---         -- default : not null

        Return :
            HAS PROBLEM          --Error                                                  -- type : tuple       -- value   : False , Message
            NO  PROBLEM          --Successfully Update                                    -- type : tuple       -- value   : True  , Message
        """
        # Chceking not enter any positional arguments
        if arg == tuple():
            # Create key value pairs as format sqlite3 and convert to string
            # using join method
            LIST = []
            for key, value in kwargs.items():
                LIST.append(f" `{key}` = '{value}' ")
            try:
                # Update person table
                self.c.execute(
                    "UPDATE INFO SET "
                    + ",".join(LIST)
                )
            except Exception as e:
                return False, e

            self.conn.commit()
            return True, "Updated successfully"

        else:
            return False, "Just kwargs acceptable"

    # -------------------------------------------------------------------------
    def AdminsList(self):
        """
        Task:
            Get all admins account info.

        Arguments:
            --
            
        Return :
            HAS PROBLEM             --Error like not exist email or national code            -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully retrun                                    -- type : tuple       -- value   : True  , Message
        """

        self.c.execute(
            f"SELECT * FROM PERSON WHERE POSITION = 'Admin'"
        )  # select data from database to get a persons account infos
        records = self.c.fetchall()
        return records

    # -------------------------------------------------------------------------
    def PayInfo(self, STATUS, DATE):
        """
        Task:
            Pay Info .

        Arguments:
            STATUS                  -- SENDING , PAYING                                   -- type : str(chr)    -- default : not null
            DATE                    -- Food date YYYY-MM-DD                               -- type : str        -- default : not null

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully                                        -- type : tuple       -- value   : True  , []
        """

        try:
            self.c.execute(
                f"SELECT * FROM `ORDER` WHERE STATE = '{STATUS}' AND DATE = '{DATE}' ORDER BY ID DESC"
            )
            records = self.c.fetchall()
            # add votes
            for data in records:
                data["info"] = self.FoodInfo(data["FOOD_ID"])

            return True, records

        except Exception as e:
            return False, e
