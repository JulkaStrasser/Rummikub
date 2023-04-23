import json

# a Python object (dict):
x = {"board": []}
cell = {"cell_0_0": {}}
tile = {"empty": False, "color": "blue", "number": 3}
cell["cell_0_0"] = tile

cell1 = {"cell_0_1": {}}
tile = {"empty": False, "color": "blue", "number": 1}
cell1["cell_0_1"] = tile

# cell["cell_0_0"] = tile
x["board"].append(cell)
x["board"].append(cell1)
# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
print(y)
