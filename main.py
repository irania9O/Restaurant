from PyQt5.QtWidgets import QDialog, QApplication, QDesktopWidget
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import sys
from frontend.ui_class.login import LoginScreen
from frontend.ui_class.signup import SignUpScreen
from frontend.ui_class.customer import MainScreen
from frontend.ui_class.manager import  ManagerScreen

indexes = {"LoginScreen": 0, "SignUpScreen": 1, "MainScreen": 2 , "ManagerScreen": 3}

def main():
    try:
        app = QApplication(sys.argv)

        widget = QtWidgets.QStackedWidget()
        widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        widget.addWidget(LoginScreen(widget))
        widget.addWidget(SignUpScreen(widget))
        widget.addWidget(MainScreen(widget))
        widget.addWidget(ManagerScreen(widget))
        widget.setFixedHeight(500)
        widget.setFixedWidth(600)
        widget.setCurrentIndex(0)

        frameGm = widget.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos()
        )
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        widget.move(frameGm.topLeft())

        widget.offset = None

        widget.show()

        sys.exit(app.exec_())

    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()
