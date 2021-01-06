number = int(input())
answer = number
while number - 1 > 0:
    answer *= number - 1
    number -= 1
print(answer)
