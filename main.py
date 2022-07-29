from PyQt5.QtWidgets import QDialog, QApplication, QDesktopWidget
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import sys
class LoginScreen(QDialog):
    def __init__(self, widget):
        self.widget = widget
        super(LoginScreen, self).__init__()
        loadUi("frontend/ui_files/login.ui", self)
        self.centralize()
        self.widget.setFixedHeight(500)
        self.widget.setFixedWidth(600)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)

    def centralize(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.widget.move(frameGm.topLeft())
        
    def GotoMainScreen(self):
        MainScreenNav = MainScreen(self.widget)
        self.widget.addWidget(MainScreenNav)
        self.widget.setCurrentIndex(widget.currentIndex() + 1)

    def loginfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()

        if len(user)==0 or len(password)==0:
            self.error.setText("USER PASS NOT IMPORTED DASHM")

        else:
            self.GotoMainScreen()
            
class MainScreen(QDialog):
    def __init__(self, widget):
        self.widget = widget
        super(MainScreen, self).__init__()
        loadUi("frontend/ui_files/MainScreen.ui",self)
        self.centralize()
        self.widget.setFixedHeight(800)
        self.widget.setFixedWidth(1200)
        self.back.clicked.connect(self.GoToStartScreen)

    def centralize(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.widget.move(frameGm.topLeft())
        
    def GoToStartScreen(self):
        StartScreenNav = LoginScreen(self.widget)
        self.widget.addWidget(StartScreenNav)
        self.widget.setCurrentIndex(widget.currentIndex() - 1)
        
def main():
    try:
        app = QApplication(sys.argv)

        global widget
        widget = QtWidgets.QStackedWidget()
        widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        InitScreen = LoginScreen(widget)
        widget.addWidget(InitScreen)

        widget.offset = None

        widget.show()

        sys.exit(app.exec_())

    except Exception as error:
        print(error)

if __name__ == '__main__':
   main()
