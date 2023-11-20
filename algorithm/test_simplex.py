from algorithm import Simplex


def test_multiple_optimum():
    s = Simplex(c=[2, 4], a=[[1, 1], [2, 1]], b=[5, 4], t="max")
    assert s.solve() == "x1=0 x2=4.0 s1=1.0 s2=0 with optimal 16.0"


def test_case1():
    assert Simplex(
        c=[4, 3],
        a=[[2, 3], [-3, 2], [0, 2], [2, 1]],
        b=[6, 3, 5, 4],
        e=0.1,
        t="max").solve() == 'x1=1.5 x2=1.0 x3=0 x4=5.5 s1=3.0 s2=0 with optimal 9.0'


def test_case2():
    assert Simplex(
        c=[8, 6],
        a=[[5, 2], [2, 4], [1, 1], [7, 8]],
        b=[5, 3, 8, 1],
        e=0.01,
        t="max").solve() == 'x1=0.14 x2=0 x3=4.29 x4=2.71 s1=7.86 s2=0 with optimal 1.14'


def test_case3():
    assert Simplex(
        c=[1, 1, 0, 0, 0],
        a=[[-1, 1, 1, 0, 0],
           [1, 0, 0, 1, 0],
           [0, 1, 0, 0, 1]],
        b=[2, 4, 4],
        e=0.01,
        t="max").solve() == 'x1=4.0 x2=4.0 x3=0 s1=0 s2=0 s3=2.0 s4=0 s5=0 with optimal 8.0'


def test_wrong_inputs():
    assert Simplex(
        c=[2, 1],
        a=[[0, 0], [0, 0], [0, 0], [0, 0, 0]],
        b=[-5, -3],
        t="max"
    ).solve() == 'Wrong inputs'
