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
    QRadioButton,
    QButtonGroup
)
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.Qt import QClipboard
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import random, os, sys, re
import pyperclip
import datetime

class ManagerScreen(QDialog):
    def __init__(self, widget, admin, market, user):
        super(ManagerScreen, self).__init__()
        self.widget_pages = widget
        self.admin = admin
        self.market = market
        self.user = user
        
        loadUi("frontend/ui_files/ManagerScreen.ui", self)
        self.tabWidget.setCurrentIndex(0)

        self.copon_code_copy.clicked.connect(self.copy_copon)
        
        self.go_to_user_screen.clicked.connect(self.GoToUserScreen)
        self.exit_button.clicked.connect(lambda x: sys.exit())
        
        self.search_food.textChanged.connect(lambda x: self.search_food_handle(x))
        self.search_drink.textChanged.connect(lambda x: self.search_drink_handle(x))
        
        self.submit_news.clicked.connect(self.add_new)
        self.update_profile_submit.clicked.connect(self.change_user_info)
        self.update_restaurant_profile.clicked.connect(self.change_restaurant_info)
        self.submit_new.clicked.connect(self.submit_fookd_drink)
        self.add_new_admin.clicked.connect(self.add_new_admin_handle)
        self.create_copon.clicked.connect(self.create_copon_handle)
        
        pixmap = QtGui.QPixmap("frontend/icons/drinks.png").scaled(300, 100)
        self.drinks_header.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("frontend/icons/foods.png").scaled(300, 100)
        self.foods_header.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("frontend/icons/foods_drinks.png").scaled(300, 100)
        self.food_drinks_header.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("frontend/icons/restaurant_info.png").scaled(350, 100)
        self.restaurant_info_header.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("frontend/icons/user_info.png").scaled(350, 100)
        self.profile_header.setPixmap(pixmap)
        
        pixmap = QtGui.QPixmap("frontend/icons/admins_info.png").scaled(350, 100)
        self.admins_info_header.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("frontend/icons/add_admin.png").scaled(350, 100)
        self.add_admin_header.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("frontend/icons/income.png").scaled(350, 100)
        self.income_header.setPixmap(pixmap)

        data = self.market.ResturantInfo()
        self.email_input_2.setText(data["EMAIL"])
        self.phone_number_input_2.setText(data["PHONE_NUMBER"])
        
        formFrameDrinks = QFrame()
        self.layout_drinks = QVBoxLayout(formFrameDrinks)
        self.layout_drinks.setAlignment(Qt.AlignTop)
        self.drinks_area.setWidget(formFrameDrinks)

        formFrameIncome = QFrame()
        self.layout_income = QVBoxLayout(formFrameIncome)
        self.layout_income.setAlignment(Qt.AlignTop)
        self.income_area.setWidget(formFrameIncome)
        
        self.group = QButtonGroup()
        self.group.setExclusive(True)
        self.group.buttonClicked.connect(self.check_buttons)
        
        self.search_food.textChanged.connect(lambda x: self.search_food_handle(x))
        self.search_drink.textChanged.connect(lambda x: self.search_drink_handle(x))

        self.calendarWidget_economy.selectionChanged.connect(self.update_economy)
        
        self.calendarWidget.setMinimumDate(self.calendarWidget.selectedDate())
        self.calendarWidget.selectionChanged.connect(self.update_foods)
        self.update_foods()

        self.foods_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.foods_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.drinks_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.drinks_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        self.foods_and_drinks_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.foods_and_drinks_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.admin_list.currentTextChanged.connect(self.on_combobox_changed)

        self.tabWidget.tabBarClicked.connect(self.handle_tabbar_clicked)

    def copy_copon(self):
        text = self.discount_code_show.text()
        if not text == "":
            pyperclip.copy(text)
        
    def search_food_handle(self, new_text):
        date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        formFrameFood = QFrame()
        self.layout_foods = QFormLayout(formFrameFood)
        self.foods_area.setWidget(formFrameFood)
        try:
            for data in self.market.SearchFood(new_text, date):
                radio_button = QRadioButton(f"{data['NAME']}\t {data['PRICE']}$", objectName= str(data["ID"]))
                radio_button.setStyleSheet('QRadioButton { font: 10pt "MV Boli"; min-height: 20px; min-width: 200px;}')
                self.group.addButton(radio_button)
                button_delete = QPushButton("", self, objectName= str(data["ID"]))
                button_delete.setStyleSheet(
                                    """QPushButton{
                                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:1 rgb(255, 189, 108), stop:0 rgb(255, 0, 0));
                                            color: white;
                                            font: 12pt "MV Boli";
                                            border: 2px solid rgb(0, 0, 0);
                                            border-radius: 12px;
                                            min-width: 20px;
                                            max-width: 20px;
                                            max-height: 20px;
                                        }
                                        QPushButton:pressed   {
                                            background-color: rgba(255, 0, 0, 255);
                                            color: white;
                                        }
                                    """
                )
                button_delete.clicked.connect(self.delete_food_drink)
                self.layout_foods.addRow(radio_button, button_delete)
        except Exception as e:
            print(e)
            
    def search_drink_handle(self, new_text):
        date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        formFrameDrink = QFrame()
        self.layout_drinks = QFormLayout(formFrameDrink)
        self.drinks_area.setWidget(formFrameDrink)
        
        try:
            for data in self.market.SearchDrinks(new_text, date):
                radio_button = QRadioButton(f"{data['NAME']}\t {data['PRICE']}$", objectName= str(data["ID"]))
                radio_button.setStyleSheet('QRadioButton { font: 10pt "MV Boli"; min-height: 20px; min-width: 200px;}')
                self.group.addButton(radio_button)
                button_delete = QPushButton("", self, objectName= str(data["ID"]))
                button_delete.setStyleSheet(
                                    """QPushButton{
                                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:1 rgb(255, 189, 108), stop:0 rgb(255, 0, 0));
                                            color: white;
                                            font: 12pt "MV Boli";
                                            border: 2px solid rgb(0, 0, 0);
                                            border-radius: 12px;
                                            min-width: 20px;
                                            max-width: 20px;
                                            max-height: 20px;
                                        }
                                        QPushButton:pressed   {
                                            background-color: rgba(255, 0, 0, 255);
                                            color: white;
                                        }
                                    """
                )
                button_delete.clicked.connect(self.delete_food_drink)
                self.layout_drinks.addRow(radio_button, button_delete)
        except Exception as e:
            print(e)
            
    def add_new(self):
        text = self.news_content_input.toPlainText()
        if text == "":
            self.error.setText("Can't add empty news.")
            return False
        
        self.admin.NewNews(
            text[0:5],
            text,
            datetime.date.today().strftime("%Y-%m-%d")
            )
        self.error.setText("Added Successfully.")
        self.news_content_input.setText("")

    def handle_tabbar_clicked(self, index):
        try:
            if index == 0:
                self.update_foods()
            elif index == 1:
                self.update_admins()
            elif index == 2:
                self.update_economy()
            elif index == 3:
                self.update_news()
            elif index == 4:
                self.update_profile()
        except Exception as e:
            print(e)
            

    def change_spin_box(self, value):
        spin_box = self.sender()
        print(spin_box)
        print(value)
        
    def update_news(self):
        self.news_content_input.clear()
        
    def update_admins(self):
        self.first_name_input_2.clear()
        self.last_name_input_2.clear()
        self.national_code_input_2.clear()
        self.password_input_2.clear()
        self.re_password_input_2.clear()
        self.last_name_input_5.clear()
        self.first_name_input_5.clear()
        self.phone_number_input_5.clear()
        self.email_input_5.clear()
        self.national_code_input_5.clear()
        self.password_input_5.clear()
        self.admin_list.clear()
        self.error5.setText("")
        self.admin_list.addItem("-- Select An Admin --")
        for data in self.admin.AdminsList():
            self.admin_list.addItem(str(data["NATIONAL_CODE"]))
            
        self.admin_list.setCurrentIndex(0)
        
    def add_new_admin_handle(self):
        try:
            firstname = self.first_name_input_2.text()
            lastname = self.last_name_input_2.text()
            phonenumber = self.phone_number_input_2.text()
            email = self.email_input_2.text()
            nationacode = self.national_code_input_2.text()
            password = self.password_input_2.text()
            password_2 = self.re_password_input_2.text()
            
            if not re.search(r'^[A-z ]{2,}$', firstname):
                self.error5.setText("Invalid First Name")
                return False
            
            elif not re.search(r'^[A-z ]{2,}$', lastname):
                self.error5.setText("Invalid Last Name")
                return False
                
            elif not re.search(r'(0|\+98|0098)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}', phonenumber):
                self.error5.setText("Invalid Phone Number")
                return False
            
            elif not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
                self.error5.setText("Invalid Email")
                return False
            
            elif not re.search(r'^\d{10}$', nationacode):
                self.error5.setText("Invalid National Code")
                return False
            
            elif not re.search(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", password):
                self.error5.setText("8 characters, at least 1 letter, 1 number & 1 special character")
                return False

            elif not password == password_2:
                self.error5.setText("Password and Re-password are not equal")
                return False
            
            status , msg  = self.user.Registery(firstname, lastname, phonenumber, email, nationacode, password, "", 0, "Admin")
            self.error5.setText(msg)
            
            if status == True:
                self.update_admins()
        except Exception as e:
            print(e)
            
    def update_economy(self):
        self.discount_code_show.setText("")
        formFrameEconomy = QFrame()
        self.layout_foods_and_drinks = QFormLayout(formFrameEconomy)
        self.foods_and_drinks_area.setWidget(formFrameEconomy)
        date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        status , all_data = self.market.AllOrders(date)
        for data in all_data:
            label = QLabel(
                f"{data['info']['NAME']} \t {data['COUNT']} \t {data['DATE']} \t {data['info']['PRICE']}$"
            )
            label.setStyleSheet('QLabel { font: 7pt "MV Boli"; min-height: 20px; max-height: 20px; min-width: 200px; }')
            button = QPushButton(f"")
            
            if data["STATE"] == "PAYING":
                button.setStyleSheet(
                                    """QPushButton{
                                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:1 rgb(255, 189, 108), stop:0 rgb(255, 0, 0));
                                            color: white;
                                            font: 12pt "MV Boli";
                                            border: 2px solid rgb(0, 0, 0);
                                            border-radius: 12px;
                                            min-width: 20px;
                                            max-width: 20px;
                                            max-height: 20px;
                                        }
                                        QPushButton:pressed   {
                                            background-color: rgba(255, 0, 0, 255);
                                            color: white;
                                        }
                                    """
                )
            else:
                button.setStyleSheet(
                                    """QPushButton{
                                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:1 rgba(7, 76, 0, 255), stop:0 rgba(66, 163, 65, 255));
                                            color: white;
                                            font: 12pt "MV Boli";
                                            border: 2px solid rgb(0, 0, 0);
                                            border-radius: 12px;
                                            min-width: 20px;
                                            max-width: 20px;
                                            max-height: 20px;
                                        }
                                        QPushButton:pressed   {
                                            background-color: rgba(255, 0, 0, 255);
                                            color: white;
                                        }
                                    """
                )


            self.layout_foods_and_drinks.addRow(label, button)
            
        for i in reversed(range(self.layout_income.count())): 
            self.layout_income.itemAt(i).widget().deleteLater()
            
        try:
            status, all_data = self.market.Income(date)
            for data in all_data:
                label = QLabel(f"{data['TRACKINGCODE']}\t {data['SUMINCOME']}$")
                label.setStyleSheet('QLabel { font: 12pt "MV Boli"; min-height: 20px; }')
                self.layout_income.addWidget(label)
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
                    self.layout_votes.addWidget(label, AlignTop)
            except Exception as e:
                print(e)
            
    def on_combobox_changed(self, value):
        if value == "-- Select An Admin --" or value == "":
            self.last_name_input_5.clear()
            self.first_name_input_5.clear()
            self.phone_number_input_5.clear()
            self.email_input_5.clear()
            self.national_code_input_5.clear()
            self.password_input_5.clear()
        else:
            data = self.user.Person(value)
            self.first_name_input_5.setText(data["FIRST_NAME"])
            self.last_name_input_5.setText(data["LAST_NAME"])
            self.phone_number_input_5.setText(data["PHONE_NUMBER"])
            self.email_input_5.setText(data["EMAIL"])
            self.national_code_input_5.setText(data["NATIONAL_CODE"])
            self.password_input_5.setText(data["PASSWORD"])

            
    def update_foods(self):
        date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        self.comboBox.setCurrentIndex(-1)
        self.name_input.clear()
        self.cost_input.setValue(0)
        self.count_input.setValue(0)
        self.material_input.clear()
        self.name_input.setDisabled(True)
        self.count_input.setDisabled(True)
        self.cost_input.setDisabled(True)
        self.material_input.setDisabled(True)
        self.submit_new.setDisabled(True)
        self.error4.setText("")
        self.submit_new.setObjectName("")
        
        formFrameFood = QFrame()
        self.layout_foods = QFormLayout(formFrameFood)
        self.foods_area.setWidget(formFrameFood)
        try:
            radio_button = QRadioButton(f"new food")
            radio_button.setStyleSheet('QRadioButton { font: 10pt "MV Boli"; min-height: 20px; min-width: 200px;}')
            self.layout_foods.addRow(radio_button)
            self.group.addButton(radio_button)
            for data in self.market.FoodMenu(date):
                radio_button = QRadioButton(f"{data['NAME']}\t {data['PRICE']}$", objectName= str(data["ID"]))
                radio_button.setStyleSheet('QRadioButton { font: 10pt "MV Boli"; min-height: 20px; min-width: 200px;}')
                self.group.addButton(radio_button)
                button_delete = QPushButton("", self, objectName= str(data["ID"]))
                button_delete.setStyleSheet(
                                    """QPushButton{
                                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:1 rgb(255, 189, 108), stop:0 rgb(255, 0, 0));
                                            color: white;
                                            font: 12pt "MV Boli";
                                            border: 2px solid rgb(0, 0, 0);
                                            border-radius: 12px;
                                            min-width: 20px;
                                            max-width: 20px;
                                            max-height: 20px;
                                        }
                                        QPushButton:pressed   {
                                            background-color: rgba(255, 0, 0, 255);
                                            color: white;
                                        }
                                    """
                )
                button_delete.clicked.connect(self.delete_food_drink)
                self.layout_foods.addRow(radio_button, button_delete)
        except Exception as e:
            print(e)
            
        formFrameDrink = QFrame()
        self.layout_drinks = QFormLayout(formFrameDrink)
        self.drinks_area.setWidget(formFrameDrink)
        
        try:
            radio_button = QRadioButton(f"new drink")
            radio_button.setStyleSheet('QRadioButton { font: 10pt "MV Boli"; min-height: 20px; min-width: 200px;}')
            self.layout_drinks.addRow(radio_button)
            self.group.addButton(radio_button)
            for data in self.market.DrinkMenu(date):
                radio_button = QRadioButton(f"{data['NAME']}\t {data['PRICE']}$", objectName= str(data["ID"]))
                radio_button.setStyleSheet('QRadioButton { font: 10pt "MV Boli"; min-height: 20px; min-width: 200px;}')
                self.group.addButton(radio_button)
                button_delete = QPushButton("", self, objectName= str(data["ID"]))
                button_delete.setStyleSheet(
                                    """QPushButton{
                                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:1 rgb(255, 189, 108), stop:0 rgb(255, 0, 0));
                                            color: white;
                                            font: 12pt "MV Boli";
                                            border: 2px solid rgb(0, 0, 0);
                                            border-radius: 12px;
                                            min-width: 20px;
                                            max-width: 20px;
                                            max-height: 20px;
                                        }
                                        QPushButton:pressed   {
                                            background-color: rgba(255, 0, 0, 255);
                                            color: white;
                                        }
                                    """
                )
                button_delete.clicked.connect(self.delete_food_drink)
                self.layout_drinks.addRow(radio_button, button_delete)
        except Exception as e:
            print(e)
            
    def delete_food_drink(self):
        self.admin.DeleteFoodDrink(self.sender().objectName())
        self.update_foods()
        
    def check_buttons(self, radioButton):
        self.name_input.setDisabled(False)
        self.count_input.setDisabled(False)
        self.cost_input.setDisabled(False)
        self.material_input.setDisabled(False)
        self.submit_new.setDisabled(False)
        self.count_input.setMinimum(1)
        
        text = radioButton.text()
        
        if text == "new food":
            self.comboBox.setCurrentIndex(0)
            self.name_input.clear()
            self.cost_input.setValue(0)
            self.count_input.setValue(1)
            self.material_input.clear()
            self.submit_new.setObjectName("new")
        elif text == "new drink":
            self.comboBox.setCurrentIndex(1)
            self.name_input.clear()
            self.cost_input.setValue(0)
            self.count_input.setValue(1)
            self.material_input.clear()
            self.submit_new.setObjectName("new")
        else:
            data = self.admin.FoodInfo(radioButton.objectName())
            self.submit_new.setObjectName(str(data["ID"]))
            self.name_input.setText(data["NAME"])
            self.cost_input.setValue(data["PRICE"])
            self.count_input.setValue(data["INVENTORY"])
            self.material_input.setText(data["MATERIAL"].replace("|","-"))
            if data["MEAL"] == "food":
                self.comboBox.setCurrentIndex(0)
            elif data["MEAL"] == "drink":
                self.comboBox.setCurrentIndex(1)


    def submit_fookd_drink(self):
        type_do = self.submit_new.objectName()
        name = self.name_input.text()
        date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        cost = self.cost_input.value()
        count = self.count_input.value()
        material = self.material_input.text().split("-")
        meal = self.comboBox.currentText()
        if name == "":
            self.error4.setText("Name input is empty.")
            return False
        
        if type_do == "new":
            self.admin.NewFood(name, cost, count, date, "", meal, material)
        else:
            self.admin.UpdateFood(type_do, name, cost, count, material)
            
        self.update_foods()
        
    def update_profile(self):
        self.error2.setText("")
        self.error3.setText("")
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
            self.error2.setText("Invalid First Name")
            return False
        
        elif not re.search(r'^[A-z ]{2,}$', lastname):
            self.error2.setText("Invalid Last Name")
            return False
            
        elif not re.search(r'(0|\+98|0098)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}', phonenumber):
            self.error2.setText("Invalid Phone Number")
            return False
        
        elif not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            self.error2.setText("Invalid Email")
            return False
        
        elif not re.search(r'^\d{10}$', nationacode):
            self.error2.setText("Invalid National Code")
            return False
        
        elif not re.search(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", password):
            self.error2.setText("8 characters, at least 1 letter, 1 number & 1 special character")
            return False

        elif not password == password_2:
            self.error2.setText("Password and Re-password are not equal")
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

    def change_restaurant_info(self):
        try:
            restaurant_name_input = self.restaurant_name_input.text()
            manager_first_name_input = self.manager_first_name_input.text()
            manager_last_name_input = self.manager_last_name_input.text()
            restaurant_phone_number_input = self.restaurant_phone_number_input.text()
            restaurant_email_input = self.restaurant_email_input.text()
            location_input = self.location_input.text()
            type_input = self.type_input.text()
            address_input = self.address_input.text()

            if not re.search(r'^[A-z ]{2,}$', manager_first_name_input):
                self.error3.setText("Invalid First Name")
                return False
            
            elif not re.search(r'^[A-z ]{2,}$', manager_last_name_input):
                self.error3.setText("Invalid Last Name")
                return False
                        
            elif not re.search(r'(0|\+98|0098)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}', restaurant_phone_number_input):
                self.error3.setText("Invalid Phone Number")
                return False
            
            elif not re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', restaurant_email_input):
                self.error3.setText("Invalid Email")
                return False

            elif not re.search(r'^[A-z ]{2,}$', location_input):
                self.error3.setText("Invalid Location")
                return False
            
            elif not re.search(r'^[A-z ]{2,}$', type_input):
                self.error3.setText("Invalid Type")
                return False
            
            elif not re.search(r'^[A-z ]{2,}$', address_input):
                self.error3.setText("Invalid Address")
                return False
            else:
                self.admin.ChangeInfo(
                    MANAGER_FIRST_NAME = manager_first_name_input,
                    MANAGER_LAST_NAME = manager_last_name_input,
                    PHONE_NUMBER = restaurant_phone_number_input,
                    EMAIL = restaurant_email_input,
                    LOCATION= location_input,
                    TYPE = type_input,
                    ADDRESS = address_input
                    )
                self.update_profile()
        except Exception as e:
            print(e)
            
    def create_copon_handle(self):
        percent = self.percent_input.value()
        count = self.count_copon_input.value()
        if percent == 0 or count == 0:
            self.discount_code_show.setText("Can't create with 0 value.")
        else:
            status , code = self.admin.NewCopon(percent, count)
            self.discount_code_show.setText(code)

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

    def GoToUserScreen(self):
        self.widget_pages.setFixedHeight(800)
        self.widget_pages.setFixedWidth(1200)
        self.widget_pages.setCurrentIndex(2)
        
        widget_to_update = self.widget_pages.widget(2)
        currnt_index = widget_to_update.tabWidget.currentIndex()
        widget_to_update.handle_tabbar_clicked(currnt_index)
        
        self.centralize()
