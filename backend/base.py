import sqlite3
import base64
from data import sendemail


class DATABASE:
    def __init__(self, returant_name, *arg):

        self.conn = sqlite3.connect(
            f"data/{returant_name}.db",
            check_same_thread=False
        )  # connecting to database
        self.conn.row_factory = self.dict_factory  # to return rows in new mode
        self.c = self.conn.cursor()  # cursor

        # Create PERSON table if deos not exist in database
        self.c.execute(
            """  CREATE TABLE IF NOT EXISTS PERSON
                           (FIRST_NAME      TEXT        NOT NULL,
                            LAST_NAME       TEXT        NOT NULL,
                            PHONE_NUMBER    CHAR(20)    NOT NULL,
                            EMAIL           TEXT        NOT NULL,
                            NATIONAL_CODE   CHAR(20)    PRIMARY KEY,
                            PASSWORD        TEXT        NOT NULL,
                            PROFILE         TEXT        NOT NULL,
                            FAILS           INTEGER     NOT NULL,
                            POSITION        TEXT        NOT NULL
                            );"""
        )

        # Create FOOD table if deos not exist in database
        self.c.execute(
            """  CREATE TABLE IF NOT EXISTS FOOD
                           (ID              INTEGER     PRIMARY KEY AUTOINCREMENT ,
                            NAME            TEXT        NOT NULL,
                            PRICE           REAL        NOT NULL,
                            INVENTORY       INTEGER     NOT NULL,
                            PROFILE         TEXT        NOT NULL,
                            DATE            TEXT        NOT NULL,
                            MEAL            TEXT        NOT NULL,
                            MATERIAL        TEXT        NOT NULL
                            );"""
        )

        # Create ORDER table if deos not exist in database
        self.c.execute(
            """  CREATE TABLE IF NOT EXISTS `ORDER`
                           (ID              INTEGER     PRIMARY KEY AUTOINCREMENT ,
                            COUNT           INTEGER     NOT NULL,
                            DATE            TEXT        NOT NULL,
                            PERSON_ID       CHAR(20)    NOT NULL,
                            STATE           CHAR(20)    NOT NULL,
                            FOOD_ID         INTEGER     NOT NULL,
                            FOREIGN KEY(PERSON_ID)      REFERENCES PERSON(NATIONAL_CODE),
                            FOREIGN KEY(FOOD_ID)        REFERENCES FOOD(ID)
                            );"""
        )

        # Create VOTE table if deos not exist in database
        self.c.execute(
            """  CREATE TABLE IF NOT EXISTS VOTE
                           (ID              INTEGER     PRIMARY KEY AUTOINCREMENT ,
                            COMMENT         TEXT        NOT NULL,
                            PERSON_ID       CHAR(20)    NOT NULL,
                            FOOD_ID         INTEGER     NOT NULL,
                            FOREIGN KEY(PERSON_ID)      REFERENCES PERSON(NATIONAL_CODE),
                            FOREIGN KEY(FOOD_ID)        REFERENCES FOOD(ID)
                            );"""
        )

        # Create NEWS table if deos not exist in database
        self.c.execute(
            """  CREATE TABLE IF NOT EXISTS NEWS
                           (ID              INTEGER     PRIMARY KEY AUTOINCREMENT ,
                            SUBJECT         TEXT        NOT NULL,
                            CONTENT         TEXT        NOT NULL,
                            DATE            TEXT        NOT NULL
                            );"""
        )

        # Create DICSOUNT table if deos not exist in database
        self.c.execute(
            """  CREATE TABLE IF NOT EXISTS DISCOUNT
                           (CODE            TEXT        PRIMARY KEY  ,
                            PERCENT         INTEGER     NOT NULL,
                            COUNT           INTEGER     NOT NULL
                            );"""
        )

        # Create ECONOMY table if deos not exist in database
        self.c.execute(
            """  CREATE TABLE IF NOT EXISTS ECONOMY
                           (SUMINCOME       REAL     NOT NULL,
                            TRACKINGCODE    TEXT     PRIMARY KEY  ,
                            DATE            TEXT     NOT NULL
                            );"""
        )

        # Create INFO table if deos not exist in database
        self.c.execute(
            """  CREATE TABLE IF NOT EXISTS INFO
                           (                           
                            MANAGER_FIRST_NAME    TEXT        NOT NULL,
                            MANAGER_LAST_NAME     TEXT        NOT NULL,
                            PHONE_NUMBER          CHAR(20)    NOT NULL,
                            EMAIL                 TEXT        NOT NULL,
                            PERSON_ID             CHAR(30)    NOT NULL,
                            PASSWORD              TEXT        NOT NULL,
                            PROFILE               TEXT        NOT NULL,
                            NAME_RESTURANT        TEXT        NOT NULL,
                            LOCATION              TEXT        NOT NULL,
                            TYPE                  TEXT        NOT NULL,
                            ADDRESS               TEXT        NOT NULL,
                            DATE                  TEXT        NOT NULL, 
                            PRIMARY KEY(NAME_RESTURANT, TYPE , ADDRESS , DATE)
                            );"""
        )

        self.conn.execute(
            "PRAGMA foreign_keys = ON"
        )  # FOREIGN KEY is not supported automatically in sqlite3
        self.conn.commit()


        self.c.execute(f"SELECT * FROM INFO")
        record = self.c.fetchone()
        if record is None and not arg == tuple():
            try:
                # Insert new user to database
                self.c.execute(
                    f"""INSERT INTO INFO( 'MANAGER_FIRST_NAME', 'MANAGER_LAST_NAME',   'PHONE_NUMBER',   'EMAIL',  'PERSON_ID' , 'PASSWORD' , 'PROFILE' , 'NAME_RESTURANT' , 'TYPE' , 'ADDRESS' , 'DATE' , 'LOCATION' ) VALUES (? ,? , ? , ?, ? ,? ,? ,? , ?, ?, ?, ?)""",
                    arg,
                )
                self.conn.commit()
                self.Registery(
                    arg[0],
                    arg[1],
                    arg[2],
                    arg[3],
                    arg[4],
                    arg[5],
                    arg[6],
                    0,
                    "Admin",
                )

            except Exception as e:
                print(e)
                pass

    # -------------------------------------------------------------------------
    def base64_encode(self, message):
        message_bytes = message.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode("ascii")
        return base64_message

    # -------------------------------------------------------------------------
    def base64_decode(self, base64_message):
        base64_bytes = base64_message.encode("ascii")
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode("ascii")
        return message

    # -------------------------------------------------------------------------
    def dict_factory(self, cursor, row):
        """
        Task:
            Convert sql row data to dictionary

        Arguments:
            FIRST_NAME      -- Customer or Manager first name     -- type : sqlite3.Cursor     -- default : not null
            LAST_NAME       -- Customer or Manager last name      -- type : tuple              -- default : not null

        Return :
            dictionary      -- All rows info in new format        -- type : dict               -- value   : dictonary
        """
        dictionary = {}
        for index, column in enumerate(cursor.description):
            dictionary[column[0]] = row[index]
        return dictionary

    # -------------------------------------------------------------------------
    def Registery(
        self,
        FIRST_NAME,
        LAST_NAME,
        PHONE_NUMBER,
        EMAIL,
        NATIONAL_CODE,
        PASSWORD,
        PROFILE,
        FAILS=0,
        POSITION="Customer",
    ):
        """
        Task:
            Registery New Account.

        Arguments:
            FIRST_NAME      -- Customer or Manager first name     -- type : str        -- default : not null
            LAST_NAME       -- Customer or Manager last name      -- type : str        -- default : not null
            PHONE_NUMBER    -- Customer or Manager phone number   -- type : str(chr)   -- default : not null
            EMAIL           -- Customer or Manager EMAIL          -- type : str        -- default : not null
            NATIONAL_CODE   -- Customer or Manager National code  -- type : str(chr)   -- default : not null
            PASSWORD        -- Customer or Manager password       -- type : str        -- default : not null
            PROFILE         -- Customer or Manager profile path   -- type : str        -- default : not null
            FAILS           -- Customer or Manager FAILS          -- type : int        -- default : 0
            POSITION        -- User if Customer or Manager        -- type : str(chr)   -- default : Customer

        Return :
            HAS PROBLEM     --Error like existing NATIONAL_CODE   -- type : bool       -- value   : False , Message
            NO  PROBLEM     --Successfully Registery              -- type : bool       -- value   : True  , Message
        """

        try:
            # Insert new user to database
            self.c.execute(
                f"""INSERT INTO PERSON
                           ( 'FIRST_NAME',   'LAST_NAME',   'PHONE_NUMBER',  'EMAIL',    'NATIONAL_CODE',   'PASSWORD',   'PROFILE',  'FAILS',    'POSITION') VALUES
                           ('{FIRST_NAME}', '{LAST_NAME}', '{PHONE_NUMBER}', '{EMAIL}', '{NATIONAL_CODE}', '{PASSWORD}', '{PROFILE}', '{FAILS}', '{POSITION}')"""
            )
            self.conn.commit()
            return True, "Account created successfully"

        except Exception as e:
            return False, e

    # -------------------------------------------------------------------------
    def Login(self, EMAIL_OR_NATIONALCODE, PASSWORD):
        """
        Task:
            Login To Account.

        Arguments:
            EMAIL_OR_NATIONALCODE   -- Customer or Manager National code or email for login  -- type : str(chr)   -- default : not null
            PASSWORD                -- Customer or Manager password                          -- type : str        -- default : not null

        Return :
            HAS PROBLEM             --Error like existing wrong password                     -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully login                                     -- type : tuple       -- value   : True  , Message
        """

        # Get account info using Person method
        records = self.Person(EMAIL_OR_NATIONALCODE)

        # Couldn't find any data
        if records is None:
            return False, "NATIONAL_CODE OR EMAIL DOES NOT EXIST IN DATABASE"

        elif not records["PASSWORD"] == PASSWORD:
            # Another error was recorded
            self.Update(
                NATIONAL_CODE=records["NATIONAL_CODE"], FAILS=records["FAILS"] + 1
            )

            # SEND EMAIL
            if records["FAILS"] + 1 > 2:
                sendemail.Email().send_email(
                    "Restaurant ",
                    records["EMAIL"],
                    "Recover Password",
                    f"Your password is {records['PASSWORD']}",
                )
                return False, "You tried more than three times wrong"
                pass

            return False, "Wrong Password"

        elif records["PASSWORD"] == PASSWORD:
            # logged in successfully
            self.Update(NATIONAL_CODE=records["NATIONAL_CODE"], FAILS=0)
            return True, records["POSITION"]

    # -------------------------------------------------------------------------
    def Person(self, EMAIL_OR_NATIONALCODE):
        """
        Task:
            Get person account info with email or national code.

        Arguments:
            EMAIL_OR_NATIONALCODE   -- Customer or Manager National code or email            -- type : str(chr)   -- default : not null

        Return :
            HAS PROBLEM             --Error like not exist email or national code            -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully retrun                                    -- type : tuple       -- value   : True  , Message
        """

        self.c.execute(
            f"SELECT * FROM PERSON WHERE EMAIL = '{EMAIL_OR_NATIONALCODE}' OR NATIONAL_CODE = '{EMAIL_OR_NATIONALCODE}'"
        )  # select data from data base to get a person account info
        records = self.c.fetchone()
        return records

    # -------------------------------------------------------------------------
    def Update(self, *arg, **kwargs):
        """
        Task:
            Update person account info with email or national code.

        Arguments:
            kwargs                  -- get all kwargs as a dict                              -- type : dict        -- default : {}

        Return :
            HAS PROBLEM             --Error like not exist email or national code            -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully Update                                    -- type : tuple       -- value   : True  , Message
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
                    "UPDATE PERSON SET "
                    + ",".join(LIST)
                    + f" WHERE NATIONAL_CODE= \'{kwargs['NATIONAL_CODE']}\'"
                )
            except Exception as e:
                return False, e

            self.conn.commit()
            return True, "Updated successfully"

        else:
            return False, "Just kwargs acceptable"

    # -------------------------------------------------------------------------
    def AllNews(self):
        """
        Task:
            Get all news.

        Arguments:
            ---

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully                                        -- type : tuple       -- value   : True  , []
        """
        self.c.execute(f"SELECT * FROM NEWS")
        record = self.c.fetchall()
        if record == None:
            return False, "Donst Exist"

        self.conn.commit()
        return True, record

    # -------------------------------------------------------------------------
    def OnDateNews(self, DATE):
        """
        Task:
            Get one day news.

        Arguments:
            DATE                 -- Food date YYYY-MM-DD                                  -- type : str        -- default : not null

        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully                                        -- type : tuple       -- value   : True  , []
        """
        self.c.execute(f"SELECT * FROM NEWS WHERE DATE = '{DATE}'")
        record = self.c.fetchall()
        if record == None:
            return False, "Donst Exist"

        self.conn.commit()
        return True, record

