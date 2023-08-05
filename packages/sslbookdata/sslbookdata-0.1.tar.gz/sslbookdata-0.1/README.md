# sslbookdata #

This python module provides functions to load the 9 data sets published in the book "Semi-Supervised Learning".

They are converted from the matlab files as found on Olivier Chapelle's web page
http://olivier.chapelle.cc/ssl-book/benchmarks.html

### Detailed description of the data ###

Each data set comes with a 10 or 12 different splits, and users can
choose the number of labeled points their training gets to see.

Labels are provided for all points (for benchmarking), but the
benchmarks suggest to use a fixed number of labels (10 or 100 for most
sets).

Full details about the benchmarks are provided in chapter 23 of the book
(online here: http://olivier.chapelle.cc/ssl-book/benchmarks.pdf)

### This code ###

* This code (c) by Oliver Obst <o.obst@westernsydney.edu.au>
  has been released under MIT License (see the LICENSE file).

* If you use these data sets in your research, you can cite the SSL book:

---
```
    @Book{ChaSchZie06,
      editor =	  {O. Chapelle and B. Sch{\"o}lkopf and A. Zien},
      title = 	  {Semi-Supervised Learning},
      publisher = {MIT Press},
      year = 	  2006,
      url =       {http://olivier.chapelle.cc/ssl-book/index.html},
      address =	  {Cambridge, MA}
    }
```