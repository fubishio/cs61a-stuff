## Rooted Trees, Linked Lists, Dictionaries ##

################
# Rooted Trees #
################

# Tree definition
def rooted(value, branches):
    for branch in branches:
        assert is_rooted(branch), 'branches must be rooted trees'
    return [value] + list(branches)

def root(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def leaf(value):
    return rooted(value, [])

def is_rooted_leaf(tree):
    return branches(tree) == []

def is_rooted(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_rooted(branch):
            return False
    return True

t = rooted(1, [leaf(2), rooted(3, [leaf(4), leaf(5)]), rooted(6, [leaf(7)])])

def print_tree(t, indent=0):
    """Return a string representation of this tree in which
    each node is indented by two spaces times its depth from
    the root.

    >>> print_tree(t)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(root(t)))
    for child in branches(t):
        print_tree(child, indent + 1)

# # Q1 (optional)
# def countdown_tree():
#     """Return a tree that has the following structure. 

#     >>> print_tree(countdown_tree())
#     10
#       9
#         8
#       7
#         6
#           5
#     """
#     "*** YOUR CODE HERE ***"

# Q2
def size_of_tree(t):
    """Return the number of entries in the tree.

    >>> print_tree(t)
    1
      2
      3
        4
        5
      6
        7
    >>> size_of_tree(t)
    7
    """
    
    
    total = 0
    if is_rooted_leaf(t):
        return 1
    for node in branches(t):
        total += size_of_tree(node)
    return total + 1

################
# Linked Lists #
################

# Linked List definition
empty = 'empty'

def is_link(s):
    """s is a linked list if it is empty or a (first, rest) pair."""
    return s == empty or (type(s) == list and len(s) == 2 and is_link(s[1]))

def link(first, rest):
    """Construct a linked list from its first element and the rest."""
    assert is_link(rest), 'rest must be a linked list.'
    return [first, rest]

def first(s):
    """Return the first element of a linked list s."""
    assert is_link(s), 'first only applies to linked lists.'
    assert s != empty, 'empty linked list has no first element.'
    return s[0]

def rest(s):
    """Return the rest of the elements of a linked list s."""
    assert is_link(s), 'rest only applies to linked lists.'
    assert s != empty, 'empty linked list has no rest.'
    return s[1]


# Q3
def sum_linked_list(lst, fn):
    """ Applies a function FN to each number in LST and returns the sum
    of the resulting values

    >>> square = lambda x: x*x
    >>> double = lambda y: 2*y
    >>> lst1 = link(1, link(2, link(3, link(4, empty))))    
    >>> sum_linked_list(lst1, square)
    30
    >>> lst2 = link(3, link(5, link(4, link(10, empty))))
    >>> sum_linked_list(lst2, double)
    44
    """
    total = 0
    if rest(lst) == empty:
        total += fn(first(lst))
        return total
    else:
        total += sum_linked_list(rest(lst), fn)
        return total + fn(first(lst))

    


################
# Dictionaries #
################

# Q4
def counter(message):
    """ Returns a dictionary of each word in message mapped 
    to the number of times it appears in the input string.
    >>> x = counter('to be or not to be')
    >>> x['to']
    2
    >>> x['be']
    2
    >>> x['not']
    1
    >>> y = counter('run forrest run')
    >>> y['run']
    2
    >>> y['forrest']
    1
    """
    word_list = message.split()
    freq = {}
    for word in word_list:
        if word not in freq:
            freq[word] = 1
        else:
            freq[word] += 1
    return freq
