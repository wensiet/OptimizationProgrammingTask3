from algorithm import interior_point


def test_test1():
    c = [9, 10, 16]
    a = [[18, 15, 12], [6, 4, 8], [5, 3, 3]]
    b = [360, 192, 180]
    initial = [1, 1, 1, 315, 174, 169]
    e = 0.01
    alpha = 0.5
    interior = interior_point.InteriorPoint(c, a, b, initial, e, alpha)
    assert interior.solve_llp() ==\
           "[2.96713352e−06; 7.99999106e+00; 2.00000010e+01; 6.67605042e−058.90140056e−06; 9.60000086e+01]"


def test_test2():
    c = [2, 5, 7]
    a = [1, 2, 3]
    b = [6]
    initial = [1, 1, 1]
    e = 0.01
    alpha = 0.9
    interior = interior_point.InteriorPoint(c, a, b, initial, e, alpha)
    assert interior.solve_llp() == "[0.00176; 2.99648; 0.00176; 14.9982]"
