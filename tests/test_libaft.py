# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from eaftest import libaft


# Dados usados nos exemplos em A.Guerreiro MSc, Chap2
simple_run1 = [(1,10), (7,4), (9,3)]
simple_run2 = [(3,9), (4,7), (8,1)]
simple_run3 = [(2,8), (5,6), (6,5), (10,2)]
simple_npsets = [simple_run1, simple_run2, simple_run3]


def test_eaf2d_simple():
    pointsets, indicators = libaft.eaf2d(simple_npsets)
    expected_pointsets = [
        [(8.0, 1.0), (7.0, 4.0), (6.0, 5.0), (5.0, 6.0),
         (4.0, 7.0), (2.0, 8.0), (1.0, 10.0)],
        [(10.0, 2.0), (9.0, 3.0), (8.0, 4.0), (7.0, 5.0),
         (5.0, 7.0), (4.0, 8.0), (3.0, 9.0), (2.0, 10.0)],
        [(10.0, 3.0), (8.0, 5.0), (7.0, 7.0), (3.0, 10.0)]
    ]
    expected_indicators = [
        [[0, 1, 0], [1, 0, 0], [0, 0, 1], [0, 0, 1],
         [0, 1, 0], [0, 0, 1], [1, 0, 0]],
        [[0, 1, 1], [1, 1, 0], [1, 1, 0], [1, 0, 1],
         [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 0, 1]],
        [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]
    ]
    assert pointsets == expected_pointsets
    assert indicators == expected_indicators


