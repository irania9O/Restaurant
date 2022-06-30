from base import DATABASE
import random

class Admin(DATABASE):
    def __init__(self):
        super().__init__()
# -------------------------------------------------------------------------
    def NewFood(self, NAME, PRICE, INVENTORY, DATE , PROFILE , MEAL, MATERIAL):
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
            NO  PROBLEM          --Successfully Update ot insert                          -- type : tuple       -- value   : True  , Message
        """
        STRING_MEAL = "|".join(MATERIAL)
        self.c.execute(
            f"SELECT * FROM FOOD WHERE date(DATE) = '{DATE}' AND NAME = '{NAME}' AND MEAL = '{MEAL}'"
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
                    f"UPDATE FOOD SET INVENTORY = {INVENTORY} ,PRICE = {PRICE} ,PROFILE = '{PROFILE}',MATERIAL='{STRING_MEAL}'   WHERE date(DATE) = '{DATE}' AND NAME = '{NAME}' AND MEAL = '{MEAL}'"
                )
            except Exception as e:
                return False , e

        self.conn.commit()
        return True
# -------------------------------------------------------------------------
    def NewCopon(self, PERCENT, COUNT):
        CODE = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for x in range(5))
        try:
            # insert
            self.c.execute(
                "INSERT INTO `DISCOUNT` ('CODE', 'PERCENT' , 'COUNT') VALUES (?,?,?)",
                (CODE, PERCENT, COUNT),
            )
        except Exception as e:
            return False , e

        self.conn.commit()
        return True , CODE
# -------------------------------------------------------------------------
    def NewNews(self, SUBJECT, CONTENT , DATE):
        try:
            # insert
            self.c.execute(
                "INSERT INTO NEWS ('SUBJECT', 'CONTENT', 'DATE') VALUES (?,?,?)",
                (SUBJECT, CONTENT, DATE),
            )
        except Exception as e:
            return False , e

        self.conn.commit()
        return True , "Successfully added"       


