from PyQt5.QtWidgets import QDialog, QApplication, QDesktopWidget , QSpinBox 
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi


class MainScreen(QDialog):
    def __init__(self, widget):
        self.widget = widget
        super(MainScreen, self).__init__()
        loadUi("frontend/ui_files/MainScreen.ui", self)
        self.tabWidget.setCurrentIndex(0)
        #self.back.clicked.connect(self.GoToLoginScreen)
        self.exit_button.clicked.connect(lambda x : QtCore.QCoreApplication.quit())

        pixmap = QtGui.QPixmap("frontend/icons/drinks.png").scaled(300, 100)
        self.drinks.setPixmap(pixmap)

        self.cocke_regular.stateChanged.connect(lambda x : self.changer_spin_box(self.cocke_regular.objectName()))
        self.pepsi_regular.stateChanged.connect(lambda x : self.changer_spin_box(self.pepsi_regular.objectName()))
        self.sprite_regular.stateChanged.connect(lambda x : self.changer_spin_box(self.sprite_regular.objectName()))
        self.string_regular.stateChanged.connect(lambda x : self.changer_spin_box(self.string_regular.objectName()))
        self.coke_1_5.stateChanged.connect(lambda x : self.changer_spin_box(self.coke_1_5.objectName()))
        self.pepsi_1_5.stateChanged.connect(lambda x : self.changer_spin_box(self.pepsi_1_5.objectName()))
        self.sprite_1_5.stateChanged.connect(lambda x : self.changer_spin_box(self.sprite_1_5.objectName()))
        self.string_1_5.stateChanged.connect(lambda x : self.changer_spin_box(self.string_1_5.objectName()))
        self.cups.stateChanged.connect(lambda x : self.changer_spin_box(self.cups.objectName()))

    def changer_spin_box(self , name):
        counter_drinks = self.findChild(QSpinBox, f"{name}_count")
        if counter_drinks.isEnabled() :
            counter_drinks.setDisabled(True)
            counter_drinks.setValue(0)
        else:
            counter_drinks.setDisabled(False)
            counter_drinks.setValue(1)
            
        
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
