"""
Tests for the blob data type.
"""

import blaze
import unittest
import tempfile, shutil, os.path

tests = []

class TestVlenDatashape(unittest.TestCase):

    def test_simple_blob(self):
        ds = blaze.dshape('x, blob')
        c = blaze.Array(["s1", "sss2"], ds)

        self.assertEqual( c[0] , "s1" )
        self.assertEqual( c[1] , "sss2" )

    def test_simple_persistent_blob(self):
        td = tempfile.mkdtemp()
        tmppath = os.path.join(td, 'c')

        ds = blaze.dshape('x, blob')
        c = blaze.Array(["s1", "sss2"], ds,
                        params=blaze.params(storage=tmppath))

        self.assertEqual( c[0] , "s1" )
        self.assertEqual( c[1] , "sss2" )

        # Remove everything under the temporary dir
        shutil.rmtree(td)

    def test_object_blob(self):
        ds = blaze.dshape('x, blob')
        c = blaze.Array([(i, str(i*.2)) for i in range(10)], ds)

        for i, v in enumerate(c):
            self.assertEqual( v[0] , i )
            self.assertEqual( v[1] , str(i*.2) )

    def test_object_unicode(self):
        ds = blaze.dshape('x, blob')
        c = blaze.Array([u'a'*i for i in range(10)], ds)

        for i, v in enumerate(c):
            # The outcome are 0-dim arrays (that might change in the future)
            self.assertEqual( v[()] , u'a'*i )

    def test_object_persistent_blob(self):
        td = tempfile.mkdtemp()
        tmppath = os.path.join(td, 'c')

        ds = blaze.dshape('x, blob')
        c = blaze.Array([(i, str(i*.2)) for i in range(10)], ds,
                        params=blaze.params(storage=tmppath))

        for i, v in enumerate(c):
            self.assertEqual( v[0] ,  i )
            self.assertEqual( v[1] , str(i*.2) )

        # Remove everything under the temporary dir
        shutil.rmtree(td)

    def test_object_persistent_blob_reopen(self):
        td = tempfile.mkdtemp()
        tmppath = os.path.join(td, 'c')

        ds = blaze.dshape('x, blob')
        c = blaze.Array([(i, "s"*i) for i in range(10)], ds,
                        params=blaze.params(storage=tmppath))

        c2 = blaze.open(tmppath)

        for i, v in enumerate(c2):
            self.assertEqual( v[0] , i )
            self.assertEqual( v[1] , "s"*i )

        # Remove everything under the temporary dir
        shutil.rmtree(td)

    def test_intfloat_blob(self):
        ds = blaze.dshape('x, blob')
        c = blaze.Array([(i, i*.2) for i in range(10)], ds)

        for i, v in enumerate(c):
            #print "v:", v, v[0], type(v[0])
            self.assertEqual( v[0] , i )
            self.assertEqual( v[1] , i*.2)


tests.append(TestVlenDatashape)

def run(verbosity=1, repeat=1):
    suite = unittest.TestSuite()
    for cls in tests:
        for _ in range(repeat):
            suite.addTest(unittest.makeSuite(cls))

    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)

if __name__ == '__main__':
    run()
