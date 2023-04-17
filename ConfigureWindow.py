import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox, QRadioButton
from random import randint
class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.
        self.noPlayersLabel = QLabel("Wybierz ilosc graczy")
        self.two_players = QRadioButton("2 graczy")
        # self.two_players.toggled.connect(self.change_2players)
        self.three_players = QRadioButton("3 graczy")
        #self.three_players.toggled.connect(self.change_3players)

        self.playerAI = QRadioButton("zagraj z AI")

        self.saveHistLabel = QLabel("Wybierz format zapisu historii gry")

        self.histsql = QCheckBox('sqlite3')
        self.histsql.setChecked(True)
        self.histjson = QCheckBox('json')
        self.histjson.setChecked(True)
        self.histxml = QCheckBox('xml')
        self.histxml.setChecked(True)

        # Create buttons
        self.playButton = QPushButton('Zacznij gre')
        self.playButton.clicked.connect(self.show_new_window)

        # Create layout
        vbox = QVBoxLayout()
        hbox0 = QHBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()

        hbox0.addWidget(self.noPlayersLabel)
        hbox1.addWidget(self.two_players)
        hbox1.addWidget(self.three_players)
        hbox1.addWidget(self.playerAI)
        hbox2.addWidget(self.saveHistLabel)
        
        hbox3.addWidget(self.histsql)
        hbox3.addWidget(self.histjson)
        hbox3.addWidget(self.histxml)

        hbox4.addWidget(self.playButton)
        

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        self.setLayout(vbox)

        # Set window properties
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('My Window')

    def show_new_window(self, checked):
        if self.w is None:
            self.w = AnotherWindow()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConfigWindow()
    window.show()
    sys.exit(app.exec_())

