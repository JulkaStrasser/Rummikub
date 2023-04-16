import sqlite3

connection = sqlite3.connect("history_rummy.db")

cursor = connection.cursor()

#Tworzymy tablice do zapisu gry
cursor.execute('create table history (player_id text, action text)')

#Wpisujemy sobie cos do bazy danych
cursor.execute("insert into history values (?,?)",("Gracz 1","Dobral plytke niebieska 1"))
cursor.execute("insert into history values (?,?)",("Gracz 1","Polozyl na plansze sekwencje"))

for row in cursor.execute("select * from history"):
    print(row)



connection.close()