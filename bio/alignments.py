"""Alignment algorithms."""


class Moves(object):
  UP = 'U'
  DIAGONAL = 'D'
  LEFT = 'L'


class Element(object):
  def __init__(self, x, y, value=None, traceback=''):
    self.x = x
    self.y = y
    self.value = value
    self.traceback = traceback
    self.up = self.x, self.y - 1
    self.down = self.x, self.y + 1
    self.left = self.x - 1, self.y
    self.right = self.x + 1, self.y
    self.diag = self.x - 1, self.y - 1
  def __repr__(self):
    #return "Element(%r, %r, %r, %r)" % (self.x, self.y, self.value, self.traceback)
    return "(%r %r)" % (self.value, self.traceback)


class AlignmentMatrix(object):
  def __init__(self, a, b, cost):
    self._matrix = []
    self.a = a
    self.b = b
    self.cost = cost
    for y in range(0, len(a) + 1):
      self._matrix.append([])
      for x in range(0, len(b) + 1):
        self._matrix[y].append(Element(x, y))

  def execute(self):
    for y in range(1, len(self.a) + 1):
      for x in range(1, len(self.b) + 1):
        element = self.get((x, y))
        diag_cost = self.get(element.diag).value + (
          self.cost.match if self.a[y - 1] == self.b[x - 1] else self.cost.mismatch
        )
        left_cost = self.get(element.left).value + self.cost.gap
        up_cost = self.get(element.up).value + self.cost.gap
        choices = [diag_cost, left_cost, up_cost]
        if diag_cost == max(choices):
          self.get((x, y)).traceback += Moves.DIAGONAL
        if left_cost == max(choices):
          self.get((x, y)).traceback += Moves.LEFT
        if up_cost == max(choices):
          self.get((x, y)).traceback += Moves.UP
        element.value = max(choices)

  def _trace(self, element):
    for move in element.traceback:
      if move == Moves.DIAGONAL:
        align_a = self.a[element.y - 1]
        align_b = self.b[element.x - 1]
        for others_a, others_b in self._trace(self.get(element.diag)):
          yield (align_a + others_a, align_b + others_b)
      elif move == Moves.LEFT:
        align_a = '-'
        align_b = self.b[element.x - 1]
        for others_a, others_b in self._trace(self.get(element.left)):
          yield (align_a + others_a, align_b + others_b)
      elif move == Moves.UP:
        align_a = self.a[element.y - 1]
        align_b = '-'
        for others_a, others_b in self._trace(self.get(element.up)):
          yield (align_a + others_a, align_b + others_b)
    if not element.traceback or element.traceback == '*':
      yield '', ''

  def make_cigar(self, this_a, this_b):
    bar = ''
    for i in range(0, len(this_a)):
      bar += '|' if this_a[i] == this_b[i] else ' '
    return '\n'.join([this_a, bar, this_b])

  def print_traces(self):
    idx = 1
    for aa, bb in self._trace(self.get((len(self.b), len(self.a)))):
      print 'Match %s (cost of %s):' % (idx, self._matrix[len(self.a)][len(self.b)].value)
      print self.make_cigar(aa[::-1], bb[::-1])
      print
      idx += 1

  def get(self, cord):
    """Get an element at an (x, y) cordinate.

      :param cord: An (x, y) cordinate as a integer tuple.

    """
    x, y = cord
    try:
      return self._matrix[y][x]
    except IndexError:
      return None

class GlobalMatrix(AlignmentMatrix):

  def initialize(self):
    self.get((0, 0)).value = 0
    self.get((0, 0)).traceback = '*'
    element = self.get((1, 0))
    while element is not None:
      element.value = self.cost.gap * element.x
      element.traceback = Moves.LEFT
      element = self.get(element.right)
    element = self.get((0, 1))
    while element is not None:
      element.value = self.cost.gap * element.y
      element.traceback = Moves.UP
      element = self.get(element.down)

  def execute(self):
    for y in range(1, len(self.a) + 1):
      for x in range(1, len(self.b) + 1):
        element = self.get((x, y))
        diag_cost = self.get(element.diag).value + (
          self.cost.match if self.a[y - 1] == self.b[x - 1] else self.cost.mismatch
        )
        left_cost = self.get(element.left).value + self.cost.gap
        up_cost = self.get(element.up).value + self.cost.gap
        choices = [diag_cost, left_cost, up_cost]
        if diag_cost == max(choices):
          self.get((x, y)).traceback += Moves.DIAGONAL
        if left_cost == max(choices):
          self.get((x, y)).traceback += Moves.LEFT
        if up_cost == max(choices):
          self.get((x, y)).traceback += Moves.UP
        element.value = max(choices)

  def print_traces(self):
    idx = 1
    for aa, bb in self._trace(self.get((len(self.b), len(self.a)))):
      print 'Match %s (cost of %s):' % (idx, self._matrix[len(self.a)][len(self.b)].value)
      print self.make_cigar(aa[::-1], bb[::-1])
      print
      idx += 1


class LocalMatrix(AlignmentMatrix):
  def __init__(self, a, b, cost):
    AlignmentMatrix.__init__(self, a, b, cost)
    self.max_value = 0
    self.max_cord = (0, 0)

  def initialize(self):
    self.get((0, 0)).value = 0
    self.get((0, 0)).traceback = '*'
    element = self.get((1, 0))
    while element is not None:
      element.value = 0
      element.traceback = ''
      element = self.get(element.right)
    element = self.get((0, 1))
    while element is not None:
      element.value = 0
      element.traceback = ''
      element = self.get(element.down)

  def execute(self):
    for y in range(1, len(self.a) + 1):
      for x in range(1, len(self.b) + 1):
        element = self.get((x, y))
        diag_cost = self.get(element.diag).value + (
          self.cost.match if self.a[y - 1] == self.b[x - 1] else self.cost.mismatch
        )
        left_cost = self.get(element.left).value + self.cost.gap
        up_cost = self.get(element.up).value + self.cost.gap
        choices = [0, diag_cost, left_cost, up_cost]
        if diag_cost == max(choices):
          self.get((x, y)).traceback += Moves.DIAGONAL
        if left_cost == max(choices):
          self.get((x, y)).traceback += Moves.LEFT
        if up_cost == max(choices):
          self.get((x, y)).traceback += Moves.UP
        element.value = max(choices)
        if element.value >= self.max_value:
          self.max_value = element.value
          self.max_cord = (x, y)

  def print_traces(self):
    idx = 1
    for aa, bb in self._trace(self.get(self.max_cord)):
      print 'Match %s (cost of %s):' % (idx, self._matrix[self.max_cord[1]][self.max_cord[0]].value)
      print self.make_cigar(aa[::-1], bb[::-1])
      print
      idx += 1
