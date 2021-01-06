cats_max = 0
cat = ""
cats = input().split(sep=" ")

while cats[0] != "MEOW":
    if int(cats[1]) > cats_max:
        cats_max = int(cats[1])
        cat = cats[0]
    cats = input().split(sep=" ")

print(cat)
