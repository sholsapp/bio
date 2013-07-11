#!/usr/bin/env python

from bio import AffineGapCost, FixedCost, random_gene
from bio.alignments import LocalMatrix


def main():
  gene1 = random_gene()
  gene2 = random_gene()

  print gene1, gene2

  l = LocalMatrix(gene1, gene2, FixedCost())
  for alignment in l.alignments:
    print alignment
    print alignment.make_cigar()
    print

if __name__ == '__main__':
  main()
