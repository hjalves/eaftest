[![Build Status](https://travis-ci.org/hjalves/eaftest.svg?branch=master)](https://travis-ci.org/hjalves/eaftest)

Second-order EAF KS-like two-sample two-sided test
==================================================

Command line tool usage:
```
eaftest <fileA> <fileB>
eaftest -i <indicators_file>

<fileA> and <fileB>: non-dominated sets of two-dimensional
                     objective vectors
<indicators_file>: point indicator file from the joint-eaf
                   computation
```

Current limitations:
- second-order only
- maximum executions: 64 (32 + 32)
- permutations: 10240 (fixed)
- significance level: 0.05 (fixed)
