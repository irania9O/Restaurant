from backend.base import DATABASE


class Market(DATABASE):
    def __init__(self, returant_name, *arg):
        super().__init__(returant_name, *arg)

    # -------------------------------------------------------------------------
    def OneVote(self, FOOD_ID):
        """
        Task:
            Get one food votes

        Arguments:
            FOOD_ID                -- Food id                                             -- type : int        -- default : not null

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully                                        -- type : tuple       -- value   : True  , []
        """

        self.c.execute(f"SELECT * FROM VOTE WHERE  FOOD_ID = '{FOOD_ID}'")
        records = self.c.fetchall()
        if records == None:
            return False, "No vote here"
        else:
            return True, list(records)

    # -------------------------------------------------------------------------
    def InfoCopon(self, CODE):
        """
        Task:
            Get Copon code details.

        Arguments:
            CODE                    -- Copon code                                         -- type : str        -- default : not null

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully                                        -- type : tuple       -- value   : True  , {}
        """
        self.c.execute(f"SELECT * FROM DISCOUNT WHERE CODE = '{CODE}'")
        record = self.c.fetchone()
        if record == None:
            return False, "Donst Exist"

        self.conn.commit()
        return True, record

    # -------------------------------------------------------------------------
    def AllVotes(self, DATE):
        """
        Task:
            Get all foods votes

        Arguments:
            DATE                    -- Date format as YYYY-MM-DD                           -- type : str        -- default : ---

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully                                        -- type : tuple       -- value   : True  , []
        """
        try:
            # Get food list
            self.c.execute(f"SELECT * FROM FOOD WHERE DATE = '{DATE}' ORDER BY MEAL")
            records = self.c.fetchall()
            # add votes
            for data in records:
                data["votes"] = self.OneVote(data["ID"])

            return True, list(records)

        except Exception as e:
            return False, e
           
    # -------------------------------------------------------------------------
    def FoodMenu(self, DATE):
        """
        Task:
            Foods that exists on Date

        Arguments:
            DATE                    -- Date format as YYYY-MM-DD                           -- type : str        -- default : ---

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully Update ot insert                       -- type : lsit        -- value   : []
        """
        try:
            # Get food list
            # self.c.execute(f"SELECT ID,NAME,DATE FROM FOOD WHERE DATE = '{DATE}'")
            self.c.execute(f"SELECT * FROM FOOD WHERE DATE = '{DATE}' AND MEAL = 'food'")
            records = self.c.fetchall()
            return list(records)

        except Exception as e:
            return False, e
            
    # -------------------------------------------------------------------------

    def DrinkMenu(self, DATE):
        """
        Task:
            Drinks that exists on Date

        Arguments:
            DATE                    -- Date format as YYYY-MM-DD                           -- type : str        -- default : ---

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully Update ot insert                       -- type : lsit        -- value   : []
        """
        try:
            # Get drink list
            # self.c.execute(f"SELECT ID,NAME,DATE FROM FOOD WHERE DATE = '{DATE}'")
            self.c.execute(f"SELECT * FROM FOOD WHERE DATE = '{DATE}' AND MEAL = 'drink'")
            records = self.c.fetchall()
            return list(records)

        except Exception as e:
            return False, e
    # -------------------------------------------------------------------------
    def SearchFood(self, data , date):
        """
        Task:
            Search Foods

        Arguments:
            DATE                    -- Date format as YYYY-MM-DD                           -- type : str        -- default : ---

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully Update ot insert                       -- type : lsit        -- value   : []
        """
        #LIST = []
        #for data in MATERIAL:
        #    LIST.append(f"MATERIAL LIKE '%{data}%' ")
        try:
            # Get food list
            self.c.execute(
            #    f"SELECT * FROM FOOD WHERE " + "AND ".join(LIST) + "OR NAME LIKE '%{MATERIAL}%'"
                 f"SELECT * FROM FOOD WHERE (MATERIAL LIKE '%{data}%' OR NAME LIKE '%{data}%') AND MEAL = 'food' AND DATE = '{date}'"
            )
            records = self.c.fetchall()
            return list(records)

        except Exception as e:
            return False, e
            
    # -------------------------------------------------------------------------
    def SearchDrinks(self, data , date):
        """
        Task:
            Search Drinks

        Arguments:
            DATE                    -- Date format as YYYY-MM-DD                           -- type : str        -- default : ---

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully Update ot insert                       -- type : lsit        -- value   : []
        """
        #LIST = []
        #for data in MATERIAL:
        #    LIST.append(f"MATERIAL LIKE '%{data}%' ")
        try:
            # Get food list
            self.c.execute(
            #    f"SELECT * FROM FOOD WHERE " + "AND ".join(LIST) + "OR NAME LIKE '%{MATERIAL}%'"
                 f"SELECT * FROM FOOD WHERE (MATERIAL LIKE '%{data}%' OR NAME LIKE '%{data}%') AND MEAL = 'drink' AND DATE = '{date}'"
            )
            records = self.c.fetchall()
            return list(records)

        except Exception as e:
            return False, e

    # -------------------------------------------------------------------------
    def Income(self, DATE):
        """
        Task:
            Get incomes .

        Arguments:
            DATE                    -- Date format as YYYY-MM-DD                           -- type : str        -- default : ---

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully                                        -- type : tuple       -- value   : True  , []
        """
        self.c.execute(f"SELECT * FROM ECONOMY WHERE DATE = '{DATE}'")
        record = self.c.fetchall()
        if record == None:
            return False, "Donst Exist"

        self.conn.commit()
        return True, record

    # -------------------------------------------------------------------------
    def PayingOrders(self, PERSON_ID):
        """
        Task:
            Pay Orders .

        Arguments:
            PERSON_ID              -- Customer National code                              -- type : str(chr)    -- default : not null

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully                                        -- type : tuple       -- value   : True  , []
        """

        try:
            self.c.execute(
                f"SELECT * FROM `ORDER` WHERE STATE = 'PAYING' AND PERSON_ID = '{PERSON_ID}'"
            )
            records = self.c.fetchall()
            # add votes
            for data in records:
                data["info"] = self.FoodInfo(data["FOOD_ID"])

            return True, records

        except Exception as e:
            return False, e

    # -------------------------------------------------------------------------
    def PayedOrders(self, PERSON_ID):
        """
        Task:
            Pay Orders .

        Arguments:
            PERSON_ID              -- Customer National code                              -- type : str(chr)    -- default : not null

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully                                        -- type : tuple       -- value   : True  , []
        """

        try:
            self.c.execute(
                f"SELECT * FROM `ORDER` WHERE STATE = 'SENDING' AND PERSON_ID = '{PERSON_ID}'"
            )
            records = self.c.fetchall()
            # add votes
            for data in records:
                data["info"] = self.FoodInfo(data["FOOD_ID"])
            return True, records

        except Exception as e:
            return False, e

    # -------------------------------------------------------------------------
    def AllOrders(self, DATE):
        """
        Task:
            All Orders .

        Arguments:
            DATE                    -- Date format as YYYY-MM-DD                           -- type : str        -- default : ---

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully                                        -- type : tuple       -- value   : True  , []
        """

        try:
            self.c.execute(
                f"SELECT * FROM `ORDER` WHERE DATE = '{DATE}'"
            )
            records = self.c.fetchall()
            # add votes
            for data in records:
                data["info"] = self.FoodInfo(data["FOOD_ID"])
            return True, records

        except Exception as e:
            return False, e
            
    # -------------------------------------------------------------------------
    def ResturantInfo(self):
        """
        Task:
            Get Resturant info.

        Arguments:
            ---

        Return :
            HAS PROBLEM          --Error                                                  -- type : tuple       -- value   : False , Message
            NO  PROBLEM          --Successfully                                           -- type : list        -- value   : []
        """
        try:
            self.c.execute(f"SELECT * FROM INFO")
            record = self.c.fetchone()
            return record
        except Exception as e:
            return False, e
