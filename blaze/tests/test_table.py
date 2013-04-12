from blaze import dshape
from blaze import NDTable, Table, NDArray, Array

import unittest

tests = []

class TestConstructors(unittest.TestCase):

    def test_arrays(self):
        # Assert that the pretty pritner works for all of the
        # toplevel structures

        expected_ds = dshape('3, int')

        a = NDArray([1,2,3])
        str(a)
        repr(a)
        a.datashape._equal(expected_ds)

        a = Array([1,2,3])
        str(a)
        repr(a)
        a.datashape._equal(expected_ds)


    def test_record(self):
        expected_ds = dshape('1, {x: int32; y: float32}')

        t = NDTable([(1, 2.1), (2, 3.1)], dshape='1, {x: int32; y: float32}')
        t.datashape._equal(expected_ds)

        str(t)
        repr(t)

    def test_record_consume(self):
        expected_ds = dshape("4, {i: int64; f: float64}")

        d = {
            'i'   : [1, 2, 3, 4],
            'f'   : [4., 3., 2., 1.]
        }
        t = NDTable(d)
        t.datashape._equal(expected_ds)

    def test_record_consume2(self):
        d = {
            'a'   : ["foo", "bar"],
            'b'   : [4., 3., 2., 1.]
        }
        table = NDTable(d)


    @unittest.skip('')
    def test_custom_dshape(self):
        from blaze import RecordDecl, derived
        from blaze import int32
        class CustomStock(RecordDecl):
            max    = int32
            min    = int32

            @derived
            def mid(self):
                return (self.min + self.max)/2

        a = Table([('GOOG', 120, 153)], CustomStock)


tests.append(TestConstructors)

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
