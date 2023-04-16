import sqlite3

class DataBase():
    def __init__(self):
        self.connection = sqlite3.connect("history_rummy.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('create table history (player text, action text)')

    def write_test_data(self):
        #Wpisujemy sobie cos do bazy danych
        self.cursor.execute("insert into history values (?,?)",("Gracz 1","Dobral plytke niebieska 1"))
        self.cursor.execute("insert into history values (?,?)",("Gracz 1","Polozyl na plansze sekwencje"))

    def write(self, player, action):
        self.cursor.execute("insert into history values (?,?)",(player,action))
        
    def read_all_data(self):
        with open('database.txt', 'w') as f:
            for row in self.cursor.execute("select * from history"):
                print(row)
                f.write(str(row)+"\n")

    def close(self):
        self.connection.close()





