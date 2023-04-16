from TileGridBase import TileGridBaseClass
from Cell import BoardCell
import logging
from PyQt5.QtWidgets import QMessageBox

class GameBoard(TileGridBaseClass):
    def __init__(self, bgColor, fgColor, gridName, rows, cols,main):
        super(GameBoard, self).__init__(rows, cols, bgColor, fgColor, gridName,main)
        self.main = main
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
                    self.main.database.write("Gracz "+ str(self.main.player_turn),"Blad ciag musi miec co najmniej 3 elementy")
                    logging.info('Blad ciag musi miec co najmniej 3 elementy !')
                    QMessageBox.warning(self,'Niedozwolony ruch','Sekwencja musi miec co najmniej 3 plytki !')
                    return False
                logging.debug(seq)
                seq = []
                # seq.clear()
            elif left_neighbour_status == 'Empty' and right_neighbour_status == 'Empty' and cell.getCellStatus() != 'Empty':
                self.main.database.write("Gracz "+ str(self.main.player_turn),"Blad ciag musi miec co najmniej 3 elementy")
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
                    self.main.database.write("Gracz "+ str(self.main.player_turn),"Nie mozna wykonac takiego ruchu !")
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
        last_turn = self.main.player_turn-1
        if last_turn == -1:
            last_turn = 3
        logging.debug('tura gracza:')
        logging.debug(last_turn)
        
        if self.main.players_first_turn[last_turn] == True:
            for item in token_number_list:
                sum += item

            if(sum<30):
                QMessageBox.warning(self,'Niedozwolony ruch','W pierwszej turze suma plytek musi byc wieksza od 30 !')
                logging.info('Niedozwolony ruch. W pierwszej turze suma plytek musi byc wieksza od 30 !')
                return False
            else:
                self.main.players_first_turn[last_turn] = False
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