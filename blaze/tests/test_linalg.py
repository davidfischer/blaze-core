# adapted from samples/dot_example.py

import blaze
from blaze.algo.linalg import dot
from blaze.test_utils import assert_raises

import unittest

tests = []

#------------------------------------------------------------------------

class TestLinalg(unittest.TestCase):

    def test_dot(self):
        '''Test of 2D dot product'''
        a = blaze.ones(blaze.dshape('20, 20, float64'))
        b = blaze.ones(blaze.dshape('20, 30, float64'))
        # Do not write output array to disk
        out = dot(a, b, outname=None)

        expected_ds = blaze.dshape('20, 30, float64')
        self.assertTrue( out.datashape._equal(expected_ds) )
        # FIXME: Slow, but no other way to do this with Array API implemented so far
        for row in out:
            for elem in row:
                self.assertTrue( abs(elem - 20.0) < 1e-8 )

    def test_dot_not2d_exception(self):
        '''Dot product of arrays other than 2D should raise exception.'''
        a = blaze.ones(blaze.dshape('20, 20, 20, float64'))
        b = blaze.ones(blaze.dshape('20, 20, 20, float64'))

        with assert_raises(ValueError):
            out = dot(a, b, outname=None)

    def test_dot_shape_exception(self):
        '''Dot product with wrong inner dimensions should raise exception.'''
        a = blaze.ones(blaze.dshape('20, 20, float64'))
        b = blaze.ones(blaze.dshape('30, 30, float64'))

        with assert_raises(ValueError):
            out = dot(a, b, outname=None)

    def test_dot_out_exception(self):
        '''Output array of wrong size should raise exception.'''
        a = blaze.ones(blaze.dshape('20, 20, float64'))
        b = blaze.ones(blaze.dshape('20, 30, float64'))
        out = blaze.zeros(blaze.dshape('20, 20, float64'))

        with assert_raises(ValueError):
            dot(a, b, out=out)

tests.append(TestLinalg)

#------------------------------------------------------------------------

def run(verbosity=1, repeat=1):
    suite = unittest.TestSuite()
    for cls in tests:
        for _ in range(repeat):
            suite.addTest(unittest.makeSuite(cls))

    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)

if __name__ == '__main__': run()
