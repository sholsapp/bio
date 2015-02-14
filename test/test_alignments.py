from bio import FixedCost
from bio.alignments import GlobalMatrix, LocalMatrix


def test_global():
  gene1 = 'GGAATGG'
  gene2 = 'ATG'
  g = GlobalMatrix(gene1, gene2, FixedCost())
  assert g._matrix[7][3].value == -5


def test_local():
  gene1 = 'GGAATGG'
  gene2 = 'ATG'
  l = LocalMatrix(gene1, gene2, FixedCost())
  assert l._matrix[6][3].value == 3
