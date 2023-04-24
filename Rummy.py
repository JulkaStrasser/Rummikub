import sys, random
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFrame, QHBoxLayout, QGridLayout, QMainWindow, QFontComboBox, QLabel, QRadioButton, QCheckBox, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtGui import QColor
from Tile import RummyTile
from GridArchive import GridArchiveManager
from AnalogTimer import AnalogTimer
import logging
from PyQt5 import QtCore,QtWidgets
from ControlPanel import ControlPanel
from Player import Player
from GameBoard import GameBoard
from History import History
from ClientClass import Client
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator


class TileBag():
    def __init__(self,main):
        self.tileBag = []
        self.nextTileToDeal = 0
        tile = main.tileCollection.getTile()

        while tile != []:
            tile.owner = "bag"
            self.tileBag.append(tile)
            tile = main.tileCollection.getTile()

        random.shuffle(self.tileBag)
        logging.info("Plytki sa przygotowane, pomieszane w worku")
        main.database.write("Wszyscy","Plytki przygotowane do gry")
        main.database.read_all_data()

    def getTileFromBag(self):

        if self.tileBag == []:
            return "empty"
        else:
            tile = self.tileBag.pop()
            tile.owner = "board"
            if window.RummyKub != None:
                window.RummyKub.controlPanel.NoOfTilesInBagIndicator.setText(str(len(self.tileBag) - 1))
            return tile

    def getNoOfTilesInBag(self):
        return len(self.tileBag) - 1

    def newGame(self):
        self.tileBag = []
        self.nextTileToDeal = 0
        tile = main.tileCollection.getTile()

        while tile != []:
            tile.owner = "bag"
            self.tileBag.append(tile)
            tile = main.tileCollection.getTile()

        random.shuffle(self.tileBag)
        logging.debug("Plytki sa w worku")
        logging.debug("Plytki pomieszane")
        random.shuffle(self.tileBag)


class TileCollection():
    def __init__(self,main):
        self.tiles = []
        index = 0
        self.tileColors = main.tileColors
        for n in [1,2]:
            for tileColor in main.tileColors:
                for tileVal in main.tileValues:
                    self.tiles.append(RummyTile(tileColor, tileVal, index))
                    index += 1

    def getTile(self):
        if self.tiles == []:
            return []
        else:
            for tile in self.tiles:
                if tile.owner == "none":
                    return tile
                    break

            return []

    def getTileAtIndex(self, index):
        if index >= len(self.tiles):
            logging.error("Nie ma plytki o indeksie "+ str(index))
            return
        else:
            return self.tiles[index]

    # dorobic tutaj funkcje przeliczajaca tile index, gdy znany jest kolor i numer
    def getTileColorNumber(self,color,number):
        color_to_num = [-1,12,25,38]
        color_index = self.tileColors.index(color)
        if color_index == -1:
            print("Nie ma takiego koloru!")
        tile_index = color_to_num[color_index]+number
        print("getTileColorNumber"+str(tile_index))
        return tile_index
    
    def printTileList(self):
        for tile in self.tiles:
            fred1 = str(tile.MasterIndex)
            fred2 = str(tile.color)
            fred3 = str(tile.value)
            fred4 = str(tile.owner)
            cellStr = fred1 + " - " + fred2 + " " + fred3 + " owner = " + fred4
            
    def clearTiles(self):
        for tile in self.tiles:
            tile.owner = "none"


class TileDestinations():
    def __init__(self):
        self.validDestinations = []


class MyView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent=parent)

        self.scene = QGraphicsScene(self)
        self.item = QGraphicsRectItem(200,300,1000,800)
        self.scene.addItem(self.item)
        self.setScene(self.scene)


class ConfigWindow(QWidget):
    def __init__(self,main):
        super().__init__()
        self.main = main
        self.RummyKub = None  # No external window yet.
        self.noPlayersLabel = QLabel("Wybierz ilosc graczy")
        self.two_players = QRadioButton("2 graczy")
        self.two_players.toggled.connect(self.change_2players)
        self.three_players = QRadioButton("3 graczy")
        self.three_players.toggled.connect(self.change_3players)

        self.playerAI = QRadioButton("zagraj z AI")

        self.saveHistLabel = QLabel("Wybierz format zapisu historii gry")

        self.histsql = QCheckBox('sqlite3')
        self.histsql.setChecked(True)
        self.histsql.stateChanged.connect(self.sqlOption)

        self.histjson = QCheckBox('json')
        self.histjson.setChecked(True)
        self.histjson.stateChanged.connect(self.jsonOption)

        self.histxml = QCheckBox('xml')
        self.histxml.setChecked(True)
        self.histjson.stateChanged.connect(self.xmlOption)

        # Network config
        self.networkLabel = QLabel("Laczenie z siecia")
        ip_input = QLabel('Adres IP :', self)
        self.ip_input = QLineEdit(self)
        self.ip_input.returnPressed.connect(self.validate_input)

        ip_regex = QRegExp("(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
        ip_validator = QRegExpValidator(ip_regex, self.ip_input)
        self.ip_input.setValidator(ip_validator)

        port_input = QLabel('Port Number:', self)
        self.port_input = QLineEdit(self)
        # Set the maximum length of the QLineEdit to 5 (the maximum length of a port number)
        self.port_input.setMaxLength(5)

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
        hbox5 = QHBoxLayout()
        hbox6 = QHBoxLayout()

        hbox0.addWidget(self.noPlayersLabel)
        hbox1.addWidget(self.two_players)
        hbox1.addWidget(self.three_players)
        hbox1.addWidget(self.playerAI)
        hbox2.addWidget(self.saveHistLabel)
        
        hbox3.addWidget(self.histsql)
        hbox3.addWidget(self.histjson)
        hbox3.addWidget(self.histxml)

        hbox4.addWidget(self.networkLabel)
        hbox5.addWidget(ip_input)
        hbox5.addWidget(self.ip_input)
        hbox5.addWidget(port_input)
        hbox5.addWidget(self.port_input)

        hbox6.addWidget(self.playButton)
        

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)

        self.setLayout(vbox)

        # Set window properties
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Okno Konfiguracyjne')

    def show_new_window(self, checked):
        if self.RummyKub is None:
            self.RummyKub = MainWin()
            self.RummyKub.show()
            self.hide()

        else:
            self.RummyKub.close()  # Close window.
            self.RummyKub = None  # Discard reference.

    def change_2players(self):
        self.main.noPlayers = 2

    def change_3players(self):
        self.main.noPlayers = 3

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

    def sqlOption(self):
        self.main.isSQL = not(self.main.isSQL)
    
    def xmlOption(self):
        self.main.isXML = not(self.main.isXML)
    
    def jsonOption(self):
        self.main.isJson = not(self.main.isJson)

class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        self.setWindowTitle("Rummy Client")
        self.view=MyView()
        self.setCentralWidget(self.view)
        self.controlPanel = ControlPanel(main)

        #Add to grid layout
        self.gameLayout = QGridLayout()
        self.gameLayout.addWidget(main.players[0].player_grid, 0, 0)
        self.gameLayout.addWidget(main.players[0].player_controls, 0, 1)

        self.gameLayout.addWidget(main.players[2].player_grid, 0, 2)
        self.gameLayout.addWidget(main.players[2].player_controls, 0, 3)

        self.gameLayout.addWidget(main.gameBoard, 1, 0, 3, 3)

        self.gameLayout.addWidget(main.players[1].player_grid, 4, 0)
        self.gameLayout.addWidget(main.players[1].player_controls, 4, 1)

        self.gameLayout.addWidget(main.players[3].player_grid, 4, 2)
        self.gameLayout.addWidget(main.players[3].player_controls, 4, 3)
        
        self.gameLayout.addWidget(self.controlPanel, 1, 3, 2 ,1)

        self.AnalogTimer = AnalogTimer()
        self.AnalogTimer.setGeometry(QtCore.QRect(110, 290, 200, 200))
        self.gameLayout.addWidget(self.AnalogTimer, 3, 3, 1 ,1)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.gameLayout)

        self.setCentralWidget(self.mainWidget)

        
class FontSelector(QWidget):
    def __init__(self):
        super(FontSelector, self).__init__()
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout = QHBoxLayout(self.frame)

        self.textBold = QPushButton(self.frame)
        self.textBold.setMaximumSize(QtCore.QSize(25, 25))
        self.textBold.setCheckable(True)
        self.textBold.setText("B")
        self.horizontalLayout.addWidget(self.textBold)

        self.textItalic = QPushButton(self.frame)
        self.textItalic.setMaximumSize(QtCore.QSize(25, 25))
        self.textItalic.setCheckable(True)
        self.textItalic.setText("I")
        self.horizontalLayout.addWidget(self.textItalic)

        self.textUnderline = QPushButton(self.frame)
        self.textUnderline.setMaximumSize(QtCore.QSize(25, 25))
        self.textUnderline.setCheckable(True)
        self.textUnderline.setText("U")
        self.horizontalLayout.addWidget(self.textUnderline)

        self.fontComboBox = QFontComboBox(self.frame)
        self.horizontalLayout.addWidget(self.fontComboBox)
        self.setLayout(self.horizontalLayout)

    

def freezePlayers():
    
    main.change = False
    noPlayers = main.noPlayers 
    
    
    if main.players[main.player_turn-1].player_grid.checkWinner() == True:
        # logging.debug('Gracz'+str(main.player_turn)+' jest zwyciezca')
        main.database.write("Gracz "+str(main.player_turn), "jest zwyciezca")
        sys.exit()

    if main.gameBoard.detectSequences() != True:
        pass
    
    else:
        # zapisywanie i wysylanie planszy do serwera
        

        main.players[main.player_turn-1].drawedTile = False
        main.database.write('Gracz'+str(main.player_turn+1),'Twoja tura')
        main.database.read_all_data()

       
        if main.player_turn == 0:
            #poczatek tury gracza 1 - czytamy dane od servera
            received_grid = main.client.Tcp_Read()
            main.gameBoard.restoreGridState(main.client.grid)
            #print(str(received_mes))
            #budzimy playera 1
            main.players[0].player_controls.playerGrid.thaw()
            main.players[0].player_controls.FrozenStateLabel.updateText("Twoja tura")
            main.players[0].player_controls.setEnabled(True)

            main.players[1].player_controls.playerGrid.freeze()
            main.players[1].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            main.players[1].player_controls.setEnabled(False)

            main.players[2].player_controls.playerGrid.freeze()
            main.players[2].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            main.players[2].player_controls.setEnabled(False)

            main.players[3].player_controls.playerGrid.freeze()
            main.players[3].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            main.players[3].player_controls.setEnabled(False)

        elif(main.player_turn == 1):
            main.gameBoard.listItems()
            data = main.client.read_json_file('GameBoard.json')
            main.client.Tcp_Write(data)
            main.players[1].player_controls.playerGrid.thaw()
            main.players[1].player_controls.FrozenStateLabel.updateText("Poczekaj! Tura gracza 2")
            main.players[1].player_controls.setEnabled(True)

            main.players[0].player_controls.playerGrid.freeze()
            main.players[0].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            main.players[0].player_controls.setEnabled(False)

            main.players[2].player_controls.playerGrid.freeze()
            main.players[2].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            main.players[2].player_controls.setEnabled(False)

            main.players[3].player_controls.playerGrid.freeze()
            main.players[3].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            main.players[3].player_controls.setEnabled(False)

        elif(main.player_turn == 2):
            main.players[2].player_controls.playerGrid.thaw()
            main.players[2].player_controls.FrozenStateLabel.updateText("Twoja tura")
            main.players[2].player_controls.setEnabled(True)
            
            main.players[0].player_controls.playerGrid.freeze()
            main.players[0].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            main.players[0].player_controls.setEnabled(False)

            main.players[1].player_controls.playerGrid.freeze()
            main.players[1].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            main.players[1].player_controls.setEnabled(False)

            main.players[3].player_controls.playerGrid.freeze()
            main.players[3].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            main.players[3].player_controls.setEnabled(False)
        elif(main.player_turn == 3):
            main.players[3].player_controls.playerGrid.thaw()
            main.players[3].player_controls.FrozenStateLabel.updateText("Twoja tura")
            main.players[3].player_controls.setEnabled(True)

            main.players[0].player_controls.playerGrid.freeze()
            main.players[0].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            main.players[0].player_controls.setEnabled(False)

            main.players[2].player_controls.playerGrid.freeze()
            main.players[2].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            main.players[2].player_controls.setEnabled(False)

            main.players[1].player_controls.playerGrid.freeze()
            main.players[1].player_controls.FrozenStateLabel.updateText("Nie twoja tura")
            main.players[1].player_controls.setEnabled(False)

        main.player_turn = (main.player_turn+1)%noPlayers
    

        
class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class LoggingWindow(QtWidgets.QDialog, QtWidgets.QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)

        logTextBox = QTextEditLogger(self)
        
        logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('rumikub.log')
        logging.getLogger().addHandler(logTextBox)
        logging.getLogger().addHandler(c_handler)
        logging.getLogger().addHandler(f_handler)

        logging.getLogger().setLevel(logging.INFO)
        layout = QtWidgets.QVBoxLayout()
        

        layout.addWidget(logTextBox.widget)
        self.setLayout(layout)

        self.show()
        self.raise_()
        self.app = QtWidgets.QApplication(sys.argv)
       
        LoggingWindow.instance = self

class Main():
    def __init__(self):
         #history
        self.isSQL = True
        self.isXML = True
        self.isJson = True
        
        self.noPlayers = 4 #default number of players
        self.database = History(self)
        self.tileColors = ["red", "black", "blue", "yellow"]
        self.tileOwner = ["none", "player", "board", "bag"]
        self.tileValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.numberOfColumns = 15
        self.numberOfTilesToDeal = 15
        self.player_turn = 0
        self.change = False

       

        self.players_first_turn = [True,True,True,True]
        # app = QApplication(sys.argv)
        self.dlg = LoggingWindow()

        self.playerBgColor = QColor('#A5A5A5')
        self.playerFgColor = QColor('#000000')

        self.boardBgColor = QColor('#F2F2F2')
        self.boardFgColor = QColor('#A5A5A5')

        self.players = []
        self.players.append(Player(0,'Gracz 1',True,self))
        self.players[0].player_controls.FreezeButton.clicked.connect(freezePlayers)
        
        self.players.append(Player(1,'Gracz 2', True,self)) 
        self.players[1].player_controls.FreezeButton.clicked.connect(freezePlayers)

        self.players.append(Player(2,'Gracz 3', True,self))
        self.players[2].player_controls.FreezeButton.clicked.connect(freezePlayers)

        self.players.append(Player(3,'Gracz 4', True,self))
        self.players[3].player_controls.FreezeButton.clicked.connect(freezePlayers)


        self.gameBoard = GameBoard(self.boardBgColor, self.boardFgColor, "GameBoard", 8, self.numberOfColumns*2,self)

        self.gridArchiveManager = GridArchiveManager(self.players[0].player_grid, self.players[1].player_grid, self.players[2].player_grid, self.players[3].player_grid, self.gameBoard)

        self.tileCollection = TileCollection(self)

        self.tileBag = TileBag(self)
        self.client = Client('172.16.35.55', 17098,self)
        self.client.Tcp_connect()

    def newGame(self):
        self.gameBoard.removeAllTiles()
        self.players[0].player_grid.removeAllTiles()
        self.players[1].player_grid.removeAllTiles()
        self.players[2].player_grid.removeAllTiles()
        self.players[3].player_grid.removeAllTiles()
        self.tileCollection.clearTiles() 
        self.tileBag.newGame()
        self.players[0].player_grid.newDeal()
        self.players[1].player_grid.newDeal()
        self.players[2].player_grid.newDeal()
        self.players[3].player_grid.newDeal()

        #do testowania
        # self.tileCollection.getTileColorNumber("red",1)
    

def getCellCol(cell):
    return cell.getCol()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    # RummyKub = MainWin()
    # RummyKub.show()
    window = ConfigWindow(main)
    window.show()
    main.newGame()
    freezePlayers()
    
   
# main.database.close()
sys.exit(app.exec_())
