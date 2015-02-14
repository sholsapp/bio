#!/usr/bin/env python

import argparse

from bio import AffineGapCost, FixedCost, random_gene
from bio.alignments import GlobalMatrix


def main():

  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--gene1', required=False, default=random_gene())
  parser.add_argument('--gene2', required=False, default=random_gene())
  args = parser.parse_args()

  gene1 = args.gene1
  gene2 = args.gene2

  print gene1, gene2

  g = GlobalMatrix(gene1, gene2, FixedCost())
  for alignment in g.alignments:
    print alignment
    print alignment.make_cigar()
    print

if __name__ == '__main__':
  main()
