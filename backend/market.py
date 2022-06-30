from base import DATABASE
class Market(DATABASE):
    def __init__(self):
        super().__init__()
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
            return False , "No vote here"
        else:
            return True, list(records)
# -------------------------------------------------------------------------
    def InfoCopon(self, CODE):
        self.c.execute(f"SELECT * FROM DISCOUNT WHERE CODE = '{CODE}'")
        record = self.c.fetchone()
        if record == None:
            return False , "Donst Exist"

        self.conn.commit()
        return True , record  
 
# -------------------------------------------------------------------------
    def AllNews(self):
        self.c.execute(f"SELECT * FROM NEWS")
        record = self.c.fetchall()
        if record == None:
            return False , "Donst Exist"

        self.conn.commit()
        return True , record
# -------------------------------------------------------------------------
    def OnDateNews(self , DATE):
        self.c.execute(f"SELECT * FROM NEWS WHERE date(DATE) = '{DATE}'")
        record = self.c.fetchall()
        if record == None:
            return False , "Donst Exist"

        self.conn.commit()
        return True , record  
# -------------------------------------------------------------------------
    def AllVotes(self, DATE):
        """
        Task:
            Get all foods votes

        Arguments:
            DATE                    -- Date format as YYYY-MM-DD                           -- type : str        -- default : Now

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully                                        -- type : tuple       -- value   : True  , []
        """
        try:
            #Get food list
            self.c.execute(f"SELECT * FROM FOOD WHERE date(DATE) = '{DATE}' ORDER BY MEAL")
            records = self.c.fetchall()
            # add votes
            for data in records:
                data['votes'] = self.OneVote(data['ID'])
                
            return True,list(records)

        except Exception as e:
            return False, e        

# -------------------------------------------------------------------------
    def FoodMenu(self, DATE):
        """
        Task:
            Foods that exists on Date

        Arguments:
            DATE                    -- Date format as YYYY-MM-DD                           -- type : str        -- default : Now

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully Update ot insert                       -- type : lsit        -- value   : []
        """
        try:
            #Get food list
            #self.c.execute(f"SELECT ID,NAME,DATE FROM FOOD WHERE date(DATE) = '{DATE}'")
            self.c.execute(f"SELECT * FROM FOOD WHERE date(DATE) = '{DATE}' ORDER BY MEAL")
            records = self.c.fetchall()
            return list(records)

        except Exception as e:
            return False, e
# -------------------------------------------------------------------------
    def SearchFood(self, MATERIAL):
        """
        Task:
            Foods that exists on Date

        Arguments:
            DATE                    -- Date format as YYYY-MM-DD                           -- type : str        -- default : Now

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully Update ot insert                       -- type : lsit        -- value   : []
        """
        LIST = []
        for data in MATERIAL:
            LIST.append(f"MATERIAL LIKE '%{data}%' ")
        try:
            #Get food list
            self.c.execute(f"SELECT * FROM FOOD WHERE " + "AND ".join(LIST) +"ORDER BY MEAL")
            records = self.c.fetchall()
            return list(records)

        except Exception as e:
            return False, e
        
# -------------------------------------------------------------------------
    def Income(self , DATE):
        self.c.execute(f"SELECT * FROM ECONOMY WHERE date(DATE) = '{DATE}'")
        record = self.c.fetchall()
        if record == None:
            return False , "Donst Exist"

        self.conn.commit()
        return True , record  
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
            self.c.execute(f"SELECT * FROM `ORDER` WHERE STATE = 'PAYING' AND PERSON_ID = '{PERSON_ID}'")
            records = self.c.fetchall()
            return True, records
        
        except Exception as e:
            return False , e
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
            self.c.execute(f"SELECT * FROM `ORDER` WHERE STATE = 'SENDING' AND PERSON_ID = '{PERSON_ID}'")
            records = self.c.fetchall()
            return True, records
        
        except Exception as e:
            return False , e
        
    
