# CS 61A Fall 2014
# Name:Johnathan Chow
# Login:AKH

def g(n):
    """Return the value of G(n), computed recursively.

    >>> g(1)
    1
    >>> g(2)
    2
    >>> g(3)
    3
    >>> g(4)
    10
    >>> g(5)
    22
    """
    a = 0
    if n <= 3:
        return n
    if n > 3:
        return g(n-1) + (2*g(n-2)) + (3*g(n-3))


def g_iter(n):
    """Return the value of G(n), computed iteratively.

    >>> g_iter(1)
    1
    >>> g_iter(2)
    2
    >>> g_iter(3)
    3
    >>> g_iter(4)
    10
    >>> g_iter(5)
    22
    """

    def gprime2(n):
        n1 = n
        totes = 0
        if n <= 3:
            return n
        else:
            while (n1-1) > 3:
                if (n1-1) > 3:
                    totes = totes + 1*(n1-1)
                if (n1-2) > 3:
                    totes = totes + 2*(n1-2)
                if (n1-3) > 3:
                    totes = totes + 3*(n1-3)
                n1 = n1 - 1
            if (n1-1) <= 3:
                    totes = totes + (n1 - 1) 
            n1 = n
            while (n1-2) > 3:
                if (n1-1) > 3:
                    totes = totes + 1*(n1-1)
                if (n1-2) > 3:
                    totes = totes + 2*(n1-2)
                if (n1-3) > 3:
                    totes = totes + 3*(n1-3)
                n1 = n1 - 2
            if (n1-2) <= 3:
                    totes = totes + 2*(n1 - 2)
            n1 = n
            while (n1 - 3) > 3:
                if (n1-1) > 3:
                    totes = totes + 1*(n1-1)
                if (n1-2) > 3:
                    totes = totes + 2*(n1-2)
                if (n1-3) > 3:
                    totes = totes + 3*(n1-3)
                n1 = n1 - 3 
            n1 = n
            if (n1-3) <= 3:
                    totes = totes + 3*(n1 - 3)    
            return totes
    return gprime2(n)


def has_seven(k):
    """Returns True if at least one of the digits of k is a 7, False otherwise.

    >>> has_seven(3)
    False
    >>> has_seven(7)
    True
    >>> has_seven(2734)
    True
    >>> has_seven(2634)
    False
    >>> has_seven(734)
    True
    >>> has_seven(7777)
    True
    """
    
    
    if k == 7:
        return True
    while k // 10 > 0:
        if k%10 == 7:
            return True
        return has_seven(k//10)
    if k != 7:
        return False
    

def pingpong(n):
    """Return the nth element of the ping-pong sequence.

    >>> pingpong(7)
    7
    >>> pingpong(8)
    6
    >>> pingpong(15)
    1
    >>> pingpong(21)
    -1
    >>> pingpong(22)
    0
    >>> pingpong(30)
    6
    >>> pingpong(68)
    2
    >>> pingpong(69)
    1
    >>> pingpong(70)
    0
    >>> pingpong(71)
    1
    >>> pingpong(72)
    0
    >>> pingpong(100)
    2
    """

    if n == 1:
        return 1
    def switch(n):
        if n%7==0 or has_seven(n):
            return -1
        else:
            return 1
    def plusorminus(n):
        if n == 1:
            return 1
        return plusorminus(n-1) * switch(n-1)

    return pingpong(n-1) + plusorminus(n)

def count_change(amount):
    """Return the number of ways to make change for amount.

    >>> count_change(7)
    6
    >>> count_change(10)
    14
    >>> count_change(20)
    60
    >>> count_change(100)
    9828
    """
    coin = 1
    while coin*2<amount:
        coin = coin*2

    def helper(amount,coin):
        if amount == coin:
            return 1 + helper(amount,coin//2)
        if amount<0:
            return 0
        if coin==0:
            return 0
        else:
            withcoin=helper(amount-coin, coin)
            withoutcoin=helper(amount, coin//2)
            return withcoin+withoutcoin
    return helper(amount,coin)

def towers_of_hanoi(n, start, end):
    """Print the moves required to solve the towers of hanoi game, starting
    with n disks on the start pole and finishing on the end pole.

    The game is to assumed to have 3 poles.

    >>> towers_of_hanoi(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> towers_of_hanoi(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> towers_of_hanoi(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    assert 0 < start <= 3 and 0 < end <= 3 and start != end, "Bad start/end"
    if n:
        towers_of_hanoi(n - 1, start, 6-start-end)
        print ('Move the top disk from rod ' + str(start) + ' to rod '  + str(end))
        towers_of_hanoi(n-1, 6-start-end, end)
 

# from operator import sub, mul

# def make_anonymous_factorial():
#     """Return the value of an expression that computes factorial.

#     >>> make_anonymous_factorial()(5)
#     120
#     """
#     return YOUR_EXPRESSION_HERE

