order = input()
menu = {'pizza': ['Margherita', 'Four Seasons', 'Neapolitan', 'Vegetarian', 'Spicy'],
        'salad': ['Caesar salad', 'Green salad', 'Tuna salad', 'Fruit salad'],
        'soup': ['Chicken soup', 'Ramen', 'Tomato soup', 'Mushroom cream soup']}

if order in menu:
    separator = ", "
    print(separator.join(menu[order]))
else:
    print("Sorry, we don't have it in the menu")
