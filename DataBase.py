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
        for row in self.cursor.execute("select * from history"):
            print(row)

    def close(self):
        self.connection.close()


# if __name__ == '__main__':
#     database = DataBase()
#     database.write_test_data()
#     database.write("Gracz 10","Suma musi byc wieksza niz 30 !")
#     database.read_all_data()
#     database.close()


