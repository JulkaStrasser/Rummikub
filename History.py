import xml.etree.ElementTree as gfg
import sqlite3
import json


class History():
    def __init__(self,main):
        self.main = main
        if self.main.isXML:
            self.xml = XMLhistory('history.xml')
        if self.main.isSQL:
            self.database = DataBase()
        if self.main.isJson:
            self.json = JsonOption('options.json')

    def write(self,player,action):
        if self.main.isXML:
            self.xml.write(player,action)
        if self.main.isSQL:
            self.database.write(player,action)
        if self.main.isJson:
            self.json.write(player,action)

    def read_all_data(self):
        if self.main.isXML:
            self.xml.file_write()
        if self.main.isSQL:
            self.database.read_all_data()
        if self.main.isJson:
            self.json.read()

    def close(self):
        if self.main.isSQL:
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


class JsonOption():
    def __init__(self,filename):
        self.filename = filename
    
    def read(self):
        with open(self.filename, 'r') as openfile:
            #Reading from json file
            json_object = openfile
        
            print(json_object)
            print(type(json_object))

    def write(self,player,action):
        movement = {
            "player":player,
            "action":action
        }
        self.json_object = json.dumps(movement, indent=2)
        with open(self.filename, "a") as outfile:
	        outfile.write(self.json_object)
                