from backend.base import DATABASE
import random

class User(DATABASE):
    def __init__(self, returant_name, national_code):
        super().__init__(returant_name)
        self.national_code = national_code

    # -------------------------------------------------------------------------
    def UseCopon(self, CODE):
        """
        Task:
            Use copon.

        Arguments:
            CODE                    -- use copon code                                     -- type : str(chr)   -- default : not null


        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully Update                                 -- type : tuple       -- value   : True  , PERCENT
        """

        self.c.execute(f"SELECT * FROM DISCOUNT WHERE CODE = '{CODE}'")
        records = self.c.fetchone()
        if records == None:
            return False, "Donst Exist"
        elif records["COUNT"] < 1:
            return False, "The code is consumed"

        try:
            # update
            self.c.execute(
                f"UPDATE DISCOUNT SET COUNT = COUNT - 1  WHERE CODE = '{CODE}'"
            )
        except Exception as e:
            return False, e

        self.conn.commit()
        return True, records["PERCENT"]

    # -------------------------------------------------------------------------
    def NewOrder(self, FOOD_ID, DATE, COUNT):
        """
        Task:
            Order new food

        Arguments:
            PERSON_ID              -- Customer or Manager National code                   -- type : str(chr)   -- default : not null
            FOOD_ID                -- Food id                                             -- type : int        -- default : not null
            DATE                   -- Date format as YYYY-MM-DD                           -- type : str        -- default : ---
            COUNT                  -- How many foods that they wants                      -- type : int        -- default : 0

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully Update ot insert                       -- type : tuple       -- value   : True  , Message
        """

        PERSON_ID = self.national_code
        try:
            # Order
            self.c.execute(
                "INSERT INTO `ORDER` ('PERSON_ID', 'FOOD_ID', 'COUNT', 'DATE','STATE') VALUES (?,?,?,?,?)",
                (PERSON_ID, FOOD_ID, COUNT, DATE, "PAYING"),
            )
        except Exception as e:
            return False, e

        self.conn.commit()
        return True, "Successfully orderd"

    # -------------------------------------------------------------------------
    def DeleteOrder(self, ORDER_ID):
        """
        Task:
            Delete Order.

        Arguments:
            PERSON_ID              -- Customer or Manager National code                   -- type : str(chr)   -- default : not null
            FOOD_ID_OR_DATE        -- Food id or Date format as YYYY-MM-DD                -- type : int|str    -- default : not null

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully Update ot insert                       -- type : tuple       -- value   : True  , Message
        """
        try:
            self.c.execute(f"DELETE FROM `ORDER` WHERE ID = {ORDER_ID}")
        except Exception as e:
            return False, e

        self.conn.commit()
        return True, "Successfully deleted"
        
    # -------------------------------------------------------------------------
    def Pay(self, SUMINCOME, DATE, Copon= ""):
        """
        Task:
            Pay Orders .

        Arguments:
            SUMINCOME              -- Total Amount                                        -- type : int         -- default : not null
            DATE                   -- Date format as YYYY-MM-DD                           -- type : str        -- default : ---
            Copon                  -- Copon Code                                          -- type : str        -- default : 0

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully                                        -- type : tuple       -- value   : True  , Message
        """
        PERSON_ID = self.national_code
        self.c.execute(
            f"SELECT * FROM `ORDER` WHERE PERSON_ID = '{PERSON_ID}' AND STATE = 'PAYING'"
        )
        records = self.c.fetchall()
        # add votes
        for data in records:
            food_id = data['FOOD_ID']
            inventory = self.FoodInfo(food_id)['INVENTORY']
            self.c.execute(
                f"UPDATE FOOD SET INVENTORY = {inventory - data['COUNT']}  WHERE ID = '{food_id}'"
            )
            
        self.c.execute(
            f"UPDATE `ORDER` SET STATE = 'SENDING' WHERE PERSON_ID = '{PERSON_ID}' AND STATE = 'PAYING'"
        )
        
        if not Copon == "":
            status, percent = self.UseCopon(Copon)

        try:
            Tracking_Code = "".join(
                random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
                for x in range(8)
            )
            # add new comment to datebase
            self.c.execute(
                "INSERT INTO ECONOMY ('SUMINCOME' , 'TRACKINGCODE', 'DATE') VALUES (?,?,?)",
                (SUMINCOME, Tracking_Code, DATE),
            )
        except Exception as e:
            return False, e
            
        self.conn.commit()
        return True, "Successfully"

    # -------------------------------------------------------------------------
    def Factor(self):
        """
        Task:
            Create Factor and Tracking Code.

        Arguments:
            PERSON_ID              -- Customer National code                              -- type : str(chr)    -- default : not null

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully                                        -- type : tuple       -- value   : [] , Tracking Code
        """
        PERSON_ID = self.national_code
        try:
            self.c.execute(
                f"SELECT * FROM `ORDER` WHERE STATE = 'PAYING' AND PERSON_ID = '{PERSON_ID}'"
            )
            records = self.c.fetchall()
            Tracking_Code = ""
            for i in records:
                Tracking_Code += str(i["FOOD_ID"]) + "/" + str(i["COUNT"]) + "|"
            return records, self.base64_encode(Tracking_Code)
        except Exception as e:
            return False, e

    # -------------------------------------------------------------------------
    def NewVote(self, FOOD_ID, COMMENT):
        """
        Task:
            Vote to a food.

        Arguments:
            PERSON_ID              -- Customer National code                              -- type : str(chr)   -- default : not null
            FOOD_ID                -- Food id                                             -- type : int        -- default : not null
            COMMENT                -- Customer comment                                    -- type : str        -- default : not null

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully Update ot insert                       -- type : tuple       -- value   : True  , Message
        """
        # person info
        PERSON_ID = self.national_code
        PERSON = self.Person(PERSON_ID)
        MESSAGE = PERSON["EMAIL"] + " : \n" + COMMENT
        self.c.execute(
            f"SELECT * FROM VOTE WHERE PERSON_ID = '{PERSON_ID}' AND FOOD_ID = '{FOOD_ID}'"
        )

        VOTE = self.c.fetchone()
        # if exists update else new comment
        if VOTE == None:
            try:
                # add new comment to datebase
                self.c.execute(
                    "INSERT INTO VOTE ('PERSON_ID', 'FOOD_ID' , 'COMMENT') VALUES (?,?,?)",
                    (PERSON_ID, FOOD_ID, MESSAGE),
                )
            except Exception as e:
                return False, e
        else:
            try:
                # update last comment
                self.c.execute(
                    f"UPDATE VOTE SET COMMENT = '{MESSAGE}'  WHERE PERSON_ID = '{PERSON_ID}' AND FOOD_ID = '{FOOD_ID}'"
                )
            except Exception as e:
                return False, e

        self.conn.commit()
        return True
