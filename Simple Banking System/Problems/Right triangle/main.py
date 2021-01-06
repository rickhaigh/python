class RightTriangle:
    def __init__(self, hyp: int, leg_1: int, leg_2: int):
        self.c = hyp
        self.a = leg_1
        self.b = leg_2
        self.area = (self.a * self.b)/2
        # calculate the area here


# triangle from the input
input_c, input_a, input_b = [int(x) for x in input().split()]

# write your code here
if (input_a**2 + input_b**2) == input_c**2:
    right_triangle = RightTriangle(input_c, input_a, input_b)
    print(round(right_triangle.area, 1))
else:
    print('Not right')
