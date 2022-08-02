from PyQt5.QtWidgets import QDialog, QApplication, QDesktopWidget
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import re 

class SignUpScreen(QDialog):
    def __init__(self, widget):
        super(SignUpScreen, self).__init__()
        self.widget_pages = widget
        loadUi("frontend/ui_files/signup.ui", self)
        self.centralize()
        self.login.clicked.connect(self.GoToLoginScreen)
        self.signup.clicked.connect(self.signupfunction)
        self.exit_button.clicked.connect(lambda x : QtCore.QCoreApplication.quit())

    def centralize(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos()
        )
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.widget_pages.move(frameGm.topLeft())
        
    def signupfunction(self):
        firstname = self.firstname.text()
        lastname = self.lastname.text()
        phonenumber = self.phonenumber.text()
        email = self.email.text()
        nationacode = self.nationacode.text()
        password = self.password.text()
        password_2 = self.password2.text()

        if len(firstname) == 0 or len(lastname) == 0 or len(phonenumber) == 0 or len(email) == 0 or len(email) == 0 or len(nationacode) == 0 or len(password) == 0 or len(password_2) == 0:
            self.error.setText("ONE FILED NOT IMPORTED")
            return False
        elif not re.search(r'(0|\+98|0098)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}', phonenumber):
            self.error.setText("Invalid Phone Number")
            return False
        
        elif not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            self.error.setText("Invalid Email")
            return False
        
        elif not re.search(r'^\d{10}$', nationacode):
            self.error.setText("Invalid National Code")
            return False
        
        elif not re.search(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", password):
            self.error.setText("8 characters, at least 1 letter, 1 number & 1 special character")
            return False


        
        else:
            self.error.setText("")
            self.firstname.setText("")
            self.lastname.setText("")
            self.phonenumber.setText("")
            self.email.setText("")
            self.nationacode.setText("")
            self.password.setText("")
            self.password2.setText("")
            self.GoToLoginScreen()
            
    def GoToLoginScreen(self):
        self.error.setText("")
        self.firstname.setText("")
        self.lastname.setText("")
        self.phonenumber.setText("")
        self.email.setText("")
        self.nationacode.setText("")
        self.password.setText("")
        self.password2.setText("")
        self.widget_pages.setFixedHeight(500)
        self.widget_pages.setFixedWidth(600)
        self.widget_pages.setCurrentIndex(0)
        self.centralize()
