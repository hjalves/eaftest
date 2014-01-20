#!/usr/bin/env python   
# -*- coding: utf-8 -*-
# Dataset input/output using native Python structures
# statistics (min, max, avg number of points...) and other helper functions

from glob import glob
import os
from itertools import groupby

# Load random non-dominated point sets from files

def load_nps(filename):
    """Loads non-dominated point set generated by multiple runs of an optimizer"""
    with open(filename) as f:
        points = [tuple(float(p) for p in line.strip().split()) for line in f]
        # groups points based on empty tuples (bool()) == False
        return [list(group) for k, group in groupby(points, bool) if k]

def load_multiple_nps(pathdir, fileext='.rnp.txt'):
    """Loads multiple np sets from multiple files, returning dict name->sets"""
    npsets = {}
    for filepath in glob(os.path.join(pathdir, '*' + fileext)):
        optimizer = os.path.basename(filepath)[:-len(fileext)]
        npsets[optimizer] = load_nps(filepath)
    return npsets

# Save random non-dominated point sets to files

def save_nps(nps, filename):
    """Saves non-dominated point set to a text file"""
    with open(filename, 'w') as f:
        for level in nps:
            f.writelines("{} {}\n".format(*p) for p in level)
            f.write("\n")
    
def save_multiple_nps(npsd, pathdir, fileext='.rnp.txt'):
    """Saves non-dominated point set dictionary to multiple text files"""
    if not os.path.exists(pathdir):
        os.makedirs(pathdir)
    for name, nps in npsd.items():
        filename = os.path.join(pathdir, name + fileext)
        save_nps(nps, filename)

# Simple statistics for the point sets

def nps_stats(nps):
    """Provides min, max, avg number of points and runs from a nps data structure"""
    pnum = map(len, nps)
    nruns = len(pnum)
    pmax, pmin, pavg = max(pnum), min(pnum), float(sum(pnum))/nruns
    return {"runs": nruns, "pmax": pmax, "pmin": pmin, "pavg": pavg}

def nps_multiple_stats(npsd):
    """Provides stats for multiple optimizer outputs"""
    return {name: nps_stats(nps) for name, nps in npsd.items()}

# Attainment surfaces data (EAF computation output)

def load_ind(filename, flat=False):
    """Load an indicator file"""
    with open(filename) as f:
        if flat:
            return [map(int, line.split()) for line in f if line.strip()]
        else:
            points = [map(int, line.split()) for line in f]
            return [list(group) for k, group in groupby(points, bool) if k]

def attdata_filter(nps, ind):
    """Removes points from the attlevel if they are already present in another upper level"""
    new_nps = [[] for level in nps]
    new_ind = [[] for level in nps]
    for num, (pset, iset) in enumerate(zip(nps, ind)):
        for p, i in zip(pset, iset):
            if sum(i) == num+1:
                new_nps[num].append(p)
                new_ind[num].append(i)
    return new_nps, new_ind

def print_attdata(nps, ind):
    """Print surface attainment points with indicator data"""
    for num, (pset, iset) in enumerate(zip(nps, ind), 1):
        print "="*26, "att %02d/%02d" % (num, len(nps)), "="*26
        for p, i in zip(pset, iset):
                print "%s : %s : %d" % ( ",".join("%8.2f" % c for c in p),
                                         "".join(map(str, i)), sum(i) )

if __name__ == '__main__':
    import aft
    npsd = load_multiple_nps("datasets/ds100")
    lt, ind = aft.eaf2d(npsd['optimA'], ind=True)
    print nps_stats(lt)
    #lt, ind = attdata_filter(lt, ind)
    #print_attdata(lt, ind)
    
    
