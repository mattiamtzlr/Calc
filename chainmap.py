from collections import ChainMap

d1 = {"a": 1, "b": 3}
d2 = {"b": 2, "c": 2}
d3 = {"a": 4, "d": 4}

chained = ChainMap(d1, d2, d3)

# Nachschlagen: doppelte Werte werden von hinten nach vorne überschrieben
print(chained["a"])

print(chained["c"])

print(chained["d"])

# Hinzufügen: fügt das Element zum ersten dictionary hinzu.
chained["e"] = 7

chained["a"] = 9

# Ausdrucken: doppelte Werte werden von hinten nach vorne überschrieben
print()
for i,j in chained.items():
    print(i + ":", j)