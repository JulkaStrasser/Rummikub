#INPUT IP ADDRES I PORT
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QMessageBox,QLabel
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

class IPInput(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        ip_input = QLabel('Adres IP :', self)
        self.ip_input = QLineEdit(self)
        self.ip_input.returnPressed.connect(self.validate_input)

        # Set the input mask to restrict user input to an IP address format
        ip_regex = QRegExp("(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
        ip_validator = QRegExpValidator(ip_regex, self.ip_input)
        self.ip_input.setValidator(ip_validator)

        layout = QVBoxLayout()
        layout.addWidget(ip_input)
        layout.addWidget(self.ip_input)

         # Create a label to describe the ineEdit
        port_input = QLabel('Port Number:', self)
        # Create the QLineEdit widget and set its initial text to '8080'
        self.port_input = QLineEdit(self)
        
        # Set the maximum length of the QLineEdit to 5 (the maximum length of a port number)
        self.port_input.setMaxLength(5)

        layout.addWidget(port_input)
        layout.addWidget(self.port_input)
        self.setLayout(layout)

    def validate_input(self):
        ip_address = self.ip_input.text()
        if not ip_address:
            QMessageBox.warning(self, "Invalid Input", "Please enter an IP address.")
            return
        else:
            octets = ip_address.split('.')
            if len(octets) != 4:
                QMessageBox.warning(self, "Invalid Input", "The IP address must have four octets.")
                return
            for octet in octets:
                if not octet.isdigit() or int(octet) < 0 or int(octet) > 255:
                    QMessageBox.warning(self, "Invalid Input", "Each octet must be an integer between 0 and 255.")
                    return
        QMessageBox.information(self, "Valid Input", "The entered IP address is valid.")

if __name__ == '__main__':
    app = QApplication([])
    ip_input = IPInput()
    ip_input.show()
    app.exec_()



