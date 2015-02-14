"""Alignment algorithms."""


class Moves(object):
  UP = 'U'
  DIAGONAL = 'D'
  LEFT = 'L'
  NONE = ''
  ORIGIN = '*'


class bcolors:
  HEADER = '\033[95m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'


class Alignment(object):
  """Encapsulates an alignment between two sequences."""

  def __init__(self, a, b, cost):
    self.a = a[::-1]
    self.b = b[::-1]
    self.cost = cost
    self.matches = 0
    self.mismatches = 0
    self.a_gaps = 0
    self.b_gaps = 0
    # Populate the analytics declared above
    self._analyze()

  def __repr__(self):
    return "Alignment(cost=%r, matches=%r, mismatches=%r, a_gaps=%r, b_gaps=%r)" % (self.cost, self.matches, self.mismatches, self.a_gaps, self.b_gaps)

  def _analyze(self):
    for i in range(0, len(self.a)):
      if self.a[i] == self.b[i]:
        self.matches += 1
      elif self.a[i] == '-':
        self.a_gaps += 1
      elif self.b[i] == '-':
        self.b_gaps += 1
      else:
        self.mismatches += 1

  def make_cigar(self):
    a_bar = ''
    b_bar = ''
    bar = ''
    for i in range(0, len(self.a)):
      color = ''
      if self.a[i] == self.b[i]:
        color = bcolors.GREEN
      elif ('-' not in [self.a[i], self.b[i]]) and self.a[i] != self.b[i]:
        color = bcolors.RED
      a_bar += '{color}{char}{end}'.format(color=color, char=self.a[i], end=bcolors.ENDC)
      bar += '|'.format(color=color, end=bcolors.ENDC) if self.a[i] == self.b[i] else ' '
      b_bar += '{color}{char}{end}'.format(color=color, char=self.b[i], end=bcolors.ENDC)
    return '\n'.join([a_bar, bar, b_bar])


class Element(object):
  def __init__(self, x, y, value=None, traceback=Moves.NONE):
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
    return "Element(%r, %r, %r, %r)" % (self.x, self.y, self.value, self.traceback)


class AlignmentMatrix(object):
  """A base alignment matrix.

    This class encapsulates common functionality between global and local
    alignment algorithms.

    :param a: The first input sequence.
    :param b: The second input sequence.
    :param cost: The class that provides costs... still under development.

  """
  def __init__(self, a, b, cost):
    self._matrix = []
    self.a = a
    self.b = b
    self.cost = cost
    for y in range(0, len(a) + 1):
      self._matrix.append([])
      for x in range(0, len(b) + 1):
        self._matrix[y].append(Element(x, y))
    self.alignments = []
    self._initialize()
    self._calculate_subsolutions()
    self._calculate_optimals()

  def _initialize(self):
    pass

  def _calculate_subsolutions(self):
    pass

  def _calculate_optimals(self):
    pass

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
    if not element.traceback or element.traceback == Moves.ORIGIN:
      yield Moves.NONE, Moves.NONE

  def _calculate_optimals_at_cord(self, cord):
    for a_alignment, b_alignment in self._trace(self.get(cord)):
      self.alignments.append(Alignment(a_alignment, b_alignment, self.get(cord).value))

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

  def _initialize(self):
    self.get((0, 0)).value = 0
    self.get((0, 0)).traceback = Moves.ORIGIN
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

  def _calculate_subsolutions(self):
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

  def _calculate_optimals(self):
    self._calculate_optimals_at_cord((len(self.b), len(self.a)))


class LocalMatrix(AlignmentMatrix):
  def __init__(self, a, b, cost):
    self.max_value = 0
    self.max_cord = (0, 0)
    AlignmentMatrix.__init__(self, a, b, cost)

  def _initialize(self):
    self.get((0, 0)).value = 0
    self.get((0, 0)).traceback = Moves.ORIGIN
    element = self.get((1, 0))
    while element is not None:
      element.value = 0
      element.traceback = Moves.NONE
      element = self.get(element.right)
    element = self.get((0, 1))
    while element is not None:
      element.value = 0
      element.traceback = Moves.NONE
      element = self.get(element.down)

  def _calculate_subsolutions(self):
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

  def _calculate_optimals(self):
    self._calculate_optimals_at_cord(self.max_cord)
