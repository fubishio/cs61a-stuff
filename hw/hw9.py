# CS 61A Fall 2014
# Name: Johnathan Chow
# Login: AKH

# A dictionary from pairs of matching brackets to the operators they indicate.
brackets = {('[', ']'): '+',
            ('(', ')'): '-',
            ('<', '>'): '*',
            ('{', '}'): '/'}

# A dictionary with left-bracket keys and corresponding right-bracket values.
left_to_right = {left: right for left, right in brackets}

# The set of all left and right brackets.
all_brackets = set(left_to_right.keys()).union(set(left_to_right.values()))

def tokenize(line):
    """Convert a string into a list of tokens.

    >>> tokenize('2.3')
    [2.3]
    >>> tokenize('(2 3)')
    ['(', 2, 3, ')']
    >>> tokenize('<2 3)')
    ['<', 2, 3, ')']
    >>> tokenize('<[2{12.5 6.0}](3 -4 5)>')
    ['<', '[', 2, '{', 12.5, 6.0, '}', ']', '(', 3, -4, 5, ')', '>']

    >>> tokenize('2.3.4')
    Traceback (most recent call last):
        ...
    ValueError: invalid token 2.3.4

    >>> tokenize('?')
    Traceback (most recent call last):
        ...
    ValueError: invalid token ?

    >>> tokenize('hello')
    Traceback (most recent call last):
        ...
    ValueError: invalid token hello

    >>> tokenize('<(GO BEARS)>')
    Traceback (most recent call last):
        ...
    ValueError: invalid token GO
    """
    # Surround all brackets by spaces so that they are separated by split.
    for b in all_brackets:
        line = line.replace(b, ' ' + b + ' ')

    # Convert numerals to numbers and raise ValueErrors for invalid tokens.
    tokens = []
    for t in line.split():
        if coerce_to_number(t) == None:
            if t == '<' or t == '>' or t == '[' or t == ']' or t == '(' or t == ')' or t == '{' or t == '}':
                tokens.append(t)
            else:
                raise ValueError('invalid token {0}'.format(t))
        else:
            tokens.append(coerce_to_number(t))
    return tokens

def coerce_to_number(token):
    """Coerce a string to a number or return None.

    >>> coerce_to_number('-2.3')
    -2.3
    >>> print(coerce_to_number('('))
    None
    """
    try:
        return int(token)
    except (TypeError, ValueError):
        try:
            return float(token)
        except (TypeError, ValueError):
            return None

# def brack_read(tokens):
#     """Return an expression tree for the first well-formed Brackulator
#     expression in tokens. Tokens in that expression are removed from tokens as
#     a side effect.

#     >>> brack_read(tokenize('100'))
#     100
#     >>> brack_read(tokenize('([])'))
#     Pair('-', Pair(Pair('+', nil), nil))
#     >>> print(brack_read(tokenize('<[2{12 6}](3 4 5)>')))
#     (* (+ 2 (/ 12 6)) (- 3 4 5))
#     >>> brack_read(tokenize('(1)(1)')) # More than one expression is ok
#     Pair('-', Pair(1, nil))
#     >>> brack_read(tokenize('[])')) # Junk after a valid expression is ok
#     Pair('+', nil)

#     >>> brack_read(tokenize('([]')) # Missing right bracket
#     Traceback (most recent call last):
#         ...
#     SyntaxError: unexpected end of line

#     >>> brack_read(tokenize('[)]')) # Extra right bracket
#     Traceback (most recent call last):
#         ...
#     SyntaxError: unexpected )

#     >>> brack_read(tokenize('([)]')) # Improper nesting
#     Traceback (most recent call last):
#         ...
#     SyntaxError: unexpected )

#     >>> brack_read(tokenize('')) # No expression
#     Traceback (most recent call last):
#         ...
#     SyntaxError: unexpected end of line
#     """
#     if not tokens:
#         raise SyntaxError('unexpected end of line')
#     token = tokens.pop(0)
#     n = coerce_to_number(token)
#     if n != None:
#         return n
#     elif token in left_to_right:
#         t = (token,left_to_right[token])
#         operator = brackets[t]
#         return Pair(operator,helperread(tokens,left_to_right[token]))
#     else:
#         raise SyntaxError('unexpected {0}'.format(token))


# def helperread(tokens,bracket):
#     if not tokens:
#         raise SyntaxError('unexpected end of line')
#     token = tokens[0]
#     n = coerce_to_number(token)
#     if token == bracket:
#         tokens.pop(0)
#         return nil
#     elif n != None:
#         tokens.pop(0)
#         return Pair(n,read_tail(tokens,bracket))
#     else:
#         return Pair(brack_read(tokens),read_tail(tokens,bracket))
###################################
# Support classes for Brackulator #
###################################

class Pair:
    """A pair has two instance attributes: first and second.  For a Pair to be
    a well-formed list, second is either a well-formed list or nil.  Some
    methods only apply to well-formed lists.

    >>> s = Pair(1, Pair(2, nil))
    >>> s
    Pair(1, Pair(2, nil))
    >>> print(s)
    (1 2)
    >>> len(s)
    2
    >>> s[1]
    2
    >>> print(s.map(lambda x: x+4))
    (5 6)
    """
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return "Pair({0}, {1})".format(repr(self.first), repr(self.second))

    def __str__(self):
        s = "(" + str(self.first)
        second = self.second
        while isinstance(second, Pair):
            s += " " + str(second.first)
            second = second.second
        if second is not nil:
            s += " . " + str(second)
        return s + ")"

    def __len__(self):
        n, second = 1, self.second
        while isinstance(second, Pair):
            n += 1
            second = second.second
        if second is not nil:
            raise TypeError("length attempted on improper list")
        return n

    def __getitem__(self, k):
        if k < 0:
            raise IndexError("negative index into list")
        y = self
        for _ in range(k):
            if y.second is nil:
                raise IndexError("list index out of bounds")
            elif not isinstance(y.second, Pair):
                raise TypeError("ill-formed list")
            y = y.second
        return y.first

    def map(self, fn):
        """Return a Scheme list after mapping Python function FN to SELF."""
        mapped = fn(self.first)
        if self.second is nil or isinstance(self.second, Pair):
            return Pair(mapped, self.second.map(fn))
        else:
            raise TypeError("ill-formed list")

class nil(object):
    """The empty list"""

    def __repr__(self):
        return "nil"

    def __str__(self):
        return "()"

    def __len__(self):
        return 0

    def __getitem__(self, k):
        if k < 0:
            raise IndexError("negative index into list")
        raise IndexError("list index out of bounds")

    def map(self, fn):
        return self

nil = nil() # Assignment hides the nil class; there is only one instance

def read_eval_print_loop():
    """Run a read-eval-print loop for the Brackulator language."""
    global Pair, nil
    from scheme_reader import Pair, nil
    from scalc import calc_eval

    while True:
        try:
            src = tokenize(input('brack> '))
            while len(src) > 0:
              expression = brack_read(src)
              print(calc_eval(expression))
        except (SyntaxError, ValueError, TypeError, ZeroDivisionError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):  # <Control>-D, etc.
            return




class Mobile:
    """A simple binary mobile that has branches of weights or other mobiles.

    >>> Mobile(1, 2)
    Traceback (most recent call last):
        ...
    TypeError: 1 is not a Branch
    >>> m = Mobile(Branch(1, Weight(2)), Branch(2, Weight(1)))
    >>> m.weight
    3
    >>> m.is_balanced()
    True
    >>> m.left.contents = Mobile(Branch(1, Weight(1)), Branch(2, Weight(1)))
    >>> m.weight
    3
    >>> m.left.contents.is_balanced()
    False
    >>> m.is_balanced() # All submobiles must be balanced for m to be balanced
    False
    >>> m.left.contents.right.contents.weight = 0.5
    >>> m.left.contents.is_balanced()
    True
    >>> m.is_balanced()
    False
    >>> m.right.length = 1.5
    >>> m.is_balanced()
    True
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right
        if type(self.left) != Branch:
            raise TypeError(str(self.left) + " is not a Branch")
        if type(self.right) != Branch:
            raise TypeError(str(self.right) + " is not a Branch")
    @property
    def weight(self):
        """The total weight of the mobile."""
        return self.left.contents.weight + self.right.contents.weight

    def is_balanced(self):
        """True if and only if the mobile is balanced."""
        if self.left.torque == self.right.torque and self.left.contents.is_balanced() and self.right.contents.is_balanced():
            return True
        else:
            return False

def check_positive(x):
    """Check that x is a positive number, and raise an exception otherwise.

    >>> check_positive(2)
    >>> check_positive('hello')
    Traceback (most recent call last):
    ...
    TypeError: hello is not a number
    >>> check_positive('1')
    Traceback (most recent call last):
    ...
    TypeError: 1 is not a number
    >>> check_positive(-2)
    Traceback (most recent call last):
    ...
    ValueError: -2 <= 0
    """
    if type(x) == int or type(x) == float:
        if x > 0:
            return None
        raise ValueError(str(x) + " <= 0")
    else:
        raise TypeError(x + " is not a number")


class Branch:
    """A branch of a simple binary mobile."""

    def __init__(self, length, contents):
        if type(contents) not in (Weight, Mobile):
            raise TypeError(str(contents) + ' is not a Weight or Mobile')
        check_positive(length)
        self.length = length
        self.contents = contents

    @property
    def torque(self):
        """The torque on the branch"""
        return self.length * self.contents.weight


class Weight:
    """A weight."""
    def __init__(self, weight):
        check_positive(weight)
        self.weight = weight

    def is_balanced(self):
        return True

def interpret_mobile(s):
    """Return a Mobile described by string s by substituting one of the classes
    Branch, Weight, or Mobile for each occurrenct of the letter T.

    >>> simple = 'Mobile(T(2,T(1)), T(1,T(2)))'
    >>> interpret_mobile(simple).weight
    3
    >>> interpret_mobile(simple).is_balanced()
    True
    >>> s = 'T(T(4,T(T(4,T(1)),T(1,T(4)))),T(2,T(10)))'
    >>> m = interpret_mobile(s)
    >>> m.weight
    15
    >>> m.is_balanced()
    True
    """
    next_T = s.find('T')        # The index of the first 'T' in s.
    if next_T == -1:            # The string 'T' was not found in s
        try:
            return eval(s)      # Interpret s
        except TypeError as e:
            return None         # Return None if s is not a valid mobile
    for t in ('Branch', 'Weight', 'Mobile'):
        a = s.replace('T',t,1)
        b = interpret_mobile(a)
        if a:
            return a
    return None


class Stream:
    """A lazily computed recursive list."""

    class empty:
        def __repr__(self):
            return 'Stream.empty'
    empty = empty()

    def __init__(self, first, compute_rest=lambda: Stream.empty):
        assert callable(compute_rest), 'compute_rest must be callable.'
        self.first = first
        self._compute_rest = compute_rest

    @property
    def rest(self):
        """Return the rest of the stream, computing it if necessary."""
        if self._compute_rest is not None:
            self._rest = self._compute_rest()
            self._compute_rest = None
        return self._rest

    def __repr__(self):
        return 'Stream({0}, <...>)'.format(repr(self.first))

    def __iter__(self):
        """Return an iterator over the elements in the stream.

        >>> it = iter(ints)
        >>> [next(it) for _ in range(6)]
        [1, 2, 3, 4, 5, 6]
        """
        yield self.first
        a = self.rest
        while a != None:
            yield a.first
            a = a.rest

    def __getitem__(self, k):
        """Return the k-th element of the stream.

        >>> ints[5]
        6
        >>> increment_stream(ints)[7]
        9
        """
        a = self.rest
        c = 1
        while a != None:
            if c == k:
                return a.first
            c += 1
            a = a.rest


def increment_stream(s):
    """Increment all elements of a stream."""
    return Stream(s.first+1, lambda: increment_stream(s.rest))

# The stream of consecutive integers starting at 1.
ints = Stream(1, lambda: increment_stream(ints))

def scale_stream(s, k):
    """Return a stream of the elements of S scaled by a number K.

    >>> s = scale_stream(ints, 5)
    >>> s.first
    5
    >>> s.rest
    Stream(10, <...>)
    >>> scale_stream(s.rest, 10)[2]
    200
    """
    return Stream(s.first*k, lambda: scale_stream(s.rest, k))

def merge(s0, s1):
    """Return a stream over the elements of strictly increasing s0 and s1,
    removing repeats. Assume that s0 and s1 have no repeats.

    >>> twos = scale_stream(ints, 2)
    >>> threes = scale_stream(ints, 3)
    >>> m = merge(twos, threes)
    >>> [m[i] for i in range(10)]
    [2, 3, 4, 6, 8, 9, 10, 12, 14, 15]
    """
    if s0 is Stream.empty:
        return s1
    elif s1 is Stream.empty:
        return s0

    e0, e1 = s0.first, s1.first
    'please review'
    if e0 > e1:
        return Stream(e1, lambda: merge(s0, s1.rest))
    if e0 < e1:
        return Stream(e0, lambda: merge(s0.rest, s1))
    if e0 == e1:
        return Stream(e0, lambda: merge(s0.rest, s1.rest))

def make_s():
    """Return a stream over all positive integers with only factors 2, 3, & 5.

    >>> s = make_s()
    >>> [s[i] for i in range(20)]
    [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, 32, 36]
    """
    def rest():
        a = scale_stream(s,2)
        b = merge(scale_stream(s,3),scale_stream(s,5))
        return merge(a, b)
    s = Stream(1, rest)
    return s

def filter(fn,s):
    if s is Stream.empty:
        return s
    def rest():
        return filter(fn,s.rest)

    if fn(s.first):
        return Stream(s.first,rest)
    else:
        return filter(fn,s.rest)
def unique(s):
    """Return a stream of the unique elements in s in the order that they
    first appear.

    >>> s = unique(to_stream([1, 2, 2, 1, 0, 4, 2, 3, 1, 9, 0]))
    >>> [s[i] for i in range(6)]
    [1, 2, 0, 4, 3, 9]
    """
    if s is Stream.empty:
        return s
    def helper(x):
        return lambda k: k != x
    def rest():
        return unique(filter(helper(s.first), s.rest))
    return Stream(s.first, rest)

def to_stream(lst):
    if not lst:
        return Stream.empty
    return Stream(lst[0], lambda: to_stream(lst[1:]))

def rle(s, max_run_length=10):
    """
    >>> example_stream = to_stream([1, 1, 1, 2, 3, 3])
    >>> encoded_example = rle(example_stream)
    >>> [encoded_example[i] for i in range(3)]
    [(3, 1), (1, 2), (2, 3)]
    >>> shorter_encoded_example = rle(example_stream, 2)
    >>> [shorter_encoded_example[i] for i in range(4)]
    [(2, 1), (1, 1), (1, 2), (2, 3)]
    >>> encoded_naturals = rle(ints)
    >>> [encoded_naturals[i] for i in range(3)]
    [(1, 1), (1, 2), (1, 3)]
    """
    "*** YOUR CODE HERE ***"

# from urllib.request import urlopen

# def puzzle_4():
#     """Return the soluton to puzzle 4."""
#     "*** YOUR CODE HERE ***"



