
from rich.console import Console
from rich.progress import track
import os
import time
import math
# from mechanics import GameMechanics

class ConsoleGame():

    console = Console()

    errors = {
    "NoToken": "Nie masz takiej plytki",
    "NoSetTable": "Tego zestawu nie ma na planszy.",
    "MoreTokens": "Minimalny zestaw to 3 płytki",
    "NoOption":"Nie ma takiej opcji",
    "TokenNotMatchSet":"Nie mozna dodac tej plytki do zestawu.",
    "BadMove":"Zly ruch, sprobuj ponownie.",
    "Not30":"Wartosc dodanych zestawow nie przekracza 30."
    }

    infos = {
    "TokenAdded":"Twoja plytka zostala pomyslnie dodana"
    }
    def __init__(self) -> None:
        pass

    

    # Funkcje do pisania w kolorze
    def prRed(self,ficha, end="\n"):
        print("\033[31m {}\033[00m".format(ficha), end=end)


    def prOrange(self,ficha, end="\n"):
        print("\033[33m {}\033[00m".format(ficha), end=end)


    def prBlue(self,ficha, end="\n"):
        print("\033[34m {}\033[00m".format(ficha), end=end)


    def prPurple(self,ficha, end="\n"):
        print("\033[35m {}\033[00m".format(ficha), end=end)

    def prGreen(self,ficha, end="\n"):
        print("\033[32m {}\033[00m".format(ficha), end=end)

    # Czyszczenie terminala
    def cleanTerminal(self):
        os.system("clear")

    # Funkcja malowania płytki na kolor. brak zerwania linii
    def paintTileColor(self,text, color):
        if color == "Czerwony":
            self.prRed(text, end="")
            return
        if color == "Czarny":
            self.prPurple(text, end="")
            return
        if color == "Niebieski":
            self.prBlue(text, end="")
            return
        if color == "Pomaranczowy":
            self.prOrange(text, end="")
            return
        print(text, end="")

    def welcome(self):
        self.cleanTerminal()
        self.console.print(
            "____                                    _   _  __          _      \n"
            + "  |  _ \   _   _   _ __ ___    _ __ ___   (_) | |/ /  _   _  | |__  \n"
            + "  | |_) | | | | | | '_ ` _ \  | '_ ` _ \  | | | ' /  | | | | | '_ \ \n"
            + "   |  _ <  | |_| | | | | | | | | | | | | | | | | . \  | |_| | | |_) |\n"
            + "  |_| \_\  \__,_| |_| |_| |_| |_| |_| |_| |_| |_|\_\  \__,_| |_.__/ \n",
            justify="center",
            style="bold",
        )
        print("\n\n")
        self.console.print(
            ":fire:",
            "Witamy w Rummikubie!!",
            ":fire:",
            justify="center",
            style="bold cyan",
        )
        self.console.print(
            "Przygotowujemy wszystko, aby jak najszybciej móc rozpocząć grę..\n"
            + "Przede wszystkim musimy wiedzieć kilka rzeczy, aby dostosować grę.\n",
            justify="center",
        )
        print("\n\n")
    
    def progressBar(self):
        for i in track(range(100), description="Ladowanie..."):
            time.sleep(0.05)

    def startGameTxt(self):
        self.cleanTerminal()
        self.console.print("\n\nWSZYSTKO GOTOWE\n¡GRAC!", justify="center")
        self.console.print("Powodzenia i niech wygra lepszy", justify="center")
        time.sleep(1.5)

    def endOfGame(self,player):
        self.cleanTerminal()

        self.console.print("Gra się skończyła! Skończyły Ci się kafelki!", justify="center")
        self.console.print("ZWYCIĘZCĄ JEST:\n", justify="center")
        self.console.print(f"\tGracz {player + 1}\n", justify="center")

        self.console.print(
            " _ ______ _   _ _    _  ____  _____            ____  _    _ ______ _   _          _  \n"
            + "(_)  ____| \ | | |  | |/ __ \|  __ \     /\   |  _ \| |  | |  ____| \ | |   /\   | | \n"
            + "| | |__  |  \| | |__| | |  | | |__) |   /  \  | |_) | |  | | |__  |  \| |  /  \  | | \n"
            + "| |  __| | . ` |  __  | |  | |  _  /   / /\ \ |  _ <| |  | |  __| | . ` | / /\ \ | | \n"
            + "| | |____| |\  | |  | | |__| | | \ \  / ____ \| |_) | |__| | |____| |\  |/ ____ \|_| \n"
            + "|_|______|_| \_|_|  |_|\____/|_|  \_\/_/    \_\____/ \____/|______|_| \_/_/    \_(_) ", justify="center"
        )

    #SHOW 
    def showGameStatus(self,player_id, player_hand, tokens,pas_option, takeToken, gameTurn):
        self.console.print(f"GRACZ {player_id + 1}", style="bold")
        print("\n\t Konfiguracje ulozone przez gracza to: ")
        self.displayBoard(tokens)
        print("\n\t Twoja reka")
        self.showHand(player_hand)

        # Mozliwe opcje
        print("\n\t Działania, które możesz wykonać, to:")
        self.showOptions(pas_option, takeToken,gameTurn, tokens)


    # Pokazywanie plytek gracza
    def showHand(self,player_hand):
        print("\n\n\tTwoja reka: ")
        print("|" + "-" * 120 + "|")
        porFila = 7
        y = 1
        for fila in range(math.ceil(len(player_hand) / porFila)):
            for x in range(porFila):
                if y > len(player_hand):
                    break
                split_token = player_hand[x + (fila * porFila)].split(" ", 1)
                color = split_token[0]
                print(f"({y})", end="")
                self.paintTileColor(f"{player_hand[x+(fila*porFila)]}\t", color)
                y += 1
            print("")
        print("|" + "-" * 120 + "|")

    # Pokazywanie opcji ktore gracz moze wykonac w tej turze
    def showOptions(self,pas_option, takeToken, gameTurn, tokens):
        if takeToken:
            self.console.print("[bold cyan]Opcja 1:[/bold cyan] [underline]Dobierz plytke.[/underline]")

        if gameTurn > 1 or len(tokens) >= 1:
            self.console.print(
                "[bold cyan]Opcja 2:[/bold cyan] [underline]Dodaj kartę do istniejącej pozycji.[/underline]"
            )

        self.console.print("[bold cyan]Opcja 3:[/bold cyan] [underline]Dodaj kartę w nowej pozycji.[/underline]")

        if pas_option:
            self.console.print("[bold cyan]Opcja 4:[/bold cyan] [underline]Pas.[/underline]")
    
    # Malowanie plytek na planszy
    #monton
    def showHeap(self,monton):
        print("\n\t Zestaw, który chcesz dodać na razie, to: ", end="")
        f = 1
        for ficha in monton:
            split_token = ficha.split(" ", 1)
            color = split_token[0]
            self.paintTileColor(f"{ficha}", color)
            f += 1
            if f <= len(monton):
                print(" -", end="")
        print()

    # Wyswietlanie plytek
    def displayBoard(self,tokens):
        print("|" + "-" * 120 + "|")
        porFila = 3
        numero = 1
        for fila in range(math.ceil(len(tokens) / porFila)):
            for x in range(porFila):
                if numero > len(tokens):
                    break
                print("", end="")
                print(f"({numero})", end="")
                self.showHeap(tokens[x + (fila * porFila)])
                print("\t\t", end="")
                numero += 1
            print("")
        print("|" + "-" * 120 + "|")

    
    #KOMUNIKATY DO AKCJI GRACZA
    def opcion1(self):
        self.prGreen("\nWziales plyteke.")

    def opcion2_input(self):
        token_user = int(input("Wybierz plytke, którą chcesz dodać: "))
        token_set = int(input("Wybierz kombinacje plytek, do którego chcesz ją dodać: "))
        return token_user, token_set
    
    def option3_input(self):
        token_user = int(input("Wybierz plytke, ktora chcesz dodac. Jesli nie chcesz dodawac wiecej, wpisz 0: "))

        return token_user
    
    def print_error(self,error):
        self.prRed(error)

    def print_info(self,info):
        self.prGreen(info)

    def cancel_input(self):
        cancelOpcion = input("Czy chcesz anulowac operacje? (t/n)")
        return cancelOpcion
    
    def players_number_input(self):
        numplayers = int(self.console.input("[b]Ilu graczy?[/b]"))
        while numplayers < 2 or numplayers > 4:
            self.prRed("\tProszę wpisać liczbę od 2 do 4.\n")
            numplayers = int(input("Ilu graczy? "))

        print("Doskonale! Za kilka sekund wszystko bedzie gotowe.\n")
        self.progressBar()
        return numplayers
    
    def choose_option(self):
        while True:
            try:
                action = int(input("\nKtora opcje wynierasz?: "))
                break
            except ValueError:
                self.prRed("\tProsze wybrac poprawny numer.")
        return action

        

    

