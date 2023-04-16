from PyQt5.QtWidgets import QPushButton,QLabel
from PyQt5.QtGui import QFont, QColor

class MyButton(QPushButton):
    def __init__(self, text):
        super(MyButton, self).__init__()
        self.setFixedWidth(120)
        self.setFixedHeight(25)
        self.setFont(QFont('SansSerif', 10))
        self.setText(text)


class MyLabel(QLabel):
    def __init__(self, legend):
        super(MyLabel, self).__init__()

        self.setText(legend)

        self.setFont(QFont('SansSerif', 12))
        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), QColor('#F2F2F2'))
        self.pal.setColor(self.foregroundRole(), QColor('#B30000')) 
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

    def updateText(self, newText):
        self.setText(newText)