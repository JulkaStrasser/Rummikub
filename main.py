from mechanics import GameMechanics
from console_game import ConsoleGame
import time

class Main():

    
    def __init__(self):
        self.mech = GameMechanics()
        self.con = ConsoleGame()
        
    
    def play(self):
        # Przygotowanie plytek do gry
        tokensRummikub = self.mech.setTokens()
        tokensRummikub = self.mech.shuffleTokens(tokensRummikub)
        # tokensRummikub = shuffleTokens(tokensRummikub)

        tokens = []
        players = []
        
        #Powitanie
        self.con.welcome()

        #Wybor ilosci graczy
        numplayers = self.con.players_number_input()

        # Rozdanie kazdemu graczowi po 14 plytek
        for player in range(numplayers):
            players.append(self.mech.giveAwayTokens(14,tokensRummikub))


        # Tury, jak gracze graja po kolei
        # Dokładamy pierwszy kafelek na planszę --> ZROBIĆ: usunąć kafelek, ponieważ jest częścią UNO
        player_turn = 0
        gameTurn = 1
        game = True

        # Czy pierwsza tura
        first_turn = True

        # Dzielimy wartość i kolor żetonu, aby dokonać porównań
        split_token = tokensRummikub[0].split(" ", 1)
        color = split_token[0]
        token_value = int(split_token[1])

        #Sprawdzanie czy mozesz wziac zeton albo czy mozesz spasowac
        pas_option = False
        takeToken = True

        self.con.startGameTxt()

        while game:

            #nie pierwsza tura
            if not first_turn:

                takeToken = True
                pas_option = False
                end_game = False

                while not end_game:
                    time.sleep(1)
                    self.con.cleanTerminal()
                    # Pokazywanie plytek na rece i planszy
                    self.con.showGameStatus(player_turn, players[player_turn], tokens,pas_option, takeToken, gameTurn)
                    while True:
                        try:
                            action = int(input("\nKtora opcje wybierasz?: "))
                            break
                        except ValueError:
                            self.con.prRed("\tProsze wprowadzic poprawny numer.")

                        #Dobieranie plytki
                    if action == 1 and takeToken:
                        self.mech.opcion1(players[player_turn], tokensRummikub)

                    elif action == 2:
                            option2_input = self.con.opcion2_input()
                            correct = self.mech.opcion2(option2_input[0], option2_input[1],players,player_turn,tokens)
                            if correct:
                                takeToken = False
                                pas_option = True

                    elif action == 3:
                            correct = self.mech.opcion3(players[player_turn], players,player_turn,tokens)
                            if correct:
                                takeToken = False
                                pas_option = True

                    elif action == 4:
                            end_game = True

                    else:
                            self.con.prRed("\tOpcja nieprawidlowa")

                
            else:
                    takeToken = True
                    pas_option = False
                    end_game = False

                    while not end_game:
                        time.sleep(1)
                        self.con.cleanTerminal()
                        
                        self.con.showGameStatus(player_turn, players[player_turn], tokens,pas_option, takeToken, gameTurn)

                        action = self.con.choose_option()

                        if action == 1 and takeToken:
                            self.mech.opcion1(players[player_turn], tokensRummikub)
                            self.con.opcion1()

                        elif action == 2:
                            option2_input = self.con.opcion2_input()
                            correct = self.mech.opcion2(option2_input[0], option2_input[1],players,player_turn,tokens)
                            if correct:
                                pas_option = True

                        elif action == 3:
                            correct = self.mech.opcion3(players[player_turn], players,player_turn,tokens)
                            if correct:
                                pas_option = True

                        elif action == 4:
                            # Liczenie czy wartosc kosteczek jest wieksza od 30, bo wtedy mozna ja wylozyc
                            token_values = 0
                            for token_set in tokens:
                                for ficha in token_set:
                                    split_token = ficha.split(" ")
                                    token_values += int(split_token[1])

                            # Aby moc pierwszy raz dodac zestaw na plansze, jego wartosc musi przekroczyc 30
                            if token_values < 30:
                                self.con.print_error(self.con.errors["Not30"])
                            else:
                                end_game = True
                                if gameTurn == numplayers:
                                    first_turn = False
                        else:
                            self.con.print_error(self.con.errors["NoOption"])
                            

            if (len(players[player_turn]) == 0):  # Jesli jakis gracz zostanie bez plytek --> koniec gry
                    game = False

            else:
                    # Przejdz do nastepnej tury
                    player_turn = player_turn + 1
                    time.sleep(1.5)

                    if player_turn == numplayers:
                        player_turn = 0

                    # Zwiekszanie numeru tury
                    gameTurn += 1

        self.con.endOfGame(player_turn)

        
if __name__ == "__main__":
    game = Main()
    game.play()