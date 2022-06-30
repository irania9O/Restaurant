import smtplib
from email.message import EmailMessage

class Email:
    
    def __init__(self):
        """ Initialize prerequisites"""
        self.server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        self.server.ehlo()
        self.server.starttls()
        self.server.login('mangerestaurantap1401@gmail.com', 'mthkhowoduosbpad')
        


    def send_email(self , from_name , to_email , subject , content):
        """
        Task:
            Send Email.

        Arguments:
            from_name              -- The name that will be displayed to the user, Ex: Moon Restaurant         -- type : str
            to_email               -- Recipient email address                                                  -- type : str        
            DATE                   -- Email Subject                                                            -- type : str   
            COUNT                  -- Email content , Ex : You password is 0000@ABC                            -- type : str            
            
        Return :
            HAS PROBLEM             --Error                                               -- type : tuple       -- value   : False , Message
            NO  PROBLEM             --Successfully                                        -- type : tuple       -- value   : True  , Message
        """
        try:
            email = EmailMessage()
            email['from'] = from_name
            email['to'] = to_email
            email['subject'] = subject
            email.set_content(content)
            self.server.send_message(email)
            return True , 'Email was sent!'
            
        except Exception as e:
            return False , e


# Example :
# print(Email().send_email("ali python ", "wwwwwq37@gmail.com", "Recover Password", "Password"))
