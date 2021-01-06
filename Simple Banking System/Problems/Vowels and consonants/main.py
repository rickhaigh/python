string = input()
vowels = "aeiouAEIOU"

for char in string:
    if char.isalpha():
        if char in vowels:
            print("vowel")
        else:
            print("consonant")
    else:
        break
