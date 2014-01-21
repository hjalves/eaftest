#!/usr/bin/env python   
# -*- coding: utf-8 -*-
# aft tests

import aft
import datasets

npsets = datasets.load_multiple_nps("datasets/ds100")
lt, ind = aft.eaf2d(npsets['optimA'], ind=True)
print datasets.nps_stats(lt)

# calcular os indicadores com o eaf conjunto optimA + optimC
lt, ind = aft.eaf2d(npsets['optimA'] + npsets['optimC'], ind=True)
# espalmar lista: lista de (m listas) * (n pontos) -> lista de m * n pontos
point_ind = [point for level in ind for point in level]

print "number of points:\t", len(point_ind)
print "vars (executions):\t", len(point_ind[0])
print "total number of bits:\t", len(point_ind[0])*len(point_ind)

stat1 = aft.ksstat(point_ind, 1)
stat2 = aft.ksstat(point_ind, 2)

print "C 1st order test statistic", stat1
print "C 2nd order test statistic", stat2

#----------
from eaf_test_kscoarse import runkernel
from time import time
import numpy as np

nvars = len(point_ind[0])
permutations = 10240
gen = runkernel(point_ind, permutations)
# Max distance array
maxdist = np.zeros(permutations, dtype=np.int32)
real = time()
for i, maxd in enumerate(gen):
    maxdist[i] = maxd
    if (i+1) % 512 == 0:
        print "%6d perms, %7.3f sec" % (i+1, time() - real)
    if (i+1) % 1024 == 0:
        print "tail:", np.bincount(maxdist[:i+1], minlength=nvars//2+1)

print "total elapsed", time() - real

