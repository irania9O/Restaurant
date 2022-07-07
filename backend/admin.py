from base import DATABASE
import random


class Admin(DATABASE):
    def __init__(self, returant_name, national_code):
        super().__init__(returant_name)
        self.national_code = national_code

    # -------------------------------------------------------------------------
    def NewFood(self, NAME, PRICE, INVENTORY, DATE, PROFILE, MEAL, MATERIAL):
        """
        Task:
            Insert new food into database if dosn't exist and Update price or inventory if exists.

        Arguments:
            NAME                 -- Food name                                             -- type : str        -- default : not null
            PRICE                -- Food price to sell                                    -- type : int        -- default : not null
            INVENTORY            -- Food inventory                                        -- type : int        -- default : not null
            DATE                 -- Food date YYYY-MM-DD                                  -- type : str        -- default : not null
            PROFILE              -- Food picture                                          -- type : str        -- default : not null
            MEAL                 -- BREAKFAST, LUNCH, SUPPER                              -- type : str        -- default : not null
            MATERIAL             -- Cheese|Yogurt,....                                    -- type : list       -- default : not null

        Return :
            HAS PROBLEM          --Error                                                  -- type : tuple       -- value   : False , Message
            NO  PROBLEM          --Successfully Update or insert                          -- type : tuple       -- value   : True  , Message
        """
        STRING_MEAL = "|".join(MATERIAL)
        self.c.execute(
            f"SELECT * FROM FOOD WHERE DATE = '{DATE}' AND NAME = '{NAME}' AND MEAL = '{MEAL}'"
        )
        FOOD = self.c.fetchone()
        if FOOD == None:
            try:
                # Insert new food into database
                self.c.execute(
                    f"INSERT INTO FOOD ( 'NAME', 'PROFILE',   'PRICE' , 'INVENTORY' , 'DATE', 'MEAL' , 'MATERIAL') VALUES ('{NAME}','{PROFILE}' , {PRICE} , {INVENTORY} , '{DATE}', '{MEAL}','{STRING_MEAL}' )"
                )
            except Exception as e:
                print(e)
                return False
        else:
            try:
                # Update price or inventory
                self.c.execute(
                    f"UPDATE FOOD SET INVENTORY = {INVENTORY} ,PRICE = {PRICE} ,PROFILE = '{PROFILE}',MATERIAL='{STRING_MEAL}'   WHERE DATE = '{DATE}' AND NAME = '{NAME}' AND MEAL = '{MEAL}'"
                )
            except Exception as e:
                return False, e

        self.conn.commit()
        return True

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
    def NewNews(self, SUBJECT, CONTENT, DATE, STATUS):
        """
        Task:
            Add new news to database.

        Arguments:
            SUBJECT              -- News subject                                          -- type : str        -- default : not null
            CONTENT              -- News content                                          -- type : str        -- default : not null
            DATE                 -- Food date YYYY-MM-DD                                  -- type : str        -- default : not null
            STATUS               -- 0 , 1                                                 -- type : int        -- default : not null

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
    def ChangeInfo(self, arg):
        """
        Task:
            Change Resturant info.

        Arguments:
            arg                  -- positionals arguments                                 -- type : ---         -- default : not null

        Return :
            HAS PROBLEM          --Error                                                  -- type : tuple       -- value   : False , Message
            NO  PROBLEM          --Successfully Update                                    -- type : tuple       -- value   : True  , Message
        """
        try:
            # insert
            self.c.execute("DELETE FROM INFO ")
            self.conn.commit()
        except Exception as e:
            return False, e

        try:
            # Insert new info to database
            self.c.execute(
                f"""INSERT INTO INFO( 'MANAGER_FIRST_NAME', 'MANAGER_LAST_NAME',   'PHONE_NUMBER',   'EMAIL',  'PERSON_ID' , 'PASSWORD' , 'PROFILE' , 'NAME_RESTURANT' , 'TYPE' , 'ADDRESS' , 'DATE' , 'LOCATION' ) VALUES (? ,? , ? , ?, ? ,? ,? ,? , ?, ?, ?, ?)""",
                arg,
            )
            self.conn.commit()
        except Exception as e:
            return False, e

        return True, "Successfully changed"

    # -------------------------------------------------------------------------
    def ChangeResturantDate(self, DATE):
        """
        Task:
            Change Resturant Date.

        Arguments:
            DATE                 -- Food date YYYY-MM-DD                                  -- type : str        -- default : not null

        Return :
            HAS PROBLEM          --Error                                                  -- type : tuple       -- value   : False , Message
            NO  PROBLEM          --Successfully Update                                    -- type : tuple       -- value   : True  , Message
        """
        try:
            self.c.execute(f"UPDATE INFO SET DATE = '{DATE}'")
        except Exception as e:
            return False, e
        self.conn.commit()
        return True, "Updated successfully"

    # -------------------------------------------------------------------------
    def Person(self):
        """
        Task:
            Get person account info with email or national code.

        Arguments:
            EMAIL_OR_NATIONALCODE   -- Customer or Manager National code or email            -- type : str(chr)   -- default : not null

        Return :
            HAS PROBLEM             --Error like not exist email or national code            -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully retrun                                    -- type : tuple       -- value   : True  , Message
        """
        return super().Person(self.national_code)
        
    # -------------------------------------------------------------------------
    def PayInfo(self, STATUS ,DATE):
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