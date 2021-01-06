# put your python code here
number = int(input())
total = number
sumofsquares = number * number

while total != 0:
    number = int(input())
    total += number
    sumofsquares += number * number
if sumofsquares == 0:
    print(0)
else:
    print(sumofsquares)
