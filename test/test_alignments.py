from nose.tools import *

from bio import Cost
from bio.alignments import GlobalMatrix, LocalMatrix

def test_global():
  gene1 = 'GGAATGG'
  gene2 = 'ATG'
  g = GlobalMatrix(gene1, gene2, Cost)
  g.initialize()
  g.execute()
  assert_equal(g._matrix[7][3].value, -5)

def test_local():
  gene1 = 'GGAATGG'
  gene2 = 'ATG'
  l = LocalMatrix(gene1, gene2, Cost)
  l.initialize()
  l.execute()
  assert_equal(l._matrix[6][3].value, 3)
