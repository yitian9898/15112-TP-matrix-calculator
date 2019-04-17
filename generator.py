######
# this script containing matrix generators is solely developed and written by Tianyi Zhu
######
import random
from matrixOperations import*
from sympy import*
#####################################################################################################
# from 15-112 course notes
def callWithLargeStack(f,*args):
    import sys
    import threading
    threading.stack_size(2**27)  # 64MB stack
    sys.setrecursionlimit(2**27) # will hit 64MB stack limit first
    # need new thread to get the redefined stack size
    def wrappedFn(resultWrapper): resultWrapper[0] = f(*args)
    resultWrapper = [None]
    #thread = threading.Thread(target=f, args=args)
    thread = threading.Thread(target=wrappedFn, args=[resultWrapper])
    thread.start()
    thread.join()
    return resultWrapper[0]
#####################################################################################################
# this function takes in an integer as the dimension of a square matrix. It returns a matrix with randomized entries from 0-9 (inclusive)
def squareMatrixGenerator(dim, a=0, b=9):
    new = [ [0] * dim for i in range(dim)]
    for i in range(dim):
        for j in range(dim):
            new[i][j] = random.randint(a, b)
    return new
# this function takes in two integers, row number and column number, as the dimension of a matrix. It returns a matrix with randomized entries from 0-9 (inclusive)
def randomMatrixGenerator(row, col, a=0, b=9):
    new = [ [0] * col for i in range(row)]
    for i in range(row):
        for j in range(col):
            new[i][j] = random.randint(a, b)
    return new
# this function takes in a 2D list as the input. It returns True if all entries of the 2D list are one-digit integers, else returns False
def isLegalResult(m):
    rows = len(m)
    cols = len(m[0])
    for i in range(rows):
        for j in range(cols):
            if (not isinstance(m[i][j], int)) or (len(str(m[i][j])) != 1) or (m[i][j] < 0):
                return False
    return True
# helper function for generating matrices for addition and subtraction
def addSubGenerator(row, col):
    m = []
    m1 = randomMatrixGenerator(row, col)
    m.append(m1)
    m2 = randomMatrixGenerator(row, col)
    m.append(m2)
    return m
# use this recursive function to generate addition matrices
def addGen(row, col):
    m = addSubGenerator(row, col)
    if isLegalResult(addition(m[0],m[1])):
        return m
    else:
        return addGen(row, col)
# use this recursive function to generate subtraction matrices
def subGen(row, col):
    m = addSubGenerator(row, col)
    if isLegalResult(subtraction(m[0],m[1])):
        return m
    else:
        return subGen(row, col)
# this function takes in three integers and generates a list of 2 matrices for the purpose of matrix multiplication problems
def multiGenerator(out1, inner, out2):
    m = []
    m1 = randomMatrixGenerator(out1, inner, 0, 3)
    m.append(m1)
    m2 = randomMatrixGenerator(inner, out2, 0, 3)
    m.append(m2)
    return m
# this recursive funtion generates multiplication matrices
def multiGen(out1, inner, out2):
    m = multiGenerator(out1, inner, out2)
    if isLegalResult(multiplication(m[0],m[1])):
        return m
    else:
        return multiGen(out1, inner, out2)
# this works
def rrefGen(row, col):
    m = randomMatrixGenerator(row, col)
    if isLegalResult(rrefSym(m)):
        return formatted(np.array(m).astype(np.float64).tolist())
    else:
        return rrefGen(row, col)
# use this recursive function to generate multiplication matrices
# this function uses recursion to generate linearly independent vectors for gram schmidt problems
def gramSchmidtGenerator(row, col):
    m = noZeroRowMatrixGenerator(row, col)
    if linearDep(m) == "linearly independent":
        return m
    else:
        return gramSchmidtGenerator(row, col)
def noZeroRow(x):
    for i in range(len(x)):
        for j in range(len(x[0])):
            if x[i].count(0) == len(x[0]):
                return False
    return True

def noZeroRowMatrixGenerator(row, col, a=0, b=9):
    m = randomMatrixGenerator(row, col)
    if noZeroRow(m):
        return m
    else: return noZeroRowMatrixGenerator(row, col)
# this function uses recursion to generate invertible matrices with integer entries for matrix inverse problems
def inverseGenerator(dim):
    m = squareMatrixGenerator(dim)
    if determinant(m) == 1 or determinant(m) == -1:
        return m
    else:
        return inverseGenerator(dim)