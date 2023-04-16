from PyQt5.QtWidgets import  QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame,QVBoxLayout, QRadioButton, QMessageBox,QApplication,QGridLayout
from PyQt5 import QtCore
from Graphics import MyButton,MyLabel
from PyQt5.QtGui import QFont, QColor
import logging
from Cell import BoardCell
from TileGridBase import TileGridBaseClass

class PlayerControls(QFrame):
    def __init__(self, bgColor, fgColor, playerGrid, playerName,main):
        super(PlayerControls, self).__init__()
        self.main = main
        self.playerGrid = playerGrid
        self.playerName = playerName
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.layout = QVBoxLayout()
        self.layout.setAlignment((QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop))
        self.setLayout(self.layout)

        self.TakeTileButton = MyButton("Dobierz plytke")
        self.TakeTileButton.clicked.connect(self.takeTile)

        self.FreezeButton = MyButton("Zakoncz ture")

        self.FrozenStateLabel = MyLabel("Twoja tura")

        self.playerNameLabel = MyLabel(playerName)

        self.layout.addWidget(self.playerNameLabel)
        self.layout.addWidget(self.TakeTileButton)
        self.layout.addWidget(self.FreezeButton)
        self.layout.addWidget(self.FrozenStateLabel)

        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), bgColor)
        self.pal.setColor(self.foregroundRole(), fgColor)
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

    def freeze(self):
        logging.debug(self.playerName[6])
        if self.main.player_turn == int(self.playerName[6])-1:
            if self.playerGrid.isFrozen():
                self.playerGrid.thaw()
                self.FrozenStateLabel.updateText("Twoja tura")
            else:
                self.playerGrid.freeze()
                self.FrozenStateLabel.updateText("Nie twoja tura")
                self.main.change = True
                self.main.player_turn = (self.main.player_turn+1) % 4
                logging.debug(self.main.change)

    def setBackgroundColor(self, color):
        self.pal.setColor(self.backgroundRole(), QColor(color))
        self.setPalette(self.pal)
        for cell in self.cellList:
            cell.setBackgroundColor(color)

    def takeTile(self, tile):
        if self.main.players[self.main.player_turn-1].drawedTile == False:
            if self.main.tileBag.getNoOfTilesInBag() > 0:
                nextTile = self.main.tileBag.getTileFromBag()
                logging.info(self.playerName + " dobiera plytke. To:  " + str(nextTile.getColor()) + str(nextTile.getValue()))
                for cell in self.playerGrid.cellList:
                    status = cell.getCellStatus()
                    if status == "Empty":
                        cell.addTile(nextTile)
                        self.main.players[self.main.player_turn-1].drawedTile = True
                        break

    def getPlayerName(self):
        return self.playerName


class PlayerGrid(TileGridBaseClass):
    def __init__(self, bgColor, fgColor, gridName, rows, cols, main):
        self.main = main
        super(PlayerGrid, self).__init__(rows, cols, bgColor, fgColor, gridName)
        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), bgColor)
        self.pal.setColor(self.foregroundRole(), fgColor)  
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

    def newDeal(self):
        
        for n in range(self.main.numberOfTilesToDeal):
            if self.main.tileBag.getNoOfTilesInBag() > 0:
                nextTile = self.main.tileBag.getTileFromBag()
                logging.info( " dobieranie plytki. Jest to : " + str(nextTile.getColor()) + str(nextTile.getValue()))
                for cell in self.cellList:
                    status = cell.getCellStatus()
                    if status == "Empty":
                        cell.addTile(nextTile)
                        break
            else:
                logging.info("Worek z plytkami jest pusty!")
                break

    def checkWinner(self):
        isWinner = True
        for cell in self.cellList:
                status = cell.getCellStatus()
                if status != "Empty":
                    isWinner = False
                    break
        if isWinner == True:
            QMessageBox.information(self,'Koniec gry','Zwyciezyl gracz '+ str(self.main.player_turn))
            logging.info("Koniec gry. Zwyciezyl gracz "+ str(self.main.player_turn))
        return isWinner
    
    
