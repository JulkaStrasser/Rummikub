import random
from console_game import ConsoleGame


class GameMechanics():

    def __init__(self) -> None:
        option_1 = False
        self.con = ConsoleGame()
        pass

    # Tworzenie plytek 
    def setTokens(self):
        tokens = []

        colors = ["Pomaranczowy", "Niebieski", "Czarny", "Czerwony"]

        for z in range(2):
            for color in colors:
                for value in range(1, 14):
                    token_value = "{} {}".format(color, value)
                    tokens.append(token_value)
        return tokens
    
    #Mieszanie plytek
    def shuffleTokens(self,tokens):
        for token_pos in range(len(tokens)):
            randPos = random.randint(0, 51)
            tokens[token_pos], tokens[randPos] = tokens[randPos], tokens[token_pos]
        return tokens

    def giveAwayTokens(self,tokens_number,tokensRummikub):
        player_tokens = []
        for x in range(tokens_number):
            player_tokens.append(tokensRummikub.pop(0))
        return player_tokens
    
    #MOZLIWE OPERACJE
    def opcion1(self,player_hand,tokensRummikub):
        player_hand.extend(self.giveAwayTokens(1,tokensRummikub))
        self.con.opcion1()

    def opcion2(self,token_user, token_set,players,player_turn, tokens):
        if token_user > len(players[player_turn]):
            self.con.print_error(self.con.errors["NoToken"])
            return False

        if token_set > len(tokens):
            self.con.print_error(self.con.errors["NoSetTable"])
            return False
        elif token_set <= len(tokens):
            return self.checkOption2(players,player_turn,token_user, tokens, token_set)
        
    #Dodaj plytki do nowej pozycji
    def opcion3(self,player_hand,players,player_turn, tokens):

        new_token_set = []
        stop_chosing = False

        while not stop_chosing:
            token_user = self.con.option3_input()
            if token_user == 0:
                if len(new_token_set) <= 2:
                    self.con.print_error(self.con.errors["MoreTokens"])
                    cancelOpcion = self.con.cancel_input()

                    if str(cancelOpcion).lower() == "t":
                        stop_chosing = True
                        players[player_turn].extend(new_token_set)
                        new_token_set.clear()

                    elif (str(cancelOpcion).lower() != "n" or str(cancelOpcion).lower() != "t"):
                        self.con.print_error(self.con.errors["NoOption"])
                else:
                    stop_chosing = True
                    tokens.append(new_token_set)

            elif token_user > len(players[player_turn]):
                self.con.print_error(self.con.errors["NoToken"])

            else:
                
                if len(new_token_set) == 0:
                    new_token_set.append(players[player_turn][token_user - 1])
                    players[player_turn].pop(token_user - 1)
                    self.con.print_info(self.con.infos["TokenAdded"])
                else:
                    if self.checkOption3(players, player_turn, token_user,new_token_set):
                        players[player_turn].pop(token_user - 1)
                        self.con.print_info(self.con.infos["TokenAdded"])
                    else:
                        self.con.print_error(self.con.errors["TokenNotMatchSet"])

                
                self.con.showHand(player_hand)
                self.con.showHeap(new_token_set)

        return len(new_token_set) != 0
    
    # Sprawdzanie czy mozna dodac plytke opcja 2
    def checkOption2(self,players,player_turn,token_user, tokens, token_set):
        input_color = players[player_turn][token_user - 1].split(" ")
        input_number = int(input_color.pop(1))

        token_color_list = []
        token_number_list = []

        for i in tokens[token_set - 1]:
            colortoken_set = i.split(" ")
            numerotoken_set = int(colortoken_set.pop(1))
            token_color_list.append(colortoken_set[0])
            token_number_list.append(numerotoken_set)

        #SPRAWDZANIE CZY KOMBINACJA JEST POPRAWNA
        if token_number_list[0] == token_number_list[1]:
            # co najmniej 3 w roznych kolorach
        
            correct = False
            while not correct:
                if input_color[0] in token_color_list or input_number != numerotoken_set:
                    self.con.print_error(self.con.errors["BadMove"])
                    return False
                else:
                    correct = True
                    tokens[token_set - 1].append(players[player_turn][token_user - 1])
                    self.con.print_info(self.con.infos["TokenAdded"])
                    return True
        else:
            # po kolei ten sam kolor
            correct = False
            while correct == False:
                if (
                    input_color != colortoken_set
                    or input_number != (token_number_list[-1] + 1)
                    and input_number != (token_number_list[0] - 1)
                ):
                    self.con.print_error(self.con.errors["BadMove"])
                    return False

                elif input_number == (token_number_list[0] - 1):
                    correct = True
                    token_number_list.append(input_number)
                    token_number_list.sort()
                    tokens[token_set - 1].insert(0, players[player_turn][token_user - 1])

                else:
                    correct = True
                    tokens[token_set - 1].append(players[player_turn][token_user - 1])

            return correct

    # Sprawdzanie czy nowa konfiguracja jest poprawna
    def checkOption3(self, players, player_turn, token_user, new_token_set):
        input_color = players[player_turn][token_user - 1].split(" ")
        input_number = int(input_color.pop(1))

        token_color_list = []
        token_number_list = []

        for i in new_token_set:
            colortoken_set = i.split(" ")
            numerotoken_set = int(colortoken_set.pop(1))
            token_color_list.append(colortoken_set[0])
            token_number_list.append(numerotoken_set)

    
        if token_number_list[0] == input_number:
            # ta sama liczba rozne kolory
            correct = False
            while not correct:
                if input_color[0] in token_color_list or input_number != numerotoken_set:
                    self.con.print_error(self.con.errors["BadMove"])
                    return False

                else:
                    correct = True
                    new_token_set.append(players[player_turn][token_user - 1])
                    return True
        else:
            # po kolei 1 kolor
            correct = False
            while not correct:
                if (input_color != colortoken_set or input_number != (token_number_list[-1] + 1) and input_number != (token_number_list[0] - 1)):
                    self.con.print_error(self.con.errors["BadMove"])
                    return False

                elif input_number == (token_number_list[0] - 1):
                    correct = True
                    token_number_list.append(input_number)
                    token_number_list.sort()
                    new_token_set.insert(0, players[player_turn][token_user - 1])
                else:
                    correct = True
                    new_token_set.append(players[player_turn][token_user - 1])
            return correct

    
