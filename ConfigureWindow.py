import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox, QRadioButton

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

