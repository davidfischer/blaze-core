import unittest

from textwrap import dedent
from blaze.cgen.blirgen import *

#------------------------------------------------------------------------
# Code Generation ( Level 1 )
#------------------------------------------------------------------------

# Level 1 just tests syntatic construction.

class TestCgenLevel1(unittest.TestCase):

    def test_compose(self):
        x = Assign('a', '3')
        y = Arg('int', 'a')
        z = VarDecl('int', 'x', '0')

        loop = For('x', Range('1', '2'), Block([x]))

        body = Block([z, loop])

        fn = FuncDef(
            name = 'kernel',
            args = [y],
            ret = 'void',
            body = body,
        )

        # XXX
        assert str(fn) is not None


tests.append(TestCgenLevel1)

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
