from PyQt5.QtWidgets import (
    QDialog,
    QMainWindow,
    QApplication,
    QDesktopWidget,
    QFrame,
    QFormLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.uic import loadUi
import sys, random, time, os, re
import datetime

from frontend.ui_class.login import LoginScreen
from frontend.ui_class.signup import SignUpScreen
from frontend.ui_class.customer import MainScreen
from frontend.ui_class.manager import ManagerScreen

from backend.base import DATABASE
from backend.admin import Admin
from backend.market import Market
from backend.user import User

indexes = {"LoginScreen": 0, "SignUpScreen": 1, "MainScreen": 2, "ManagerScreen": 3}


def main(restaurant_name):
    try:
        # app = QApplication(sys.argv)
        print(restaurant_name)
        widget = QStackedWidget()
        widget.setWindowFlags(Qt.FramelessWindowHint)

        admin = Admin(restaurant_name, "0")
        market = Market(restaurant_name, "0")
        user = User(restaurant_name, "0")

        widget.addWidget(LoginScreen(widget, admin, market, user))
        widget.addWidget(SignUpScreen(widget, admin, market, user))
        widget.addWidget(MainScreen(widget, admin, market, user))
        widget.addWidget(ManagerScreen(widget, admin, market, user))
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

        # widget.show()
        return widget

        # sys.exit(app.exec_())

    except Exception as error:
        print(error)


class ThreadProgress(QThread):
    mysignal = pyqtSignal(int)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        i = 0
        while i < 101:
            time.sleep(0.03)
            self.mysignal.emit(i)
            i += 1


class Splash(QDialog):
    def __init__(self, restaurant_name, parent=None):
        super(Splash, self).__init__(parent)
        self._restaurant_name = restaurant_name
        self.load_int = random.randint(40, 80)

        loadUi("frontend/ui_files/SplashScreen.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.centralize()

        pixmap = QPixmap("frontend/icons/restaurant.png").scaled(320, 320)
        self.logo.setPixmap(pixmap)

        self.restaurant_name.setText(restaurant_name)

        progress = ThreadProgress(self)
        progress.mysignal.connect(self.progress)
        progress.start()

    @pyqtSlot(int)
    def progress(self, i):
        self.progressBar.setValue(i)
        if i == self.load_int:
            self.w_l = main(self._restaurant_name)
        if i == 100:
            self.hide()
            self.w_l.show()

    def centralize(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos()
        )
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


class Restaurants(QDialog):
    def __init__(self):
        super(Restaurants, self).__init__()
        loadUi("frontend/ui_files/Restaurants.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.tabWidget.setCurrentIndex(0)
        self.centralize()

        self.show_restaurants()

        pixmap = QPixmap("frontend/icons/restaurant_info.png").scaled(350, 100)
        self.restaurant_info_header.setPixmap(pixmap)

        pixmap = QPixmap("frontend/icons/restaurants.png").scaled(350, 100)
        self.restaurants_header.setPixmap(pixmap)

        self.restaurants_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.restaurants_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.add_new_restaurant.clicked.connect(self.add_new_restaurant_button)

        self.exit_button.clicked.connect(lambda x: sys.exit())

        self.tabWidget.tabBarClicked.connect(self.handle_tabbar_clicked)

    def handle_tabbar_clicked(self, index):
        if index == 0:
            self.show_restaurants()
        elif index == 1:
            self.clear_restaurant_inputs()

    def add_new_restaurant_button(self):
        try:
            restaurant_name_input = self.restaurant_name_input.text()
            manager_first_name_input = self.manager_first_name_input.text()
            manager_last_name_input = self.manager_last_name_input.text()
            restaurant_phone_number_input = self.restaurant_phone_number_input.text()
            restaurant_email_input = self.restaurant_email_input.text()
            national_code_input = self.national_code_input.text()
            location_input = self.location_input.text()
            type_input = self.type_input.text()
            address_input = self.address_input.text()
            password_input = self.password_input.text()
            re_password_input = self.re_password_input.text()

            if not re.search(r"^[A-z \d]{2,}$", restaurant_name_input):
                self.error.setText("Invalid Restaurant Name")
                return False

            elif not re.search(r"^[A-z ]{2,}$", manager_first_name_input):
                self.error.setText("Invalid First Name")
                return False

            elif not re.search(r"^[A-z ]{2,}$", manager_last_name_input):
                self.error.setText("Invalid Last Name")
                return False

            elif not re.search(
                r"(0|\+98|0098)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}",
                restaurant_phone_number_input,
            ):
                self.error.setText("Invalid Phone Number")
                return False

            elif not re.search(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}",
                restaurant_email_input,
            ):
                self.error.setText("Invalid Email")
                return False

            elif not re.search(r"^\d{10}$", national_code_input):
                self.error.setText("Invalid National Code")
                return False

            elif not re.search(r"^[A-z ]{2,}$", location_input):
                self.error.setText("Invalid Location")
                return False

            elif not re.search(r"^[A-z ]{2,}$", type_input):
                self.error.setText("Invalid Type")
                return False

            elif not re.search(r"^[A-z ]{2,}$", address_input):
                self.error.setText("Invalid Address")
                return False

            elif not re.search(
                r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
                password_input,
            ):
                self.error.setText(
                    "8 characters, at least 1 letter, 1 number & 1 special character"
                )
                return False

            elif not password_input == re_password_input:
                self.error.setText("Password and Re-password are not equal")
                return False

            DATABASE(
                restaurant_name_input,
                manager_first_name_input,
                manager_last_name_input,
                restaurant_phone_number_input,
                restaurant_email_input,
                national_code_input,
                password_input,
                "",
                restaurant_name_input,
                type_input,
                address_input,
                datetime.date.today().strftime("%Y-%m-%d"),
                location_input,
            )
            self.clear_restaurant_inputs()
            self.error.setText("Added Successfully.")
        except Exception as e:
            print(e)

    def clear_restaurant_inputs(self):
        self.restaurant_name_input.clear()
        self.manager_first_name_input.clear()
        self.manager_last_name_input.clear()
        self.restaurant_phone_number_input.clear()
        self.restaurant_email_input.clear()
        self.national_code_input.clear()
        self.location_input.clear()
        self.type_input.clear()
        self.address_input.clear()
        password_input = self.password_input.clear()
        re_password_input = self.re_password_input.clear()
        self.error.setText("")

    def show_new_window(self):
        restaurant_name = self.sender().objectName()
        try:
            self.hide()
            self.w = Splash(restaurant_name)
            self.w.show()
        except Exception as e:
            print(e)

    def show_restaurants(self):
        formFrameRestaurants = QFrame()
        self.restaurants = QFormLayout(formFrameRestaurants)
        self.restaurants_area.setWidget(formFrameRestaurants)
        files = [name for name in os.listdir("backend/data") if name.endswith(".db")]
        if len(files) == 0:
            label = QLabel(f"No restaurant has been added yet.")
            label.setStyleSheet(
                'QLabel { font: 10pt "MV Boli"; min-height: 30px; max-height: 30px; min-width: 230px; }'
            )
            self.restaurants.addRow(label)
        else:
            for file in files:
                name = file.replace(".db", "")
                label = QLabel(f"{name}")
                label.setStyleSheet(
                    'QLabel { font: 12pt "MV Boli"; min-height: 30px; max-height: 30px; min-width: 230px; }'
                )

                button = QPushButton(f"Enter", objectName=f"{name}")
                button.setStyleSheet(
                    """QPushButton{
                                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:1 rgb(255, 189, 108), stop:0 rgb(255, 0, 0));
                                            color: white;
                                            font: 12pt "MV Boli";
                                            border: 2px solid rgb(0, 0, 0);
                                            border-radius: 12px;
                                            min-width: 60px;
                                            max-width: 60px;
                                            max-height: 30px;
                                        }
                                        QPushButton:pressed   {
                                            background-color: rgba(255, 0, 0, 255);
                                            color: white;
                                        }
                                    """
                )
                button.clicked.connect(self.show_new_window)
                self.restaurants.addRow(label, button)

    def centralize(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos()
        )
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


app = QApplication(sys.argv)
w = Restaurants()
w.show()
app.exec()

# if __name__ == "__main__":
#    main()
