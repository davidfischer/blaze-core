'''Tests of blaze.metadata package.'''
import blaze
import unittest

tests = []

class TestMetadata(unittest.TestCase):

    def test_metadata_has_prop(self):
        a = blaze.ones(blaze.dshape('20, 20, float64'))
        c = blaze.NDTable([(1.0, 1.0), (1.0, 1.0)], dshape='2, {x: int32; y: float32}')

        self.assertTrue( blaze.metadata.has_prop(a, blaze.metadata.arraylike) )
        self.assertTrue( blaze.metadata.has_prop(c, blaze.metadata.tablelike) )
        self.assertTrue( not blaze.metadata.has_prop(a, blaze.metadata.tablelike) )

    def test_metadata_all_prop(self):
        a = blaze.ones(blaze.dshape('20, 20, float64'))
        b = blaze.zeros(blaze.dshape('20, 20, float64'))
        c = blaze.NDTable([(1.0, 1.0), (1.0, 1.0)], dshape='2, {x: int32; y: float32}')

        self.assertTrue( blaze.metadata.all_prop((a, b), blaze.metadata.arraylike) )
        self.assertTrue(not blaze.metadata.all_prop((a, b, c), blaze.metadata.arraylike))

tests.append(TestMetadata)

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
