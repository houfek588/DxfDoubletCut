import numpy as np
import math
from scipy.optimize import fsolve

def line_circle_intersection(line_points, cirle_points):

    # line
    # y = a * x + b
    x1 = line_points[0][0]
    y1 = line_points[0][1]
    x2 = line_points[1][0]
    y2 = line_points[1][1]

    a = (y1 - y2) / (x1 - x2)
    b = y2 - a * x2

    # circle
    # (x - m)2 + (y - n)2 = R2
    m = cirle_points[0][0]
    n = cirle_points[0][1]
    R = cirle_points[1]

    # solution
    # a_sq = 1 + a**2
    # b_sq = 2 * (a * b - a * n - m)
    # c_sq = pow(m, 2) + pow(n, 2) + pow(b, 2) - pow(R, 2) - 2 * b * n

    # intersection points
    # x_in = np.roots([a_sq, b_sq, c_sq])
    # y_in = x_in * a + b

    # print(x_in)
    # print(y_in)

    # out = [(x_in[0], y_in[0]), (x_in[1], y_in[1])]

    def equations(vars):
        x, y = vars
        eq1 = (x - m) ** 2 + (y - n) ** 2 - R ** 2
        eq2 = a*x + b - y
        return [eq1, eq2]

    print('fsolve = ')
    return fsolve(equations, (x1, y1))


    # return out


def circle_circle_intersection(circle_points1, circle_points2, x0, y0):
    m1 = circle_points1[0][0]
    n1 = circle_points1[0][1]
    R1 = circle_points1[1]

    m2 = circle_points2[0][0]
    n2 = circle_points2[0][1]
    R2 = circle_points2[1]

    def equations(vars):
        x, y = vars
        eq1 = (x - m1) ** 2 + (y - n1) ** 2 - R1 ** 2
        eq2 = (x - m2) ** 2 + (y - n2) ** 2 - R2 ** 2
        return [eq1, eq2]

    return fsolve(equations, (x0, y0))






l = [(2,-1), (0,0)]
p = [(2,-1), math.sqrt(20)]
print(line_circle_intersection(l,p))

# print(circle_circle_intersection(-1,2))