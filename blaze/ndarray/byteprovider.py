"""
ByteProvider base class.
"""

# FIXME: for creating new read-write buffers
import numpy as np

from ..byteproto import READ, WRITE, CONST
defaultN = 8000

"""
    The ByteProvider provides a wrapper around bytes.  The bytes can be from
    any source imagineable.   ByteProviders are always 1 dimensional but they can be
    a concatenation of multiple sources
       * the original source (object referencing the source --- can be a list of sources
         but STREAM source must be final source)
       * a memory object that should be read from (data understandable by data-shape system)
       * buflen = number of bytes of memory object
       * the number of bytes for this object (-1 for STREAM)
       * kind (STREAM, MEMORY, FILE, GPU)
       
       If a source is a dictionary, then a key of "source" is the source object and
       the key "map" is a callable that returns a buffer object from the first argument
       
       READ -- can READ from
       WRITE -- can WRITE to
       CONST -- data is immutable

    bytes should be accessed from the buffer object (which points either to the original source,
    or buffers from it).
"""

# Default is just a single object which it creates a read-only buffer from
class ByteProvider(object):
    def __init__(self, obj):
        self.original = obj
        self.buffer = memoryview(obj)
        self.buflen = len(self.buffer) * self.buffer.itemsize        
        self.nbytes = self.buflen
        self.flags = CONST | READ
        
    # Point self.buffer to the next chunk
    #   limit any data-copy or file-read to N bytes
    def nextchunk(self, N=defaultN): 
        raise StopIteration

class NumPyBytes(ByteProvider):
    def __init__(self, arr):
        self.original = arr
        self.buffer = memoryview(arr)
        self.buflen = arr.nbytes
        self.nbytes = self.buflen
        self.flags = READ | (WRITE if arr.flags.writeable else 0)

class ValueBytes(ByteProvider):
    def __init__(self, tup_or_N):
        self.original = tup_or_N
        val = 0
        dt = 'B'
        if isinstance(tup_or_N, tuple):
            N = tup[0]
            if len(tup) > 1:
                val = tup[1]
            if len(tup) > 2:
                dt = tup[2]
        else:
            N = tup_or_N          
        arr = np.empty(N, dtype=dt)
        arr.fill(val)
        
        self.buffer = memoryview(arr)
        self.buflen = arr.nbytes
        self.nbytes = self.buflen
        self.flags = READ | WRITE

class FileBytes(ByteProvider):
    def __init__(self, filespec):
        if isinstance(filespec, file):
            fid = filespec
        elif isinstance(filespec, (str, unicode)):
            fid = open(filespec, 'rb')
        elif isinstance(filespec, tuple) and len(filespec) > 1:
            fid = open(filespec[0], filespec[1]+'b')

        # Setup memory-map
        # create memory view from a slice of the file
        self._offset = 0
        fid.seek(0,2)
        self._filesize = fid.tell()
        fid.seek(0)
        self._mmap = mmap.mmap(fid.fileno(), 0)

        # Not finished...
        
