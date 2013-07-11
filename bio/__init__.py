"""Some utilities for :mod:`bio`."""

import random


def random_gene(size=32, chars='GATC'):
  """Create a random gene."""
  return ''.join(random.choice(chars) for x in range(size))


class FixedCost(object):
  """A fixed cost matrix."""
  match = 1
  mismatch = -1
  gap = -2


class AffineGapCost(object):
  """An affine gap cost matrix.

    Affine gap cost matrices have an increased penalty for starting a gap, but
    a lesser cost for extending a gap.

  """
  def __init__(self):
    self.in_gap = False
  @property
  def match(self):
    self.in_gap = False
    return 1
  @property
  def mismatch(self):
    self.in_gap = False
    return -1
  @property
  def gap(self):
    if self.in_gap:
      return -1
    self.in_gap = True
    return -4
