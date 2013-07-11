#!/usr/bin/env python

from bio import AffineGapCost, FixedCost, random_gene
from bio.alignments import GlobalMatrix


def main():
  gene1 = random_gene()
  gene2 = random_gene()

  print gene1, gene2

  g = GlobalMatrix(gene1, gene2, FixedCost())
  for alignment in g.alignments:
    print alignment
    print alignment.make_cigar()
    print

if __name__ == '__main__':
  main()
