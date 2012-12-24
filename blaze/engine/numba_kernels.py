"""
Kernels written in Numba.
"""

from numba import *

char_pp = char.pointer().pointer()

@autojit(locals={'data_pointers_': Py_uintptr_t,
                 'stride': Py_ssize_t,
                 'size': size_t})
def numba_full_reduce(data_pointers_, strides, size, reduce_kernel,
                      dst_type, dst_type_p):
    data_pointers = char_pp(data_pointers_)
    rhs_data = data_pointers[0]
    lhs_data = dst_type_p(data_pointers[1])

    if size == 0:
        return

    result = dst_type_p(rhs_data)[0]
    for i in range(size - 1):
        rhs_data = rhs_data + stride
        value = dst_type_p(rhs_data)[0]
        result = reduce_kernel(result, value)

    lhs_data[0] = result
