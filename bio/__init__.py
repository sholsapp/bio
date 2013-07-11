"""Some utilities for :mod:`bio`."""

import random


def random_gene(size=32, chars='GATC'):
  """Create a random gene."""
  return ''.join(random.choice(chars) for x in range(size))


class Cost(object):
  """A simple cost matrix."""
  match = 1
  mismatch = -1
  gap = -2
