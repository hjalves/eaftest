#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 

import sys
import datasets
import aft
import time
from eaf_test_kscoarse import runkernel
from aft_test import criticalvalue, pvalue, eafindicators
import numpy as np


def main(args):
    print
    print "Second-order EAF KS-like two-sample two-sided test"
    print "=================================================="
    print 
    
    if len(args) < 3:
        print "Usage: %s <fileA> <fileB>" % args[0]
        print
        return
    
    eaftest(args[1], args[2])


def eaftest(fileA, fileB):

    # ------ Loading files ------

    print "- Loading the following non-dominated sets of two-dimensional"
    print "  objective vectors and computing the joint-EAF:"
    print "  * A:", fileA
    print "  * B:", fileB, '\n'
    
    npsetA = datasets.load_nps(fileA)
    npsetB = datasets.load_nps(fileB)
    assert len(npsetA) == len(npsetB), ("The npsets must have the same length "
        "(i.e. same number of executions)")
    
    # ------ EAF and get attainment indicator values ------

    
    point_ind = eafindicators(npsetA, npsetB)
    
    npoints = len(point_ind)
    nvars = len(point_ind[0])                   # Número de execuções total
    nruns = nvars // 2                          # Número de execuções de 1 algo
    
    print "- Attainment indicator values information:"
    print "  * Number of points:", npoints
    print "  * Joint executions:", nvars, "(%d + %d)" % (nruns, nruns), '\n'
    
    assert nvars % 2 == 0, "Number of total joint executions must be even."
    assert nvars <= 64, "Not implemented with more than 64 joint executions."
    
    # ------ Test Statistic ------

    print "- Computing the test statistic..."    
    
    stat2 = aft.ksstat(point_ind, 2)
    
    print "  * Test statistic = %d/%d" % (stat2, nruns)
    print "                   = %f" % (stat2 / float(nruns)), '\n'
    
    # ------ Estimate null distribution ------
    
    permutations = 10240
    
    print "- Using %d random permutations to estimate null distribution." % permutations
    print "  Please be patient..."

    gen = runkernel(point_ind, permutations)
    maxdist = np.zeros(permutations, dtype=np.int32)    # Max distance array
    rtime = time.time()
    for i, maxd in enumerate(gen):
        maxdist[i] = maxd
        if (i+1) % (permutations//8) == 0:
            print "    %6d permutations, %7.3f sec" % (i+1, time.time()-rtime)
        #if (i+1) % 1024 == 0:
        #    print "tail:", np.bincount(maxdist[:i+1], minlength=nvars//2+1)
    print "  * Time elapsed: %7.3f" % (time.time()-rtime)
    
    # Compute null distribution from max distance array
    tail = np.bincount(maxdist, minlength=nruns+1)
    print "  * Non-normalized null distribution:"
    print tail
    print 
    
    
    # ------ Accept/reject null hypothesis ------

    alpha = 0.05        # significance level
    
    # NB: -1 resulta de diferentes convenções para a definição de valor crítico
    crit = criticalvalue(tail, alpha * permutations) - 1
    #crit /= float(nruns)
    pval = pvalue(tail, stat2) / float(permutations)
    
    print "- Null hypothesis final decision:"  
    print "  * Critical value = %d/%d" % (crit, nruns)
    print "                   = %f" % (crit / float(nruns))
    print "  * p-value = %f" % pval
    if pval <= alpha:
        csym = '=' if pval == alpha else '<'
        print "            %s alpha (%s)" % (csym, alpha)
        print "  * Decision: REJECT the null hypothesis"
    else:
        print "            > alpha (%s)" % alpha
        print "  * Decision: do NOT REJECT the null hypothesis"
    print
        
    
    

if __name__ == '__main__':
    #sys.system("make -f 
    main(sys.argv)
