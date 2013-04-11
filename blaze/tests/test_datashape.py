import unittest
from blaze.datashape import *

tests = []

#------------------------------------------------------------------------

a = IntegerConstant(800)
b = IntegerConstant(600)
c = IntegerConstant(300)

class TestDatashapeConstruct(unittest.TestCase):

    def test_associative(self):
        sig1 = a * (b * int64)
        sig2 = (a * b) * int64
        sig3 = a * b * int64
        self.assertTrue( sig1.parameters == sig2.parameters == sig3.parameters )

    def test_associative2(self):
        sig1 = a * (b * c * (int64))
        sig2 = ((a * b) * c) * int64
        sig3 = a * b * c * int64
        sig4 = a * ( b * c ) * int64

        self.assertTrue(
            sig1.parameters == sig2.parameters ==
            sig3.parameters == sig4.parameters
            )

    def test_coersion(self):
        sig1 = IntegerConstant(2)*int64
        sig2 = IntegerConstant(3)*IntegerConstant(2)*int64

        self.assertTrue( isinstance(sig1[0], IntegerConstant) )
        self.assertTrue( isinstance(sig2[0], IntegerConstant) )

    def test_fromlist(self):
        it = (a, b, int64)
        ds = DataShape(parameters=it)

        x,y,z = tuple(ds)
        self.assertTrue( all([x is a, y is b, z is int64]) )

    def test_fromlist_compose(self):
        it1 = (a, b)
        it2 = (int64, )
        ds1 = DataShape(parameters=it1)
        ds2 = DataShape(parameters=it2)

        ds = ds1 * ds2

        self.assertEqual( ds[2] , int64 )

    def test_fromlist_compose2(self):
        it1 = (a, b)
        it2 = (int64, )
        ds1 = DataShape(parameters=it1)
        ds2 = DataShape(parameters=it2)

        ds_x = ds1 * ds2
        ds_y = DataShape(parameters=(ds1, ds2))

        self.assertEqual( list(ds_x) , list(ds_y) )

    def test_iteration(self):
        ds = DataShape(parameters=[a,a,a])

        ds2 = (ds * ds) * int64

        self.assertEqual(ds2[0], a)
        self.assertEqual(ds2[1], a)
        self.assertEqual(ds2[-1], int64 )


tests.append(TestDatashapeConstruct)

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
