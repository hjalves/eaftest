#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# aft tests

from eaf_test_kscoarse import runkernel
from time import time
import numpy as np
import aft
import datasets


def criticalvalue(tail, alpha):
    """Derive a critical value (tail index) from a null distribution"""
    cumtail = np.cumsum(tail[::-1])
    # Valor crítico. Atenção! Não é a mesma convenção do aft-test...
    # este valor crítico ainda pertence à região crítica!
    critvalue = (i for i, p in enumerate(cumtail[::-1]) if p < alpha).next()
    return critvalue

def pvalue(tail, stat):
    """Derive p-value from a test statistic and null distribution"""
    pvalue = 0
    for i in range(len(tail)-1, stat-1, -1):
        pvalue += tail[i]
    return pvalue

def eafindicators(npsA, npsB):
    """From the output of two optimizers (NP sets), get eaf indicators"""
    # calcular os indicadores com o eaf conjunto
    lt, ind = aft.eaf2d(npsA + npsB, ind=True)
    # espalmar lista, ou seja,
    # (m listas) * (n pontos) * (b bits) -> lista de (m * n pontos) * (b bits)
    flat_ind = [point for level in ind for point in level]
    return flat_ind

if __name__ == '__main__':

    # dataset load: non-dominated point set
    npsets = datasets.load_multiple_nps("datasets/ds100")
    lt, ind = aft.eaf2d(npsets['optimA'], ind=True)
    print datasets.nps_stats(lt)
    # joint-eaf point indicators
    point_ind = eafindicators(npsets['optimA'], npsets['optimC'])

    print "number of points:\t", len(point_ind)
    print "vars (executions):\t", len(point_ind[0])
    print "total number of bits:\t", len(point_ind[0])*len(point_ind)


    stat1 = aft.ksstat(point_ind, 1)
    stat2 = aft.ksstat(point_ind, 2)


    print "C 1st order test statistic", stat1
    print "C 2nd order test statistic", stat2


    #----------


    nvars = len(point_ind[0])                   # Número de execuções total
    nruns = nvars // 2                          # Número de execuções de 1 algo

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

    alpha = 0.05
    tail = np.bincount(maxdist, minlength=nvars//2+1)
    crit = criticalvalue(tail, alpha * permutations) - 1
    #crit /= float(nruns)
    pval = pvalue(tail, stat2)
    pval /= float(permutations)

    print "critical value: %d/%d" % (crit, nruns)
    print "critical value", crit / float(nruns)
    print "pval", pval
