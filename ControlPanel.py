import sys, random
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow, QFontComboBox, QPlainTextEdit, QColorDialog, QSizePolicy

from PyQt5.QtGui import QFont, QColor, QImage, QPixmap
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QT_VERSION_STR, QPoint, QDir, QEvent

# from Tile import RummyTile
# from Cell import BoardCell
# from GridArchive import GridArchiveManager
from Rummy import *

class ControlPanel(QFrame):
    def __init__(self):

        super(ControlPanel, self).__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.layout = QVBoxLayout()
        self.layout.setAlignment((QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop))
        self.setLayout(self.layout)
        self.setMinimumHeight(300)
        self.setMinimumWidth(140)
        self.buttonBar = QVBoxLayout()

        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # Create buttons
        # ++++++++++++++++++++++++++++++++++++++++++++++++

        self.newGameButton = MyButton("Nowa gra")
        self.newGameButton.clicked.connect(self.newGame)

        self.ExitButton = MyButton("Wyjscie")
        self.ExitButton.clicked.connect(self.Exit)

        self.SaveGameStateButton = MyButton("Zapisz")
        self.SaveGameStateButton.clicked.connect(self.saveBoardState)

        self.RestoreGameStateButton = MyButton("Odswiez")
        self.RestoreGameStateButton.clicked.connect(self.restoreBoardState)

        self.buttonBar.addWidget(self.newGameButton)
        self.buttonBar.addWidget(self.ExitButton)
        self.buttonBar.addWidget(self.SaveGameStateButton)
        self.buttonBar.addWidget(self.RestoreGameStateButton)

        self.layout.addLayout(self.buttonBar)
        self.infoBar = QVBoxLayout()
        self.layout.setAlignment((QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop))

        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # Create info box
        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # self.tilesLeftInfoBox = QPlainTextEdit()
        # tileLeftFont = QFont("Consolas", 10)
        # self.tilesLeftInfoBox.setFont(tileLeftFont)
        # self.tilesLeftInfoBox.setPlainText("All tiles in bag")
        # self.infoBar.addWidget(self.tilesLeftInfoBox)
        # self.layout.addLayout(self.infoBar)

        self.NoOfTilesInBagIndicator = RemainingTilesIndicator2("hjhh")
        self.layout.addWidget(self.NoOfTilesInBagIndicator)
        self.NoOfTilesInBagIndicator.updateText("0")

    def masterTileList(self):
        tileCollection.printTileList()

    def listBoard(self):
        self.tilesLeftInfoBox.clear()
        for cell in gameBoard.cellList:
            index = cell.getCellListIndex()
            cellStr = str(index) + " - " + str(cell.getCellStatus())
            self.tilesLeftInfoBox.appendPlainText(cellStr)

    def takeTile(self):
        print("Taking a tile")
        if tileBag.getNoOfTilesInBag() > 0:
            nextTile = tileBag.getTileFromBag()
            gameBoard.AddTileFromBag(nextTile)


    def Exit(self):
        print("Exiting....")
        sys.exit()

    def setNumberOfTiles(self, NoOfTiles):
        tempStr = str(NoOfTiles) + " tiles left in bag"
        self.tilesLeftInfoBox.setPlainText(tempStr)

    def clearInfoBox(self):
        self.tilesLeftInfoBox.clear()

    def appendInfo(self, tempStr):
        self.tilesLeftInfoBox.appendPlainText(tempStr)

    def saveBoardState(self):
        gridArchiveManager.saveGameState()

    def saveBoardState(self):
        gridArchiveManager.saveGameState()

    def restoreBoardState(self):
        gridArchiveManager.restoreGameState()
