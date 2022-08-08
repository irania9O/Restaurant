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
    QVBoxLayout,
    QPushButton,
    QRadioButton 
)
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import sys
import random

indexes = {0: "Menu", 1: "Cart", 2: "Orders"}


class MainScreen(QDialog):
    def __init__(self, widget, admin, market, user):
        super(MainScreen, self).__init__()
        self.widget_pages = widget
        self.admin = admin
        self.market = market
        self.user = user
        
        loadUi("frontend/ui_files/MainScreen.ui", self)
        self.tabWidget.setCurrentIndex(0)
        
        self.go_to_admin_screen.clicked.connect(self.GoToAdminScreen)
        self.exit_button.clicked.connect(lambda x: sys.exit())
    
        pixmap = QtGui.QPixmap("frontend/icons/drinks.png").scaled(300, 100)
        self.drinks_header.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("frontend/icons/foods.png").scaled(300, 100)
        self.foods_header.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("frontend/icons/factor.png").scaled(350, 100)
        self.factor_header.setPixmap(pixmap)
        
        pixmap = QtGui.QPixmap("frontend/icons/restaurant_info.png").scaled(350, 100)
        self.restaurant_info_header.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("frontend/icons/user_info.png").scaled(350, 100)
        self.profile_header.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("frontend/icons/register_vote.png").scaled(300, 100)
        self.register_vote_header.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("frontend/icons/foods_drinks.png").scaled(300, 100)
        self.food_drinks_header.setPixmap(pixmap)
        
        # print(self.lcdNumber.intValue())
        # self.lcdNumber.display(150)
        # print(self.lcdNumber.intValue())
        self.search_food.textChanged.connect(lambda x: self.doSomething(x))
        self.search_drink.textChanged.connect(lambda x: self.doSomething(x))

        self.calendarWidget_vote.selectionChanged.connect(self.update_vote)
        
        self.calendarWidget.setMinimumDate(self.calendarWidget.selectedDate())
        self.calendarWidget.selectionChanged.connect(self.update_foods)
        self.update_foods()

        self.foods_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.foods_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.drinks_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.drinks_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.cart_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.cart_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.tabWidget.tabBarClicked.connect(self.handle_tabbar_clicked)

        self.foods_orderd.currentTextChanged.connect(self.on_combobox_changed)
        
        formFrameNews = QFrame()
        self.layout_news = QVBoxLayout(formFrameNews)
        self.news_area.setWidget(formFrameNews)

        formFrameVotes = QFrame()
        self.layout_votes = QVBoxLayout(formFrameVotes)
        self.votes_area.setWidget(formFrameVotes)
        
        formFrameVotesFoodsDrinks = QFrame()
        self.layout_votes_foods_drinks = QVBoxLayout(formFrameVotesFoodsDrinks)
        self.foods_and_drinks_area.setWidget(formFrameVotesFoodsDrinks)
        
    def check_admin(self):
        if self.user.Person(self.user.national_code)["POSITION"] == "Admin":
            self.go_to_admin_screen.show()
        else:
            self.go_to_admin_screen.hide()
        
    def doSomething(self, new_text):
        print(new_text)

    def handle_tabbar_clicked(self, index):
        if index == 0:
            self.update_foods()
        elif index == 1:
            self.update_cart()   
        elif index == 2:
            self.update_orders()
        elif index == 3:
            self.update_vote()
        elif index == 4:
            self.update_news()
            
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
        
    def update_news(self):
        for i in reversed(range(self.layout_news.count())): 
            self.layout_news.itemAt(i).widget().deleteLater()
        status , data = self.user.AllNews()
        if not len(data) == 0:
            for news in data:
                label = QLabel(news["CONTENT"])
                label.setStyleSheet('QLabel { font: 12pt "MV Boli"; min-height: 20px; max-height: 20px;}')
                self.layout_news.addWidget(label)
        else:
            label = QLabel("No News Published Yet.")
            label.setStyleSheet('QLabel { font: 12pt "MV Boli"; min-height: 20px; }')
            self.layout_news.addWidget(label)
            
    def update_vote(self):
        for i in reversed(range(self.layout_votes.count())): 
            self.layout_votes.itemAt(i).widget().deleteLater()
            
        for i in reversed(range(self.layout_votes_foods_drinks.count())): 
            self.layout_votes_foods_drinks.itemAt(i).widget().deleteLater()
        
        try:
            for i in range(40):
                radio_button = QRadioButton(f" button radio {i} {random.randint(3, 90)}")
                radio_button.setStyleSheet('QRadioButton { font: 12pt "MV Boli"; min-height: 20px; }')
                radio_button.toggled.connect(self.radio_button_selection)
                self.layout_votes_foods_drinks.addWidget(radio_button)
        except Exception as e:
            print(e)
            
        try:
            self.foods_orderd.clear()
            self.foods_orderd.addItems(["-- Select An Order --", "f2", "f3", "f4"])
            self.foods_orderd.setCurrentIndex(0)
        except Exception as e:
            print(e)

            

    def radio_button_selection(self ):
        radioButton = self.sender()
        if radioButton.isChecked():
            print(radioButton)
            for i in reversed(range(self.layout_votes.count())): 
                self.layout_votes.itemAt(i).widget().deleteLater()
            try:
                for i in range(40):
                    label = QLabel(f" vote {i} {random.randint(3, 90)}")
                    label.setStyleSheet('QLabel { font: 12pt "MV Boli"; min-height: 20px; }')
                    self.layout_votes.addWidget(label)
            except Exception as e:
                print(e)
            
    def on_combobox_changed(self, value):
        if value == "-- Select An Order --" or value == "":
            self.vote_text_area.setDisabled(True)
        else:
            self.vote_text_area.setDisabled(False)
            print("combobox changed", value , self.sender())
    
    def update_cart(self):
        formFrameCart = QFrame()
        self.layout_cart = QFormLayout(formFrameCart)
        self.cart_area.setWidget(formFrameCart)
            
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
            button.clicked.connect(self.delete_function)
            self.layout_cart.addRow(label, button)
            
    def delete_function(self):
        print(self.sender())
        print(self.sender().objectName())
        print()
        
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

            self.layout_orders.addRow(label, button)
            
    def update_foods(self):
        print(self.calendarWidget.selectedDate().toString("yyyy-MM-dd"))
        print(self.admin.national_code)
        
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
        
    def GoToAdminScreen(self):
        self.widget_pages.setFixedHeight(800)
        self.widget_pages.setFixedWidth(1200)
        self.widget_pages.setCurrentIndex(3)
        self.centralize()
