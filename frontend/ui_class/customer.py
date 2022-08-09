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
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import sys, re
import random
import datetime

indexes = {0: "Menu", 1: "Cart", 2: "Orders"}


class MainScreen(QDialog):
    def __init__(self, widget, admin, market, user):
        super(MainScreen, self).__init__()
        self.widget_pages = widget
        self.admin = admin
        self.market = market
        self.user = user
        self.orders = {}
        
        loadUi("frontend/ui_files/MainScreen.ui", self)
        self.tabWidget.setCurrentIndex(0)
        
        self.go_to_admin_screen.clicked.connect(self.GoToAdminScreen)
        self.exit_button.clicked.connect(lambda x: sys.exit())
        self.update_profile_submit.clicked.connect(self.change_user_info)
        self.order.clicked.connect(self.confirm_order)
        self.use_copon.clicked.connect(self.use_copon_handle)
        self.pay.clicked.connect(self.pay_handle)
        
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
        self.layout_news.setAlignment(Qt.AlignTop)
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
        elif index == 5:
            self.update_profile()
            
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
        changer = int(spin_box.objectName().replace("_count",""))
        self.orders[changer] = value
        self.MenuTotalAmount.display(self.calculate_total())
        # print(self.lcdNumber.intValue())
       
        
    def update_news(self):
        for i in reversed(range(self.layout_news.count())): 
            self.layout_news.itemAt(i).widget().deleteLater()
        status , data = self.user.AllNews()
        if not len(data) == 0:
            for news in data:
                label = QLabel(news["CONTENT"])
                label.setStyleSheet('QLabel { font: 12pt "MV Boli"; min-height: 30px; max-height: 20px;}')
                self.layout_news.addWidget(label)
        else:
            label = QLabel("No News Published Yet.")
            label.setStyleSheet('QLabel { font: 12pt "MV Boli"; min-height: 30px; }')
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
        sum_orders = 0
        self.discount_code.setDisabled(False)
        self.use_copon.setDisabled(False)
        self.discount_code.clear()
        
        formFrameCart = QFrame()
        self.layout_cart = QFormLayout(formFrameCart)
        self.cart_area.setWidget(formFrameCart)
        try:
            status , all_data = self.market.PayingOrders(self.user.national_code)
            for data in all_data:
                sum_orders += data['COUNT'] * data['info']['PRICE']
                label = QLabel(
                    f"{data['info']['NAME']} \t {data['info']['PRICE']}$ \t {data['COUNT']} \t {data['DATE']}"
                )
                label.setStyleSheet('QLabel { font: 12pt "MV Boli"; min-width: 850px;}')

                button = QPushButton(f"DELETE", self, objectName= f"del_{data['ID']}")
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
        except Exception as e:
            print(e)
        self.CartTotalAmount.display(sum_orders)
        
    def delete_function(self):
        order_id = int(self.sender().objectName().replace("del_",""))
        self.user.DeleteOrder(order_id)
        self.update_cart()
        
    def update_orders(self):
        formFrameOrders = QFrame()
        self.layout_orders = QFormLayout(formFrameOrders)
        self.orders_area.setWidget(formFrameOrders)

        status , all_data = self.market.PayedOrders(self.user.national_code)
        for data in all_data:
            label = QLabel(
                f"{data['info']['NAME']} \t {data['info']['PRICE']}$ \t {data['COUNT']} \t {data['DATE']}"
            )
            label.setStyleSheet('QLabel { font: 12pt "MV Boli"; min-width: 850px;}')

            button = QPushButton(f"PAYED")
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
        self.MenuTotalAmount.display(0)
        date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        
        formFrameFoods = QFrame()
        self.layout_foods = QFormLayout(formFrameFoods)
        self.foods_area.setWidget(formFrameFoods)

        for data in self.market.FoodMenu(date):
            if data['INVENTORY'] < 1:
                continue
            checkbox = QCheckBox(f"{data['NAME']}\t {data['PRICE']}$", objectName= str(data["ID"]))
            checkbox.setStyleSheet(
                'QCheckBox { font: 10pt "MV Boli"; min-width: 160px;}'
            )
            checkbox.stateChanged.connect(lambda x: self.enable_disable_spin_box(x))

            spinbox = QSpinBox(self, objectName=f"{data['ID']}_count")
            spinbox.setStyleSheet('QSpinBox { font: 10pt "MV Boli"; }')
            spinbox.setDisabled(True)
            spinbox.setMaximum(data["INVENTORY"])
            spinbox.valueChanged.connect(lambda x: self.change_spin_box(x))

            if data["ID"] in self.orders:
                count = self.orders[data["ID"]]
                if count > 0 :
                    checkbox.setChecked(True)
                    spinbox.setDisabled(False)
                    spinbox.setValue(count)
                
            self.layout_foods.addRow(checkbox, spinbox)

        formFrameDrinks = QFrame()
        self.layout_drinks = QFormLayout(formFrameDrinks)
        self.drinks_area.setWidget(formFrameDrinks)

        for data in self.market.DrinkMenu(date):
            if data['INVENTORY'] < 1:
                continue
            checkbox = QCheckBox(f"{data['NAME']}\t {data['PRICE']}$", objectName= str(data["ID"]))
            checkbox.setStyleSheet(
                'QCheckBox { font: 10pt "MV Boli"; min-width: 160px;}'
            )
            checkbox.stateChanged.connect(lambda x: self.enable_disable_spin_box(x))

            spinbox = QSpinBox(self, objectName=f"{data['ID']}_count")
            spinbox.setStyleSheet('QSpinBox { font: 10pt "MV Boli"; }')
            spinbox.setDisabled(True)
            spinbox.setMaximum(data["INVENTORY"])
            spinbox.valueChanged.connect(lambda x: self.change_spin_box(x))

            if data["ID"] in self.orders:
                count = self.orders[data["ID"]]
                if count > 0 :
                    checkbox.setChecked(True)
                    spinbox.setDisabled(False)
                    spinbox.setValue(count)
            
            self.layout_drinks.addRow(checkbox, spinbox)
            
    def calculate_total(self):
        try:
            sum_orders = 0
            for key, value in self.orders.items():
                if value > 0:
                    sum_orders += self.user.FoodInfo(key)["PRICE"] * value
            return sum_orders
        except Exception as e:
            print(e)
            
    def confirm_order(self):
        date = datetime.date.today().strftime("%Y-%m-%d")
        for key, value in self.orders.items():
            self.user.NewOrder(key, date, value)
        self.orders = {}
        self.update_foods()
        self.update_cart()
        self.tabWidget.setCurrentIndex(1)
            
    def update_profile(self):
        self.error.setText("")
        self.re_password_input.setText("")
        data = self.market.ResturantInfo()
        self.restaurant_name_input.setText(data["NAME_RESTURANT"])
        self.manager_first_name_input.setText(data["MANAGER_FIRST_NAME"])
        self.manager_last_name_input.setText(data["MANAGER_LAST_NAME"])
        self.restaurant_phone_number_input.setText(data["PHONE_NUMBER"])
        self.restaurant_email_input.setText(data["EMAIL"])
        self.location_input.setText(data["LOCATION"])
        self.type_input.setText(data["TYPE"])
        self.address_input.setText(data["ADDRESS"])

        data_person =  self.user.Person(self.user.national_code)
        self.first_name_input.setText(data_person["FIRST_NAME"])
        self.last_name_input.setText(data_person["LAST_NAME"])
        self.phone_number_input.setText(data_person["PHONE_NUMBER"])
        self.email_input.setText(data_person["EMAIL"])
        self.national_code_input.setText(data_person["NATIONAL_CODE"])
        self.password_input.setText(data_person["PASSWORD"])
        
    def change_user_info(self):
        firstname = self.first_name_input.text()
        lastname = self.last_name_input.text()
        phonenumber = self.phone_number_input.text()
        email = self.email_input.text()
        nationacode = self.national_code_input.text()
        password = self.password_input.text()
        password_2 = self.re_password_input.text()
        
        if not re.search(r'^[A-z ]{2,}$', firstname):
            self.error.setText("Invalid First Name")
            return False
        
        elif not re.search(r'^[A-z ]{2,}$', lastname):
            self.error.setText("Invalid Last Name")
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

        elif not password == password_2:
            self.error.setText("Password and Re-password are not equal")
            return False
        
        else:
            self.user.Update(FIRST_NAME = firstname,
                             LAST_NAME = lastname,
                             PHONE_NUMBER = phonenumber,
                             EMAIL = email,
                             NATIONAL_CODE = nationacode,
                             PASSWORD = password
                             )
            self.update_profile()
            
    def use_copon_handle(self):
        status, msg = self.market.InfoCopon(self.discount_code.text())
        if status == False :
            self.discount_code.setText(msg)
        else:
            self.discount_code.setDisabled(True)
            self.use_copon.setDisabled(True)
            if msg["COUNT"] > 0:
                new_total = int(self.CartTotalAmount.intValue() * (100 - msg["PERCENT"]) / 100)
                self.CartTotalAmount.display(new_total)
            else:
                self.discount_code.setText("Copon Consumed.")
            
    def pay_handle(self):
        try:
            date = datetime.date.today().strftime("%Y-%m-%d")
            if self.discount_code.isEnabled() or self.discount_code.text() == "":
                self.user.Pay(self.CartTotalAmount.intValue(), date)
            else:
                self.user.Pay(self.CartTotalAmount.intValue(), date, self.discount_code.text())
            self.update_cart()
            self.update_orders()
            self.tabWidget.setCurrentIndex(2)
        except Exception as e:
            print(e)
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
        
        widget_to_update = self.widget_pages.widget(3)
        currnt_index = widget_to_update.tabWidget.currentIndex()
        widget_to_update.handle_tabbar_clicked(currnt_index)
        
        self.centralize()
