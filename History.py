import xml.etree.ElementTree as gfg
import sqlite3

class History():
    def __init__(self):
        self.xml = XMLhistory('history.xml')
        self.database = DataBase()

    def write(self,player,action):
        self.xml.write(player,action)
        self.database.write(player,action)

    def read_all_data(self):
        self.xml.file_write()
        self.database.read_all_data()

    def close(self):
        self.database.close()


class XMLhistory():
    def __init__(self,filename):
        self.root = gfg.Element("History")
        self.filename = filename

    def write(self,player,action):
        elem = gfg.Element("movement")
        self.root.append (elem)

        sub_elem1 = gfg.SubElement(elem, "player")
        sub_elem1.text = player

        sub_elem2 = gfg.SubElement(elem, "action")
        sub_elem2.text = action

    def file_write(self):
        tree = gfg.ElementTree(self.root)
        gfg.indent(tree, space="\t", level=0)
        with open (self.filename, "wb") as files :
            tree.write(files,encoding="utf-8")


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