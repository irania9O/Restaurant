from PyQt5.QtWidgets import (
    QDialog,
    QApplication,
    QDesktopWidget,
    QFrame,
    QSpinBox,
    QCheckBox,
    QLabel,
    QLineEdit,
    QFormLayout,
    QPushButton,
)
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi

indexes = {0: "Menu", 1: "Orders", 2: "History"}


class MainScreen(QDialog):
    def __init__(self, widget):
        super(MainScreen, self).__init__()
        self.widget_pages = widget
        loadUi("frontend/ui_files/MainScreen.ui", self)
        self.tabWidget.setCurrentIndex(0)
        self.order.clicked.connect(self.GoToLoginScreen)
        self.exit_button.clicked.connect(lambda x: QtCore.QCoreApplication.quit())

        pixmap = QtGui.QPixmap("frontend/icons/drinks.png").scaled(300, 100)
        self.drinks.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("frontend/icons/foods.png").scaled(300, 100)
        self.foods.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("frontend/icons/factor.png").scaled(350, 100)
        self.factor.setPixmap(pixmap)

        # print(self.lcdNumber.intValue())
        # self.lcdNumber.display(150)
        # print(self.lcdNumber.intValue())
        self.search_food.textChanged.connect(lambda x: self.doSomething(x))
        self.search_drink.textChanged.connect(lambda x: self.doSomething(x))

        self.calendarWidget.setMinimumDate(self.calendarWidget.selectedDate())
        self.calendarWidget.selectionChanged.connect(self.update_foods)
        self.update_foods()

        self.foods_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.foods_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.drinks_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.drinks_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.orders_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.orders_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.tabWidget.tabBarClicked.connect(self.handle_tabbar_clicked)

    def doSomething(self, new_text):
        print(new_text)

    def handle_tabbar_clicked(self, index):
        if index == 0:
            self.update_foods()
            
        if index == 1:
            self.update_orders()
        elif index == 2:
            self.update_history()

    def enable_disable_spin_box(self, name):
        counter_drinks = self.findChild(QSpinBox, f"{self.sender().objectName()}_count")
        if counter_drinks.isEnabled():
            counter_drinks.setDisabled(True)
            counter_drinks.setValue(0)
        else:
            counter_drinks.setDisabled(False)
            counter_drinks.setValue(1)

    def change_spin_box(self, value):
        spin_box = self.sender()
        print(spin_box)
        print(value)

    def update_orders(self):
        formFrameOrders = QFrame()
        self.layout_orders = QFormLayout(formFrameOrders)
        self.orders_area.setWidget(formFrameOrders)

        for i in range(40):
            date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
            label = QLabel(
                f"label{i} \t {i*10}$ \t {i*2 + 5} \t {date} \t",
                self,
                objectName=f"label{i}",
            )
            label.setStyleSheet('QLabel { font: 12pt "MV Boli"; min-width: 850px;}')

            button = QPushButton(f"DELETE", self, objectName=f"food{i}_count")
            button.setStyleSheet(
                                """QPushButton{
                                        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:1 rgb(255, 189, 108), stop:0 rgb(255, 0, 0));
                                        color: white;
                                        font: 12pt "MV Boli";
                                        border: 2px solid rgb(58, 134, 255);
                                        border-radius: 12px;
                                    }
                                    
                                    QPushButton:pressed   {
                                        background-color: rgba(255, 0, 0, 255);
                                        color: white;
                                    }
                                """
            )

            self.layout_orders.addRow(label, button)
            
    def update_history(self):
        formFrameHistory = QFrame()
        self.layout_payed = QFormLayout(formFrameHistory)
        self.payed_area.setWidget(formFrameHistory)

        for i in range(40):
            date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
            label = QLabel(
                f"label{i} \t {i*10}$ \t {i*2 + 5} \t {date} \t",
                self,
                objectName=f"label{i}",
            )
            label.setStyleSheet('QLabel { font: 12pt "MV Boli"; min-width: 850px;}')

            button = QPushButton(f"PAYED", self, objectName=f"food{i}_count")
            button.setStyleSheet(
                                """QPushButton{
                                        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:1 rgba(7, 76, 0, 255), stop:0 rgba(66, 163, 65, 255));
                                        color: white;
                                        font: 12pt "MV Boli";
                                        border: 2px solid rgb(58, 134, 255);
                                        border-radius: 12px;
                                    }
                                """
            )

            self.layout_payed.addRow(label, button)
            
    def update_foods(self):
        print(self.calendarWidget.selectedDate().toString("yyyy-MM-dd"))

        formFrameFoods = QFrame()
        self.layout_foods = QFormLayout(formFrameFoods)
        self.foods_area.setWidget(formFrameFoods)

        for i in range(5):
            checkbox = QCheckBox(f"food{i} \t {i*10}$", self, objectName=f"food{i}")
            checkbox.setStyleSheet(
                'QCheckBox { font: 10pt "MV Boli"; min-width: 160px;}'
            )
            checkbox.stateChanged.connect(lambda x: self.enable_disable_spin_box(x))

            spinbox = QSpinBox(self, objectName=f"food{i}_count")
            spinbox.setStyleSheet('QSpinBox { font: 10pt "MV Boli"; }')
            spinbox.setDisabled(True)
            spinbox.valueChanged.connect(lambda x: self.change_spin_box(x))

            self.layout_foods.addRow(checkbox, spinbox)

        formFrameDrinks = QFrame()
        self.layout_drinks = QFormLayout(formFrameDrinks)
        self.drinks_area.setWidget(formFrameDrinks)

        for i in range(5):
            checkbox = QCheckBox(f"drink{i} \t {i*10}$", self, objectName=f"drink{i}")
            checkbox.setStyleSheet(
                'QCheckBox { font: 10pt "MV Boli"; min-width: 160px;}'
            )
            checkbox.stateChanged.connect(lambda x: self.enable_disable_spin_box(x))

            spinbox = QSpinBox(self, objectName=f"drink{i}_count")
            spinbox.setStyleSheet('QSpinBox { font: 10pt "MV Boli"; }')
            spinbox.setDisabled(True)
            spinbox.valueChanged.connect(lambda x: self.change_spin_box(x))

            self.layout_drinks.addRow(checkbox, spinbox)

    def centralize(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos()
        )
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.widget_pages.move(frameGm.topLeft())

    def GoToLoginScreen(self):
        self.widget_pages.setFixedHeight(500)
        self.widget_pages.setFixedWidth(600)
        self.widget_pages.setCurrentIndex(0)
        self.centralize()
