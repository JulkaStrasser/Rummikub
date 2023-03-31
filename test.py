from PyQt5 import QtGui, QtCore
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsRectItem
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow

# zeby Czubik sie nie czepial, ze nie ma QGraphics Scene

class MyView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent=parent)

        self.scene = QGraphicsScene(self)
        self.item = QGraphicsRectItem(0,0,1000,800)
        self.scene.addItem(self.item)
        self.setScene(self.scene)

class Window(QMainWindow):
    def __init__(self):
        #This initializes the main window or form
        super(Window,self).__init__()
        self.setGeometry(50,50,900,700)
        self.setWindowTitle("Pre-Alignment system")
        #create the view
        self.view=MyView()
        self.setCentralWidget(self.view)

if __name__=='__main__':
    app = QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())