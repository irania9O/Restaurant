from PyQt5.QtWidgets import QDialog, QApplication, QDesktopWidget, QFrame, QSpinBox , QCheckBox , QLabel, QLineEdit , QFormLayout
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

        pixmap = QtGui.QPixmap("frontend/icons/foods.png").scaled(300, 100)
        self.foods.setPixmap(pixmap)
        
        pixmap = QtGui.QPixmap("frontend/icons/factor.png").scaled(300, 100)
        self.factor.setPixmap(pixmap)        

        #print(self.lcdNumber.intValue())
        #self.lcdNumber.display(150)
        #print(self.lcdNumber.intValue())
        self.search_food.textChanged.connect(self.doSomething)
        self.search_drink.textChanged.connect(self.doSomething)
        
        self.calendarWidget.setMinimumDate(self.calendarWidget.selectedDate())
        self.calendarWidget.selectionChanged.connect(self.update_foods)
        self.update_foods()
        
        self.foods_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.foods_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        self.drinks_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.drinks_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
    def doSomething(self):
        print(0)
        
    def enable_disable_spin_box(self , name):
        counter_drinks = self.findChild(QSpinBox, f"{self.sender().objectName()}_count")
        if counter_drinks.isEnabled() :
            counter_drinks.setDisabled(True)
            counter_drinks.setValue(0)
        else:
            counter_drinks.setDisabled(False)
            counter_drinks.setValue(1)

    def change_spin_box(self , value):
        spin_box = self.sender()         
        print(spin_box)
        print(value)

    def update_foods(self):
        print(self.calendarWidget.selectedDate().toString("yyyy-MM-dd"))
        
        formFrameFoods = QFrame()
        self.layout_foods = QFormLayout(formFrameFoods)
        self.foods_area.setWidget(formFrameFoods)
        
        for i in range(5):
            checkbox = QCheckBox(f"food{i} \t {i*10}$", self, objectName = f"food{i}") 
            checkbox.setStyleSheet('QCheckBox { font: 10pt "MV Boli"; }')
            checkbox.stateChanged.connect(lambda x : self.enable_disable_spin_box(x))
            
            spinbox = QSpinBox(self, objectName = f"food{i}_count") 
            spinbox.setStyleSheet('QSpinBox { font: 10pt "MV Boli"; }')
            spinbox.setDisabled(True)
            spinbox.valueChanged.connect(lambda x : self.change_spin_box(x))                       
            
            self.layout_foods.addRow(checkbox, spinbox)
            
        formFrameDrinks = QFrame()
        self.layout_drinks = QFormLayout(formFrameDrinks)
        self.drinks_area.setWidget(formFrameDrinks)
  
        for i in range(5):
            checkbox = QCheckBox(f"drink{i} \t {i*10}$", self, objectName = f"drink{i}") 
            checkbox.setStyleSheet('QCheckBox { font: 10pt "MV Boli"; }')
            checkbox.stateChanged.connect(lambda x : self.enable_disable_spin_box(x))
            
            spinbox = QSpinBox(self, objectName = f"drink{i}_count") 
            spinbox.setStyleSheet('QSpinBox { font: 10pt "MV Boli"; }')
            spinbox.setDisabled(True)
            spinbox.valueChanged.connect(lambda x : self.change_spin_box(x))                       
            
            self.layout_drinks.addRow(checkbox, spinbox)
            
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
