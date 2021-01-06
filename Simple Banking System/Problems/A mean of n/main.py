# n = int(input())
# total = 0
# for _ in range(n):
#     total += int(input())
# print(total / n)

i = 10
while i > 0:
    i -= 2
    if i % 2 == 1:
        break
    else:
        i -= 2
else:
    print("End.")