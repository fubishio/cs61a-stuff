# CS 61A Fall 2014
# Name:
# Login:


def two_equal(a, b, c):
    """Return whether exactly two of the arguments are equal and the
    third is not.

    >>> two_equal(1, 2, 3)
    False
    >>> two_equal(1, 2, 1)
    True
    >>> two_equal(1, 1, 1)
    False
    >>> result = two_equal(5, -1, -1) # return, don't print
    >>> result
    True

    """
    if a == b == c:
        return False
    elif a == b and b != c:
        return True
    elif a == c and a != b:
        return True
    elif c == b and a != b:
        return True
    else:
        return False



def same_hailstone(a, b):
    """Return whether a and b are both members of the same hailstone
    sequence.

    >>> same_hailstone(10, 16) # 10, 5, 16, 8, 4, 2, 1
    True
    >>> same_hailstone(16, 10) # order doesn't matter
    True
    >>> result = same_hailstone(3, 19) # return, don't print
    >>> result
    False

    """
    x = a
    y = b

    def hailstone(n):
        while n != 1:
            if n == 1:
                return False   
            elif n == y:
                return n == y
            elif n % 2 == 1:
                n = n * 3 + 1
            else:
                n = n // 2
                     

    def hailstone1(n):
        while n != 1:
            if n == 1:
                return False    
            elif n == x:
                return n == x
            elif n % 2 == 1:
                n = n * 3 + 1
            else:
                n = n // 2
            
    if hailstone(a) == True:
        return True
    elif hailstone1(b) == True:
        return True
    else:
        return False
    


    




    






def near_golden(perimeter):
    """Return the integer height of a near-golden rectangle with PERIMETER.

    >>> near_golden(42) # 8 x 13 rectangle has perimeter 42
    8
    >>> near_golden(68) # 13 x 21 rectangle has perimeter 68
    13
    >>> result = near_golden(100) # return, don't print
    >>> result
    19

    """
    perimeter = perimeter / 2
  
    height = 1
    width = perimeter - 1
    c = 100000000
    k = 100000000
    if perimeter * 2 == 4:
        return 1

    else:
        while height != width:
        
            height = height + 1
            width = width - 1
            c = k
            k = abs((height/width) - ((width/height) - 1))
            if k > c:
                return height - 1
                