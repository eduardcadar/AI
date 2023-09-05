from problems import Problems


def test1():
    assert Problems.solve1("ana are mere rosii si galbene") == "si"
    assert Problems.solve1("b o s o e t d") == "t"
    assert Problems.solve1("ana ana ana ana") == "ana"


def test2():
    assert Problems.solve2([1, 5], [4, 1]) == 5
    assert Problems.solve2([1, 1], [1, 1]) == 0
    assert Problems.solve2([1, 1], [2, 1]) == 1


def test3():
    assert Problems.solve3([1, 0, 2, 0, 3], [1, 2, 0, 3, 1]) == 4


def test4():
    assert sorted(Problems.solve4("ana abecedar are ana nu are mere rosii ana")) == ['abecedar', 'mere', 'nu', 'rosii']
    assert sorted(Problems.solve4("text de proba de test")) == ['proba', 'test', 'text']


def test5():
    assert Problems.solve5([1, 2, 3, 4, 2]) == 2
    assert Problems.solve5([1, 3, 3, 2]) == 3
    assert Problems.solve5([2, 5, 1, 3, 7, 4, 6, 1, 9, 8]) == 1


def test6():
    assert Problems.solve6([2, 8, 7, 2, 2, 5, 2, 3, 1, 2, 2]) == 2
    assert Problems.solve6([1, 2, 2, 4]) is None
    assert Problems.solve6([0, 3, 9, 3, 3, -7, 3, 3, 3, 4]) == 3


def test7():
    assert Problems.solve7([7, 4, 6, 3, 9, 1], 2) == 7
    assert Problems.solve7([8, 2, 9, 3, 8, 5], 3) == 8
    assert Problems.solve7([5, 4, 3, 1, 1, 2, 2], 5) == 2


def test8():
    assert Problems.solve8(4) == [1, 10, 11, 100]
    assert Problems.solve8(8) == [1, 10, 11, 100, 101, 110, 111, 1000]
    assert Problems.solve8(1) == [1]
    assert Problems.solve8(0) == []


def test9():
    assert Problems.solve9(
        [[0, 2, 5, 4, 1],
         [4, 8, 2, 3, 7],
         [6, 3, 4, 6, 2],
         [7, 3, 1, 8, 3],
         [1, 5, 7, 9, 4]],
        [[[1, 1], [3, 3]],
         [[2, 2], [4, 4]],
         [[0, 1], [3, 4]]]) == [38, 44, 62]


def test10():
    assert Problems.solve10([[0, 0, 0, 1, 1],
                             [0, 1, 1, 1, 1],
                             [0, 0, 1, 1, 1]]) == 2
    assert Problems.solve10([[1, 1, 1, 1, 1],
                             [0, 1, 1, 1, 1],
                             [0, 0, 1, 1, 1]]) == 1
    assert Problems.solve10([[0, 0, 1, 1, 1],
                             [0, 0, 1, 1, 1],
                             [0, 1, 1, 1, 1]]) == 3
    assert Problems.solve10([[0, 0],
                             [0, 0],
                             [0, 0]]) == 1


def test11():
    assert Problems.solve11([[1, 1, 1, 1, 0, 0, 1, 1, 0, 1],
                             [1, 0, 0, 1, 1, 0, 1, 1, 1, 1],
                             [1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 0, 0, 1, 1, 0, 1],
                             [1, 0, 0, 1, 1, 0, 1, 1, 0, 0],
                             [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                             [1, 1, 1, 0, 1, 0, 1, 0, 0, 1],
                             [1, 1, 1, 0, 1, 1, 1, 1, 1, 1]]) == [[1, 1, 1, 1, 0, 0, 1, 1, 0, 1],
                                                                  [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
                                                                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                                                  [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                                                                  [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                                                                  [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                                                                  [1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
                                                                  [1, 1, 1, 0, 1, 1, 1, 1, 1, 1]]


def tests():
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
    test10()
    test11()
