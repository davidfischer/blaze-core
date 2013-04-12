import unittest
from unittest import skip

from blaze.layouts.scalar import Interval, Chart, vstack,\
    hstack, dstack

tests = []

#------------------------------------------------------------------------

# dummy space
class Space(object):
    def __init__(self, n):
        self.n = n
    def __eq__(self, other):
        return self.n == other.n

#------------------------------------------------------------------------

class TestCharts(unittest.TestCase):

    @skip('')
    def test_multiple_charts(self):
        alpha = Space(1)
        beta  = Space(2)

        a = Interval(0,2)
        b = Interval(0,2)

        x = Chart([a,b], alpha)
        y = Chart([a,b], beta)

        # -------------
        s = hstack(x,y)
        # -------------

    @skip('')
    def test_vertical_stack(self):
        alpha = Space(1)
        beta  = Space(2)

        a = Interval(0,2)
        b = Interval(0,2)

        x = Chart([a,b], alpha)
        y = Chart([a,b], beta)

        # -------------
        s = vstack(x,y)
        # -------------

        block, coords = s[[3,1]]
        assert block == beta
        assert coords == [1,1]

        block, coords = s[[0,0]]
        assert block == alpha
        assert coords == [0,0]

        block, coords = s[[1,0]]
        assert block == alpha
        assert coords == [1,0]

        block, coords = s[[2,0]]
        assert block == beta
        assert coords == [0,0]

        block, coords = s[[2,1]]
        assert block == beta
        assert coords == [0,1]

    @skip('')
    def test_horizontal_stack(self):
        alpha = Space(1)
        beta  = Space(2)

        a = Interval(0,2)
        b = Interval(0,2)

        x = Chart([a,b], alpha)
        y = Chart([a,b], beta)

        # -------------
        s = hstack(x,y)
        # -------------

        block, coords = s[[0,0]]
        assert block == alpha
        assert coords == [0,0]

        block, coords = s[[0,1]]
        assert block == alpha
        assert coords == [0,1]

        block, coords = s[[0,2]]
        assert block == beta
        assert coords == [0,0]

        block, coords = s[[2,4]]
        assert block == beta
        assert coords == [2,2]

    @skip('')
    def test_third_axis(self):
        alpha = Space(1)
        beta  = Space(2)

        a = Interval(0,2)
        b = Interval(0,2)
        c = Interval(0,2)

        x = Chart([a,b,c], alpha)
        y = Chart([a,b,c], beta)

        # -------------
        s = dstack(x,y)
        # -------------

        block, coords = s[[0,0,0]]
        assert block == alpha
        assert coords == [0,0,0]

tests.append(TestCharts)

#------------------------------------------------------------------------

def run(verbosity=1, repeat=1):
    suite = unittest.TestSuite()
    for cls in tests:
        for _ in range(repeat):
            suite.addTest(unittest.makeSuite(cls))

    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)

if __name__ == '__main__':
    run()
