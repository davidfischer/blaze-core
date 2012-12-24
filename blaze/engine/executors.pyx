cimport cpython
from libc.stdlib cimport malloc, free
cimport numpy as cnp
from cpython cimport PyObject, Py_INCREF

from blaze.sources.descriptors cimport lldescriptors

#------------------------------------------------------------------------
# NumPy Utilities
#------------------------------------------------------------------------

import numpy as np

cdef extern from "Python.h":
    ctypedef unsigned int Py_uintptr_t

cdef extern from "numpy/arrayobject.h":
    object PyArray_NewFromDescr(
            PyObject *subtype, object descr, int nd,
            cnp.npy_intp* dims, cnp.npy_intp* strides,
            void* data, int flags, PyObject *obj)

cnp.import_array()

cdef build_fake_array(dtype):
    "Build a numpy array without data"
    cdef cnp.npy_intp shape = 0
    cdef cnp.npy_intp strides = dtype.itemsize
    cdef int flags = cnp.NPY_C_CONTIGUOUS | cnp.NPY_WRITEABLE

    # PyArray_NewFromDescr will steal our reference
    Py_INCREF(dtype)

    array = PyArray_NewFromDescr(
        <PyObject *> np.ndarray,        # subtype
        dtype,                          # descr
        1,                              # ndim
        &shape,                         # shape
        &strides,                       # strides
        <void *> 1,                     # data
        flags,                          # flags
        NULL,                           # obj
    )

    return array

#------------------------------------------------------------------------
# Various forms of Executors
#------------------------------------------------------------------------

cdef class Executor(object):

    cdef public object strategy
    cdef public object operation # for debugging and printing

    def __init__(self, strategy, operation="<operation>"):
        # assert strategy in ('chunked', 'tiled', 'indexed')
        self.strategy = strategy
        self.operation = operation

    def __call__(self, operands, out_operand):
        "Execute a kernel over the data given the operands and the LHS"
        # print operands, out_operand
        method = getattr(self, "execute_%s" % self.strategy)
        return method(operands, out_operand)

    def execute_chunked(self, operands, out_operand):
        cdef int i
        cdef void **data_pointers
        cdef void *lhs_data

        cdef lldescriptors.Chunk chunk

        operands.append(out_operand)
        descriptors = [op.data.read_desc() for op in operands]

        nbtyes = descriptors[0].nbytes
        assert all(desc.nbytes == nbtyes for desc in descriptors)

        data_pointers = <void **> malloc(len(operands) * sizeof(void *))
        if data_pointers == NULL:
            raise MemoryError

        try:
            # TODO: match up chunks of different sizes
            iterators = [desc.as_chunked_iterator() for desc in descriptors]
            for paired_chunks in zip(*iterators):
                paired_chunks, lhs_chunk = paired_chunks[:-1], paired_chunks[-1]
                for i, chunk in enumerate(paired_chunks):
                    data_pointers[i] = chunk.chunk.data

                chunk = lhs_chunk
                lhs_data = chunk.chunk.data

                self.execute_chunk(data_pointers, lhs_data,
                                   chunk.chunk.size)

                for it, chunk in zip(iterators, paired_chunks):
                    it.dispose(chunk)

                iterators[-1].commit(lhs_chunk)
        finally:
            free(data_pointers)

    cdef execute_chunk(self, void **data_pointers, void *out, size_t size):
        raise NotImplementedError

    def __repr__(self):
        return "Executor(%s, %s)" % (self.strategy, self.operation)

#------------------------------------------------------------------------
# Numba Executors
#------------------------------------------------------------------------

cdef class ElementwiseLLVMExecutor(Executor):

    cdef object ufunc, result_dtype
    cdef list operands, dtypes
    cdef object lhs_array
    cdef void *lhs_data

    def __init__(self, strategy, ufunc, dtypes, result_dtype, **kwargs):
        super(ElementwiseLLVMExecutor, self).__init__(strategy, **kwargs)
        self.ufunc = ufunc
        self.result_dtype = result_dtype

        self.operands = []
        for dtype in dtypes:
            array = build_fake_array(dtype)
            self.operands.append(array)

        self.lhs_array = build_fake_array(result_dtype)

    cdef execute_chunk(self, void **data_pointers, void *out, size_t size):
        """
        Execute a kernel over the data

        TODO: strides, reductions
        """
        cdef int i
        cdef size_t itemsize
        cdef cnp.ndarray op

        for i, operand in enumerate(self.operands):
            op = self.operands[i]
            op.data = <char *> data_pointers[i]
            op.shape[0] = size
            # print hex(<Py_uintptr_t> op.data), size

        if out == NULL:
            raise NotImplementedError

        op = self.lhs_array
        op.data = <char *> out
        op.shape[0] = size

        # print "lhs", hex(<Py_uintptr_t> op.data), size
        self.ufunc(*self.operands, out=self.lhs_array)

    def __repr__(self):
        return "LLVMExecutor(%s, %s)" % (self.strategy, self.operation)
