"""
a 3 in the array is a spawn point for now, and i simply put a house there for testing.
a 1 is ocean.
a 2 is a grass tile.
"""


import json

data = {}
data["map"] = []

num_rows = 50
num_cols = 50

for col in range(num_cols):
    x = []
    for row in range(num_rows):
        if col == 0 or col == 1 or row == 0 or row == 1 or col == num_cols-1 or row == num_rows-1 or col == num_cols-2 or row == num_rows-2:
            x.append(1)
        elif col == 10 and row == 10:
            x.append(3)
        else:
            x.append(2)
    data["map"].append(x)

print(data)

with open("quadratic_island.json", "w") as file:
    json.dump(data, file)
