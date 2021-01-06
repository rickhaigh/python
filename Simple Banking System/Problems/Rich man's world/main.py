import math


def compound_interest(principle, rate):
    # Calculates compound interest
    time = 0
    Amount = 0
    while Amount < max_balance:
        time += 1
        Amount = principle * (pow((1 + rate / 100), time))
        CI = Amount - principle

    print(time)
    return time


max_balance = 700000
min_balance = 50000
interest_rate = 7.1 # 7.1%
time = 0
balance = int(input())

if min_balance < balance < max_balance:
    # A = P(1+(r/n)^(nt)
    # A = the future value of the investment/loan, including interest
    # P = the principal investment amount (the initial deposit or loan amount)
    # r = the annual interest rate (decimal)
    # n = the number of times that interest is compounded per unit t
    # t = the time the money is invested or borrowed for
    a = max_balance
    p = balance
    r = interest_rate
    t = 0
    # Driver Code
    time = compound_interest(p, r)
