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
