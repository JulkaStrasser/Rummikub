import sqlite3

connection = sqlite3.connect("testdatabase.db")

cursor = connection.cursor()

cursor.execute('create table tab1 (release_year integer, release_name text, city text)')
release_list = [
    (1997, "Grand Theft Auto", "state of New Guernsey"),
    (1999, "Grand Theft Auto 2", "Anywhere, USA"),
    (2001, "Grand Theft Auto III", "Liberty City"),
    (2002, "Grand Theft Auto: Vice City", "Vice City"),
    (2004, "Grand Theft Auto: San Andreas", "state of San Andreas"),
    (2008, "Grand Theft Auto IV", "Liberty City"),
    (2013, "Grand Theft Auto V", "Los Santos")
]    

cursor.executemany("insert into tab1 values (?,?,?)", release_list)

for row in cursor.execute("select * from tab1"):
    print(row)

# tylko produkcje w liberty city
cursor.execute("select * from tab1 where city=:c",{"c":"Liberty City"})
tab_search = cursor.fetchall()
print("****")
print(tab_search)

cursor.execute('create table cities (gta_city text, real_city text)')
cursor.execute("insert into cities values (?,?)",("Liberty City","New York"))
cursor.execute("select * from cities where gta_city=:c",{"c":"Liberty City"})
city_search = cursor.fetchall()
print("***")
print(city_search)

#laczenie 2 tabel
print()
print("laczymy")

for i in tab_search:
    #[rzad][kolumna]
    adjusted = [city_search[0][1] if value == city_search[0][0] else value for value in i]
    print(adjusted)

connection.close()