from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QDesktopWidget, QFrame, QFormLayout, QLabel, QPushButton
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread , pyqtSignal, pyqtSlot
from PyQt5.uic import loadUi
import sys , random, time
from frontend.ui_class.login import LoginScreen
from frontend.ui_class.signup import SignUpScreen
from frontend.ui_class.customer import MainScreen
from frontend.ui_class.manager import  ManagerScreen

indexes = {"LoginScreen": 0, "SignUpScreen": 1, "MainScreen": 2 , "ManagerScreen": 3}

def main():
    try:
        #app = QApplication(sys.argv)

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

        #widget.show()
        return widget

        #sys.exit(app.exec_())

    except Exception as error:
        print(error)
        
class ThreadProgress(QThread):
    mysignal = pyqtSignal(int)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        
    def run(self):
        i = 0
        while i<101:
            time.sleep(0.03)
            self.mysignal.emit(i)
            i += 1
            
class Splash(QDialog):
    def __init__(self, restaurant_name, parent = None):
        super(Splash, self).__init__(parent)
        
        self.load_int = random.randint(40, 80)
        
        loadUi("frontend/ui_files/SplashScreen.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralize()

        pixmap = QtGui.QPixmap("frontend/icons/restaurant.png").scaled(320, 320)
        self.logo.setPixmap(pixmap)

        self.restaurant_name.setText(restaurant_name)
        
        progress = ThreadProgress(self)
        progress.mysignal.connect(self.progress)
        progress.start()
        
    @pyqtSlot(int)
    def progress(self, i):
        self.progressBar.setValue(i)
        if i == self.load_int:
            self.w_l = main()
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
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.tabWidget.setCurrentIndex(0)
        self.centralize()
        
        self.show_restaurants()
        
        pixmap = QtGui.QPixmap("frontend/icons/restaurant_info.png").scaled(350, 100)
        self.restaurant_info_header.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("frontend/icons/restaurants.png").scaled(350, 100)
        self.restaurants_header.setPixmap(pixmap)
        
        self.restaurants_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.restaurants_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.add_new_restaurant.clicked.connect(self.add_new_restaurant_button)
        
        self.exit_button.clicked.connect(lambda x: sys.exit())

        self.tabWidget.tabBarClicked.connect(self.handle_tabbar_clicked)
        
    def handle_tabbar_clicked(self, index):
        if index == 0:
            self.show_restaurants()
        elif index == 1:
            self.clear_restaurant_inputs()
            
    def add_new_restaurant_button(self):
        print(self.restaurant_name_input.text(),
        self.manager_first_name_input.text(),
        self.manager_last_name_input.text(),
        self.restaurant_phone_number_input.text(),
        self.restaurant_email_input.text(),
        self.location_input.text(),
        self.type_input.text(),
        self.address_input.text())

        self.clear_restaurant_inputs()
        
    def clear_restaurant_inputs(self):
        self.restaurant_name_input.clear()
        self.manager_first_name_input.clear()
        self.manager_last_name_input.clear()
        self.restaurant_phone_number_input.clear()
        self.restaurant_email_input.clear()
        self.location_input.clear()
        self.type_input.clear()
        self.address_input.clear()
        
    def show_new_window(self):
        restaurant_name = self.sender().objectName()
        try:
            self.hide()
            self.w = Splash(restaurant_name)
            self.w.show()
        except Exception as e:
            print(e)

    def show_restaurants(self):
        print(0)
        formFrameRestaurants = QFrame()
        self.restaurants = QFormLayout(formFrameRestaurants)
        self.restaurants_area.setWidget(formFrameRestaurants)
        for i in range(40):
            label = QLabel(
                f"label{i} {random.randint(3, 90)}"
            )
            label.setStyleSheet('QLabel { font: 8pt "MV Boli"; min-height: 30px; max-height: 30px; min-width: 230px; }')

            button = QPushButton(f"Enter", objectName=f"label{i}")
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

#if __name__ == "__main__":
#    main()
