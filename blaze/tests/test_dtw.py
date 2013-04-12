import unittest

from blaze import dshape, fromiter
from blaze.ts.ucr_dtw import ucr
from math import sin, pi
from nose.tools import ok_, eq_

tests = []

#------------------------------------------------------------------------

class TestDynamicTimeWarp(unittest.TestCase):

    def test_dtw(self):
        # note: ucr.dtw only supports float64 atm
        count = 100
        data  = fromiter((sin(2*pi*i/count) for i in xrange(count)), 'x, float64')
        query = data[50:60]

        loc, dist = ucr.dtw(data, query, 0.1, verbose=False)

        # these are stupid, mostly just to check for regressions
        self.assertTrue(isinstance(loc, (int, long)))
        self.assertTrue(isinstance(dist, float))
        self.assertEqual(loc, 50)
        self.assertTrue((dist < 1e-10 and dist >= 0.0))

tests.append(TestDynamicTimeWarp)

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
