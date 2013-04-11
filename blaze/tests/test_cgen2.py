import unittest
import numpy as np

from blaze.blir import compile, assembly, bitcode, Context, execute
from blaze.cgen.utils import namesupply
from blaze.cgen.kernels import *
from blaze.cgen.blirgen import *

tests = []

#------------------------------------------------------------------------

class TestBlirGen(unittest.TestCase):

    def test_cgen2_expadd(self):
        with namesupply():

            krn = ElementwiseKernel(
                [
                    (IN  , VectorArg((300,), 'array[float]')),
                    (IN  , VectorArg((300,), 'array[float]')),
                    (OUT , VectorArg((300,), 'array[float]')),
                ],
                '_out0[i0] = exp(_in0[i0] + _in1[i0])',
            )

            krn.verify()
            ast, env = krn.compile()

            ctx = Context(env)

            a = np.array(xrange(300), dtype='double')
            b = np.array(xrange(300), dtype='double')
            c = np.empty_like(b)

            execute(ctx, args=(a,b,c), fname='kernel0', timing=False)
            self.assertTrue( np.allclose(c, np.exp(a + b)) )

    def test_cgen2_add(self):
        with namesupply():

            krn = ElementwiseKernel(
                [
                    (IN  , VectorArg((300,), 'array[int]')),
                    (IN  , VectorArg((300,), 'array[int]')),
                    (OUT , VectorArg((300,), 'array[int]')),
                ],
                '_out0[i0] = _in0[i0] + _in1[i0]',
            )

            krn.verify()
            ast, env = krn.compile()

            ctx = Context(env)

            a = np.array(xrange(300), dtype='int32')
            b = np.array(xrange(300), dtype='int32')
            c = np.empty_like(b)

            execute(ctx, args=(a,b,c), fname='kernel0', timing=False)
            self.assertTrue( np.allclose(c, a + b) )


tests.append(TestBlirGen)

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
