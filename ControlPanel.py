from PyQt5.QtWidgets import  QLineEdit, QLabel, QFrame,QVBoxLayout, QRadioButton, QMessageBox,QApplication
import logging
from PyQt5 import QtCore
from Graphics import MyButton
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import sys
from PyQt5.QtGui import QFont, QColor
from GamePlayback import PlayBack

class RemainTiles(QLabel):
    def __init__(self, legend):
        super(RemainTiles, self).__init__()

        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(3)
       

        self.setText(legend)

        self.setFont(QFont('SansSerif', 18))
        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), QColor('#F2F2F2'))
        self.pal.setColor(self.foregroundRole(), QColor('#000000'))
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

    def updateText(self, newText):
        self.setText(newText)

class ControlPanel(QFrame):
    def __init__(self,params):
        self.params = params
        super(ControlPanel, self).__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.layout = QVBoxLayout()
        self.layout.setAlignment((QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop))
        self.setLayout(self.layout)
        self.setMinimumHeight(300)
        self.setMinimumWidth(140)
        self.buttonBar = QVBoxLayout()

        self.playback = PlayBack()
        self.is_disp_playback = False
        #BUTTONS
        self.newGameButton = MyButton("Nowa gra")
        self.newGameButton.clicked.connect(params.newGame)

        self.ExitButton = MyButton("Wyjscie")
        self.ExitButton.clicked.connect(self.Exit)

        self.SaveHistoryButton = MyButton("Zapisz historie gry")
        self.SaveHistoryButton.clicked.connect(self.playback.save_game)

        self.PlaybackButton = MyButton("Playback historii")
        self.PlaybackButton.clicked.connect(self.playback_options)
   

        # ip_input = QLabel('Adres IP :', self)
        # self.ip_input = QLineEdit(self)
        # self.ip_input.returnPressed.connect(self.validate_input)

        # ip_regex = QRegExp("(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
        # ip_validator = QRegExpValidator(ip_regex, self.ip_input)
        # self.ip_input.setValidator(ip_validator)

        # port_input = QLabel('Port Number:', self)
        # self.port_input = QLineEdit(self)
        # # Set the maximum length of the QLineEdit to 5 (the maximum length of a port number)
        # self.port_input.setMaxLength(5)

    
        
        # self.buttonBar.addWidget(ip_input)
        # self.buttonBar.addWidget(self.ip_input)

        # self.buttonBar.addWidget(port_input)
        # self.buttonBar.addWidget(self.port_input)

        self.buttonBar.addWidget(self.newGameButton)
        self.buttonBar.addWidget(self.ExitButton)
        self.buttonBar.addWidget(self.SaveHistoryButton)
        self.buttonBar.addWidget(self.PlaybackButton)
       
        
        self.layout.addLayout(self.buttonBar)
        self.infoBar = QVBoxLayout()
        self.layout.setAlignment((QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop))

        self.NoOfTilesInBagIndicator = RemainTiles("hjhh")
        self.layout.addWidget(self.NoOfTilesInBagIndicator)
        self.NoOfTilesInBagIndicator.updateText("0")

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

    def masterTileList(self):
        self.params.tileCollection.printTileList()

    def listBoard(self):
        self.tilesLeftInfoBox.clear()
        for cell in self.params.gameBoard.cellList:
            index = cell.getCellListIndex()
            cellStr = str(index) + " - " + str(cell.getCellStatus())
            self.tilesLeftInfoBox.appendPlainText(cellStr)

    def takeTile(self):
        if self.params.tileBag.getNoOfTilesInBag() > 0:
            nextTile = self.params.tileBag.getTileFromBag()
            self.params.gameBoard.AddTileFromBag(nextTile)


    def Exit(self):
        logging.info('Wyjscie z programu')
        sys.exit()

    def setNumberOfTiles(self, NoOfTiles):
        tempStr = str(NoOfTiles) + " tiles left in bag"
        self.tilesLeftInfoBox.setPlainText(tempStr)

    def clearInfoBox(self):
        self.tilesLeftInfoBox.clear()

    def appendInfo(self, tempStr):
        self.tilesLeftInfoBox.appendPlainText(tempStr)

    def saveBoardState(self):
        self.params.gridArchiveManager.saveGameState()

    def saveBoardState(self):
        self.params.gridArchiveManager.saveGameState()

    def restoreBoardState(self):
        self.params.gridArchiveManager.restoreGameState()

    def playback_options(self):
        # if self.is_disp_playback == False:
        #     self.playback.save_game()
        #     self.playback.stop()
        #     self.is_disp_playback = True
        # else:
        self.playback.display_history()
            # self.is_disp_playback = False




if __name__ == '__main__':
    app = QApplication(sys.argv)
    exit(app.exec_())