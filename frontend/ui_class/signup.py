from PyQt5.QtWidgets import QDialog, QApplication, QDesktopWidget
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi


class SignUpScreen(QDialog):
    def __init__(self, widget):
        self.widget = widget
        super(SignUpScreen, self).__init__()
        loadUi("frontend/ui_files/signup.ui", self)
        self.centralize()
        self.login.clicked.connect(self.GoToLoginScreen)
        self.exit_button.clicked.connect(lambda x: self.widget.close())

    def centralize(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos()
        )
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.widget.move(frameGm.topLeft())

    def GoToLoginScreen(self):
        self.widget.setFixedHeight(500)
        self.widget.setFixedWidth(600)
        self.widget.setCurrentIndex(0)
        self.centralize()
