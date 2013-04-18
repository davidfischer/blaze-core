# This file defines the Concrete Array --- a leaf node in the expression graph
#
# A concrete array is constructed from a Data Descriptor Object, a Data Shape Object, a MetaData Object
#  and a few addtional attributes that are meant for convenience (i.e. flags

from datadescriptor import Descriptor
from datashape import dshape

# An NDArray is a
#   Sequence of Bytes (where are the bytes)
#   Index Object (how do I get to them)
#   Data Shape Object (what are the bytes? how do I interpret them)
#   Meta-data (axis and dimension labels and other internal meta-data, internal dictionary)
#   user-defined meta-data (whatever are needed --- provenance propagation)
class NDArray(object):
    def __init__(self, data, **user):
        assert isinstance(data, DataDescriptor)
        self.data = data
        self._meta = {'axes': ['']*self.nd,
                      'labels' : [None]*self.nd,
                      }
        self.user = user
        # Need to inject attributes on the NDArray depending on dshape attributes
        
    @staticmethod
    def fromfiles(list_of_files, converters):
        raise NotImplementedError

    @staticmethod
    def fromfile(file, converter):
        raise NotImplementedError

    @staticmethod
    def frombuffers(list_of_buffers, converters):
        raise NotImplementedError

    @staticmethod
    def frombuffer(buffer, converter):
        raise NotImplementedError        

    @staticmethod
    def fromobjects():
        raise NotImplementedError

    @staticmethod
    def fromiterator(buffer):
        raise NotImplementedError        

    @property
    def shape(self):
        return self._dshape.shape

    @property
    def nd(self):
        return len(self.shape)


    def __getitem__(self, key):
        
