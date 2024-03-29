# FIXME: Python 2 only!
# -*- coding: utf-8 -*-

import os, sys
import numpy as np
import pyopencl as cl
from time import time, clock
from .clkernels import loadkernel
from .bintools import pack_arrays_uint32
from .datasets import load_ind

# Compilation errors & warnings output
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'
# Use the first opencl device
os.environ['PYOPENCL_CTX'] = '0'

def data_attributes(bdata, bmask):
    npoints, unitspp = bdata.shape
    permutations, _  = bmask.shape
    bytespu = bdata.dtype.itemsize
    return npoints, permutations, unitspp, bytespu

def runkernel(indicators, masks):
    # Create context and command queue
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)
    
    # Make indicator & permutation masks binary data
    data, mask, nvars = pack_arrays_uint32(indicators, masks)
    # Data attributes: number of points, permutations, units per point, bytes per unit
    npoints, perms, unitspp, bytespu = data_attributes(data, mask)
    
    # Create device buffers
    mf = cl.mem_flags
    databuf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data)
    maskbuf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=mask)
    
    # Maximal distance array
    dist = np.zeros(512, dtype=np.int32)
    distbuf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=dist)
    
    # Kernel arguments
    kargs = {"npoints": npoints, "intpp": unitspp,
             "bytespu": bytespu, "nvars": nvars, "masklen": nvars//2}
    
    # Kernel custom arguments
    tblock, pblock = 64, 8
    tdivs = (npoints-1)//tblock + 1
    kargs.update(tblock=tblock, pblock=pblock)
    
    # Load and build kernel
    #print "DEBUG:", " ; ".join("%s: %s" % (k, v) for k, v in kargs.items())
    kstr, kopt = loadkernel("square-3-xor-parted", **kargs)
    prg = cl.Program(ctx, kstr).build(options=kopt)
    
    # Run kernel
    globalsize, localsize = (512//pblock, tdivs), (tblock, 1)
    
    for z in xrange(0, permutations//pblock, 512//pblock):
        dist[:] = 0
        cl.enqueue_copy(queue, distbuf, dist)
        for i in range(tdivs):
            prg.eaf_test2(queue, globalsize, localsize, databuf, maskbuf, distbuf,
                np.int32(z), np.int32(i)).wait()
        cl.enqueue_copy(queue, dist, distbuf)
        # Yield 512 maximum distances
        for d in dist:
            yield d



