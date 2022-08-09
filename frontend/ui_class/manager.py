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
        
        self.submit_news.clicked.connect(self.add_new)
        self.update_profile_submit.clicked.connect(self.change_user_info)
        self.update_restaurant_profile.clicked.connect(self.change_restaurant_info)
        
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

                
        formFrameFoods = QFrame()
        self.layout_foods = QVBoxLayout(formFrameFoods)
        self.foods_area.setWidget(formFrameFoods)

        formFrameDrinks = QFrame()
        self.layout_drinks = QVBoxLayout(formFrameDrinks)
        self.drinks_area.setWidget(formFrameDrinks)

        formFrameIncome = QFrame()
        self.layout_income = QVBoxLayout(formFrameIncome)
        self.income_area.setWidget(formFrameIncome)
        
        self.group = QButtonGroup()
        self.group.setExclusive(True)
        self.group.buttonClicked.connect(self.check_buttons)
        
        self.search_food.textChanged.connect(lambda x: self.doSomething(x))
        self.search_drink.textChanged.connect(lambda x: self.doSomething(x))

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
        
        self.tabWidget.tabBarClicked.connect(self.handle_tabbar_clicked)

    def copy_copon(self):
        text = self.discount_code_show.text()
        if not text == "":
            pyperclip.copy(text)
        
    def doSomething(self, new_text):
        print(new_text)
        
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
        self.phone_number_input_2.clear()
        self.email_input_2.clear()
        self.national_code_input_2.clear()
        self.password_input_2.clear()
        self.re_password_input_2.clear()
        self.last_name_input_5.clear()
        self.first_name_input_2.clear()
        self.phone_number_input_5.clear()
        self.email_input_5.clear()
        self.national_code_input_5.clear()
        self.password_input_5.clear()
        self.re_password_input_5.clear()
        self.admin_list.clear()
        self.admin_list.addItems(["-- Select An Admin --", "reza", "ali", "mosa"])
        self.admin_list.setCurrentIndex(0)
        
    def update_economy(self):
        formFrameEconomy = QFrame()
        self.layout_foods_and_drinks = QFormLayout(formFrameEconomy)
        self.foods_and_drinks_area.setWidget(formFrameEconomy)
        date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        for i in range(40):
            label = QLabel(
                f"label{i} {random.randint(3, 90)}",
                self,
                objectName=f"label{i}",
            )
            label.setStyleSheet('QLabel { font: 8pt "MV Boli"; min-height: 20px; max-height: 20px; min-width: 210px; }')

            button = QPushButton(f"", self, objectName=f"food{i}_count")
            if i % 2 == 0 :
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
            for i in range(40):
                label = QLabel(f"economy {i} {random.randint(3, 90)}")
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
                    self.layout_votes.addWidget(label)
            except Exception as e:
                print(e)
            
    def on_combobox_changed(self, value):
        if value == "-- Select An Order --" or value == "":
            self.vote_text_area.setDisabled(True)
        else:
            self.vote_text_area.setDisabled(False)
            print("combobox changed", value , self.sender())

            
    def update_foods(self):
        print(self.calendarWidget.selectedDate().toString("yyyy-MM-dd"))
        
        for i in reversed(range(self.layout_foods.count())): 
            self.layout_foods.itemAt(i).widget().deleteLater()
            
        for i in reversed(range(self.layout_drinks.count())): 
            self.layout_drinks.itemAt(i).widget().deleteLater()

        for button in self.group.buttons():
               self.group.removeButton(button)

        try:
            radio_button = QRadioButton(f"new food")
            radio_button.setStyleSheet('QRadioButton { font: 12pt "MV Boli"; min-height: 20px; }')
            self.layout_foods.addWidget(radio_button)
            self.group.addButton(radio_button)
            for i in range(20):
                radio_button = QRadioButton(f"button radio f {i} {random.randint(3, 90)}")
                radio_button.setStyleSheet('QRadioButton { font: 12pt "MV Boli"; min-height: 20px; }')
                self.layout_foods.addWidget(radio_button)
                self.group.addButton(radio_button)
        except Exception as e:
            print(e)
            
        try:
            radio_button = QRadioButton(f"new drink")
            radio_button.setStyleSheet('QRadioButton { font: 12pt "MV Boli"; min-height: 20px; }')
            self.layout_drinks.addWidget(radio_button)
            self.group.addButton(radio_button)
            for i in range(20):
                radio_button = QRadioButton(f"button radio d {i} {random.randint(3, 90)}")
                radio_button.setStyleSheet('QRadioButton { font: 12pt "MV Boli"; min-height: 20px; }')
                self.layout_drinks.addWidget(radio_button)
                self.group.addButton(radio_button)
        except Exception as e:
            print(e)            

    def check_buttons(self, radioButton):
        print(radioButton.text())
        
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
            self.error.setText("Invalid First Name")
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
