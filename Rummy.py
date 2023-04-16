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



# GAME BOARD
class TileGridBaseClass(QFrame):
    def __init__(self, rows, cols, bgColor, fgColor, gridName):
        super(TileGridBaseClass, self).__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.tileGrid = QGridLayout()
        self.tileGrid.setHorizontalSpacing(0)
        self.tileGrid.setVerticalSpacing(0)
        self.rows = rows
        self.cols = cols
        self.cellList = []
        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), bgColor)
        self.pal.setColor(self.foregroundRole(), fgColor)
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)
        self.frozen = False
        for row in range(self.rows):
            for col in range(self.cols):
                newCell = BoardCell(row, col, bgColor, fgColor, gridName)
                self.tileGrid.addWidget(newCell, row, col)  
                self.cellList.append(newCell)
        self.setLayout(self.tileGrid)

        # tell each cell who it's neighbours are
        for n in range(len(self.cellList)):
            cell = self.cellList[n]
            (row, col) = cell.getPosition()
            if col == 0:
                left = None
                right = self.cellList[n+1]
            elif col == self.cols - 1:
                left = self.cellList[n - 1]
                right = None
                
            else:
                left = self.cellList[n - 1]
                right = self.cellList[n + 1]
            cell.setNeighbours(left, right)

    def isFrozen(self):
        return self.frozen

    def freeze(self):
        self.frozen = True
        for cell in self.cellList:
            cell.freeze()

    def thaw(self):
        self.frozen = False
        for cell in self.cellList:
            cell.thaw()

    def setBackgroundColor(self, color):
        self.pal.setColor(self.backgroundRole(), QColor(color))
        self.setPalette(self.pal)
        for cell in self.cellList:
            cell.setBackgroundColor(color)

    def setForegroundColor(self, color):
        self.pal.setColor(self.foregroundRole(), QColor(color))
        self.setPalette(self.pal)
        for cell in self.cellList:
            cell.setForegroundColor(color)

    def removeAllTiles(self):
        logging.debug("Usun wszystkie plytki z planszy")
        for cell in self.cellList:
            cell.removeTile()

    def getGridState(self):
        gridState = []
        for cell in self.cellList:
            tileIndex = cell.getTileMasterIndex()
            gridState.append(tileIndex)
        return gridState

    def restoreGridState(self, grid):
        self.removeAllTiles()
        if len(self.cellList) != len(grid):
            logging.error("Problem z zaladowaniem planszy ")
            return
        for n in range(len(grid)):
            index = grid[n]
            if index is not None:
                tile = main.tileCollection.getTileAtIndex(index)
                self.cellList[n].addTile(tile)


class PlayerControls(QFrame):
    def __init__(self, bgColor, fgColor, playerGrid, playerName):
        super(PlayerControls, self).__init__()
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
        if main.player_turn == int(self.playerName[6])-1:
            if self.playerGrid.isFrozen():
                self.playerGrid.thaw()
                self.FrozenStateLabel.updateText("Twoja tura")
            else:
                self.playerGrid.freeze()
                self.FrozenStateLabel.updateText("Nie twoja tura")
                main.change = True
                main.player_turn = (main.player_turn+1) % 4
                logging.debug(main.change)

    def setBackgroundColor(self, color):
        self.pal.setColor(self.backgroundRole(), QColor(color))
        self.setPalette(self.pal)
        for cell in self.cellList:
            cell.setBackgroundColor(color)

    def takeTile(self, tile):
        if main.players[main.player_turn-1].drawedTile == False:
            if main.tileBag.getNoOfTilesInBag() > 0:
                nextTile = main.tileBag.getTileFromBag()
                logging.info(self.playerName + " dobiera plytke. To:  " + str(nextTile.getColor()) + str(nextTile.getValue()))
                for cell in self.playerGrid.cellList:
                    status = cell.getCellStatus()
                    if status == "Empty":
                        cell.addTile(nextTile)
                        main.players[main.player_turn-1].drawedTile = True
                        break

    def getPlayerName(self):
        return self.playerName


class GameBoard(TileGridBaseClass):
    def __init__(self, bgColor, fgColor, gridName, rows, cols):
        super(GameBoard, self).__init__(rows, cols, bgColor, fgColor, gridName)
        self.listItems()
        self.all_sequences = []

    def listItems(self):
        logging.debug("Lista plytek na planszy:")
        cellsList = self.findChildren(BoardCell)
        for cell in cellsList:
            logging.debug(str(cell.row) + str(cell.col))
            status = cell.getCellStatus()
            logging.debug(status[0])
            logging.debug(status[1])
    
    def detectSequences(self):
        logging.debug("Sasiedzi plytki")
        cellsList = self.findChildren(BoardCell)
        seq = []
        detected_sequence = False
        self.all_sequences = []
        for cell in cellsList:
            
            if cell.left != None:
                left_neighbour_status = cell.left.getCellStatus()
               
            else:
                left_neighbour_status ='Empty'

            if cell.right != None:
                right_neighbour_status = cell.right.getCellStatus()
               
            else:
                right_neighbour_status = 'Empty'
            
            # the first element of a squence
            if left_neighbour_status == 'Empty' and right_neighbour_status != 'Empty' and cell.getCellStatus() !='Empty':
                seq.append(cell)
                detected_sequence = True
            elif detected_sequence == True and left_neighbour_status != 'Empty' and right_neighbour_status != 'Empty':
                seq.append(cell)
            #the last element of a sequence
            elif left_neighbour_status != 'Empty' and right_neighbour_status == 'Empty' and cell.getCellStatus() !='Empty' and detected_sequence == True:
                seq.append(cell)
                detected_sequence = False
                if len(seq) > 2:
                    self.all_sequences.append(seq)
                else:
                    logging.info('Blad ciag musi miec co najmniej 3 elementy !')
                    QMessageBox.warning(self,'Niedozwolony ruch','Sekwencja musi miec co najmniej 3 plytki !')
                    return False
                logging.debug(seq)
                seq = []
                # seq.clear()
            elif left_neighbour_status == 'Empty' and right_neighbour_status == 'Empty' and cell.getCellStatus() != 'Empty':
                logging.info('Blad ciag musi miec co najmniej 3 elementy !')
                QMessageBox.warning(self,'Niedozwolony ruch','Sekwencja musi miec co najmniej 3 plytki !')
                return False
        
        if len(self.all_sequences) == 0:
            return True
        else:
            return self.checkAllSequences()
    
    def printAllSequences(self):
        for i,seq in enumerate(self.all_sequences):
            logging.debug('Wszystkie zestawy plytek ')
            logging.debug(seq)
            for cell in seq:
                status = cell.getCellStatus()
                logging.debug(status[0])
                logging.debug(status[1])
                logging.debug()
            logging.debug('---------')

    def checkAllSequences(self):
        ok = True
        for i,seq in enumerate(self.all_sequences):
            logging.debug('Sprawdzanie sekwencji plytek')

            # 1. Create tokens color and number lists
            token_color_list = []
            token_number_list = []

            for cell in seq:
                status = cell.getCellStatus()
                token_color_list.append(status[0])
                token_number_list.append(int(status[1]))

            # 2. CHECK IF CORRECT SEQUENCE
            #check if player first turn
            if (self.checkSum(token_number_list) == False):
                ok = False
            # Option1 : more than 3 in different colors
            else:
                check_diff_colors = self.check3diffColor(token_color_list, token_number_list)
                logging.info('Opcja 1'+ str(check_diff_colors))

                # Option2: 1 color number, each one +1
                check_plus_num = self.checkPlusNumber(token_color_list, token_number_list)
                logging.info('Opcja 2'+ str(check_plus_num))

                # IF BAD SEQ
                if check_diff_colors == False and check_plus_num == False:
                    logging.info('Nie mozna wykonac takiego ruchu !')
                    for cell in seq:
                        cell.errorHighLightOn()
                    QMessageBox.warning(self,'Niedozwolony ruch','Nie mozesz wykonac takiego ruchu')
                    for cell in seq:
                        cell.errorHighLightOff()
                    ok = False
                
        return ok
        

    def check3diffColor(self,token_color_list, token_number_list):
        #check if all numbers are the same
        numbers_equal = token_number_list.count(token_number_list[0]) == len(token_number_list)
        logging.debug('Numery na plytkach sa takie same'+ str(numbers_equal))

        #check if all colors are unique
        colors_unique = False
        if(len(set(token_color_list)) == len(token_color_list)):
            colors_unique = True
        logging.debug('Kolory sa rozne' + str(colors_unique))

        if numbers_equal == True and colors_unique == True:
            return True
        else:
            return False
            
    def checkPlusNumber(self,token_color_list,token_number_list):
        #Check if colors are the same
        colors_equal = token_color_list.count(token_color_list[0]) == len(token_color_list)
        logging.debug('Kolory sa takie same'+ str(colors_equal))

        #check +1 sequence
        numPlus = True
        last_item = token_number_list[0]
        num_len = len(token_number_list)
        for i in range(1,num_len):
            item = token_number_list[i]
            if(item - last_item) == 1:
                last_item = item
            else:
                numPlus = False
        logging.debug('Kazdy numer na plytce o 1 wiekszy od poprzedniego: '+str(numPlus))
        
        if colors_equal == True and numPlus == True:
            return True
        else:
            return False
                
    def checkSum(self, token_number_list):
        sum = 0
        last_turn = main.player_turn-1
        if last_turn == -1:
            last_turn = 3
        logging.debug('tura gracza:')
        logging.debug(last_turn)
        
        if main.players_first_turn[last_turn] == True:
            for item in token_number_list:
                sum += item

            if(sum<30):
                QMessageBox.warning(self,'Niedozwolony ruch','W pierwszej turze suma plytek musi byc wieksza od 30 !')
                logging.info('Niedozwolony ruch. W pierwszej turze suma plytek musi byc wieksza od 30 !')
                return False
            else:
                main.players_first_turn[last_turn] = False
                return True
        else:
            return True
        

    def AddTileFromBag(self, tile):
        logging.debug("Dobieranie plytki")

        for cell in self.cellList:
            status = cell.getCellStatus()
            if status == "Empty":
                cell.addTile(tile)
                break

    def GetNextEmptyCellPosition(self):
        logging.debug("Nowa pozycja plytki")

    def removeTile(self, index):
        self.cellList[index].removeTile()


class PlayerGrid(TileGridBaseClass):
    def __init__(self, bgColor, fgColor, gridName, rows, cols):
        super(PlayerGrid, self).__init__(rows, cols, bgColor, fgColor, gridName)
        self.pal = self.palette()
        self.pal.setColor(self.backgroundRole(), bgColor)
        self.pal.setColor(self.foregroundRole(), fgColor)  
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

    def newDeal(self):
        
        for n in range(main.numberOfTilesToDeal):
            if main.tileBag.getNoOfTilesInBag() > 0:
                nextTile = main.tileBag.getTileFromBag()
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
            QMessageBox.information(self,'Koniec gry','Zwyciezyl gracz '+ str(main.player_turn))
            logging.info("Koniec gry. Zwyciezyl gracz "+ str(main.player_turn))
        return isWinner
    
    
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
    

class Player():
    def __init__(self, player_id, player_name,player_first_turn,main):
        self.player_id = player_id
        self.player_name = player_name
        playerBgColor = QColor('#A5A5A5')
        playerFgColor = QColor('#000000')
        self.player_grid = PlayerGrid(playerBgColor, playerFgColor, "PlayerGrid", 2, main.numberOfColumns)
        self.player_controls = PlayerControls(playerBgColor, main.playerFgColor, self.player_grid, self.player_name)
        self.player_first_turn = player_first_turn
        self.drawedTile = False
    
    def change_first_turn(self,first_turn):
        self.player_first_turn = first_turn
        

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

class Params():
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


        self.gameBoard = GameBoard(self.boardBgColor, self.boardFgColor, "GameBoard", 8, self.numberOfColumns*2)

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
    # RummyKub = MainWin()

def getCellCol(cell):
    return cell.getCol()

if __name__ == "__main__":
    print("HIIIIIIIII")
    app = QApplication(sys.argv)
    main = Params()
    
    RummyKub = MainWin()
    
    RummyKub.show()
    
    main.newGame()
    
    freezePlayers()
   

sys.exit(app.exec_())