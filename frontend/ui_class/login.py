from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit
from PyQt5.uic import loadUi
import sys


class LoginScreen(QDialog):
    def __init__(self, widget, admin, market, user):
        super(LoginScreen, self).__init__()
        self.widget_pages = widget
        self.admin = admin
        self.market = market
        self.user = user

        loadUi("frontend/ui_files/LoginScreen.ui", self)
        self.centralize()
        self.exit_button.clicked.connect(lambda x: sys.exit())
        self.signup.clicked.connect(self.GotoSignUpScreen)
        self.login.clicked.connect(self.loginfunction)

        # icon  = QtGui.QIcon('CC.png')
        # self.b_login.setIconSize(QtCore.QSize(200,200))
        # self.b_login.setIcon(icon)
        self.show_hide_password.stateChanged.connect(self.show_hide_pass)

    # A Method for checkbox to show or hide password.
    def show_hide_pass(self):
        if self.password.echoMode() == 0:
            self.password.setEchoMode(QLineEdit.Password)
        else:
            self.password.setEchoMode(QLineEdit.Normal)

    def centralize(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos()
        )
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.widget_pages.move(frameGm.topLeft())

    def GotoMainScreen(self):
        self.widget_pages.setFixedHeight(800)
        self.widget_pages.setFixedWidth(1200)
        self.widget_pages.setCurrentIndex(2)
        self.centralize()

    def loginfunction(self):
        user = self.username.text()
        password = self.password.text()

        if len(user) == 0 or len(password) == 0:
            ##elf.database[0].national_code = "22"
            ##print(self.database[0].national_code)
            ##print(self.database)
            self.error.setText("USER OR PASSWORD NOT IMPORTED")

        else:
            status, msg = self.user.Login(user, password)
            if status == True:
                self.admin.national_code = msg
                self.market.national_code = msg
                self.user.national_code = msg
                try:
                    self.widget_pages.widget(2).check_admin()
                except Exception as e:
                    print(e)
                self.error.setText("")
                self.username.setText("")
                self.password.setText("")
                self.GotoMainScreen()
            else:
                self.error.setText(msg)

    def GotoSignUpScreen(self):
        self.error.setText("")
        self.username.setText("")
        self.password.setText("")
        self.widget_pages.setFixedHeight(750)
        self.widget_pages.setFixedWidth(600)
        self.widget_pages.setCurrentIndex(1)
        self.centralize()
