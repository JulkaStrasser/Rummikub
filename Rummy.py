import sys, random
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow, QFontComboBox, QPlainTextEdit, QColorDialog, QSizePolicy, QRadioButton
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont, QColor, QImage, QPixmap
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QT_VERSION_STR, QPoint, QDir, QEvent
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from Tile import RummyTile
from Cell import BoardCell
from GridArchive import GridArchiveManager
import time
from AnalogTimer import AnalogTimer
import logging
from PyQt5 import QtGui, QtCore,QtWidgets
from Graphics import MyLabel, MyButton
from ControlPanel import ControlPanel,RemainTiles
from Player import PlayerControls, PlayerGrid,Player
from TileGridBase import TileGridBaseClass
from GameBoard import GameBoard



# ++++++++++++++++++++++++++++++++++++++++++++++
#          TILE BAG
# ++++++++++++++++++++++++++++++++++++++++++++++
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

    def getTileFromBag(self):

        if self.tileBag == []:
            return "empty"
        else:
            tile = self.tileBag.pop()
            tile.owner = "board"
            RummyKub.controlPanel.NoOfTilesInBagIndicator.setText(str(len(self.tileBag) - 1))
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


class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
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
    
    if main.players[main.player_turn-1].player_grid.checkWinner() == True:
        # logging.debug('Gracz'+str(main.player_turn)+' jest zwyciezca')
        sys.exit()

    if main.gameBoard.detectSequences() != True:
        pass
    
    else:
        main.players[main.player_turn-1].drawedTile = False
        if main.player_turn == 0:
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
            main.players[1].player_controls.playerGrid.thaw()
            main.players[1].player_controls.FrozenStateLabel.updateText("Twoja tura")
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

        main.player_turn = (main.player_turn+1)%4
    

        
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
    

def getCellCol(cell):
    return cell.getCol()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    RummyKub = MainWin()
    RummyKub.show()
    main.newGame()
    freezePlayers()
   

sys.exit(app.exec_())