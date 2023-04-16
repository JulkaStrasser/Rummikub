import json

#ZAPIS DO PLIKU
# Data to be written
movement = {
	"player": "Gracz 1",
	"action": "Dobral plytke"
}

# Serializing json
json_object = json.dumps(movement, indent=2)

# Writing to sample.json
with open("sample.json", "w") as outfile:
	outfile.write(json_object)

#ODCZYT Z PLIKU
with open('sample.json', 'r') as openfile:
 
    # Reading from json file
    json_object = json.load(openfile)
 
print(json_object)
print(type(json_object))