__version__ = '0.1-dev'

from datashape import dshape
from table import Array, Table, NDArray, NDTable

# From numpy compatability, ideally ``import blaze as np``
# should be somewhat backwards compatable
array   = Array
ndarray = NDArray
dtype   = dshape

# Install the Blaze library of dispatch functions
import lib

# Shorthand namespace dump
from datashape.shorthand import *

# Record class declarations
from datashape.record import RecordDecl, derived

# The compatability wrappers
from datashape.coretypes import to_numpy, from_numpy

# Errors
from blaze.error import *
