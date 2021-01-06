money = int(input())

animals = {"chicken": 23, "goat": 678, "pig": 1296, "cow": 3848, "sheep": 6769}
purchase_price = 0
purchase_animal = ""
purchase_qty = 0
temp_qty = 0

for animal in animals:
    temp_qty = money//animals[animal]
    if temp_qty > 0:
        if temp_qty > 1:
            if animal != 'sheep':
                purchase_animal = animal + 's'
            else:
                purchase_animal = animal
        else:
            purchase_animal = animal
        purchase_qty = temp_qty
if purchase_qty == 0:
    print('None')
else:
    print(f'{purchase_qty} {purchase_animal}')
