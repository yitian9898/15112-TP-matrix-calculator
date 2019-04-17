######
# this script containing matrix operations is solely developed and written by Tianyi Zhu
######
# fix python 2.7 division issues by importing python 3.6 division module
from __future__ import division
# import all modules
import math
import copy
import decimal
from sympy import*
import numpy as np
# roundHalfUp from 15-112 hw1
######
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
######
# almostEqual from 15-112 hw1
######
def almostEqual(d1, d2):
    epsilon=10**-2
    return (abs(d2 - d1) < epsilon)
######
# this function takes in two possible matrices and returns False if the addition is not legal, else returns the result of addition as a new matrix
def addition(a, b):
    rowA = len(a)
    colA = len(a[0])
    rowB = len(b)
    colB = len(b[0])
    # the matrices have different dimentions
    if rowA != rowB or colA != colB:
        # return error message
        return "Matrices do not have the same dimensions!"
    else:
        result = [ ([0] * colA) for row in range(rowA) ]
        for row in range(rowA):
            for col in range(colA):
                result[row][col] = a[row][col] + b[row][col]
    return result
# this function takes in two possible matrices and returns False if the subtraction is not legal, else returns the result of subtraction as a new matrix
def subtraction(a, b):
    rowA = len(a)
    colA = len(a[0])
    rowB = len(b)
    colB = len(b[0])
    # the matrices have different dimensions
    if rowA != rowB or colA != colB:
        # return error message
        return "Matrices do not have the same dimensions!"
    else:
        result = [ ([0] * colA) for row in range(rowA) ]
        for row in range(rowA):
            for col in range(colA):
                result[row][col] = a[row][col] - b[row][col]
    return result
# this function takes in two possible matrices and returns False if the subtraction is not legal, else returns the result of subtraction as a new matrix
def multiplication(a, b):
    rowA = len(a)
    colA = len(a[0])
    rowB = len(b)
    colB = len(b[0])
    # the matrices have different inner dimensions
    if colA != rowB:
        # return error message
        return "Matrices do not have the same inner dimensions!"
    else:
        result = [ ([0] * colB) for row in range(rowA) ]
        for i in range(rowA):
            for j in range(colB):
                for k in range(rowB):
                    result[i][j] += a[i][k] * b[k][j]
    return result
# this function takes in a matrix and returns the transposed matrix
def transposed(a):
    row = len(a)
    col = len(a[0])
    result = [ ([0] * row) for i in range(col) ]
    for i in range(row):
        for j in range(col):
            result[j][i] = a[i][j]
    return result
# this recursive function takes in a matrix and returns False if the input matrix is not square or is a 1x1 matrix, else returns the determinant of the original square matrix
# this function computes the determinant by using the Laplace expansion formula
def determinant(a):
    row = len(a)
    col = len(a[0])
    entryList = []
    # if not square matrix
    if row != col:
        # return error message
        return "Matrix is not square!"
    # if matrix has only one row
    if row <= 1:
        # return error message
        return "Matrix has a single row!"
    # base case for recursion: the matrix is 2x2
    if col == 2:
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]
    # recursively Laplace expand
    else:
        for j in range(col):
            new = copy.deepcopy(a)
            del new[0]
            deleteCol(new, j)
            multiplier = a[0][j] * math.pow(-1, (2+j))
            det = determinant(new)
            entryList.append(multiplier * det)
        return int(sum(entryList))
# this function takes in a matrix, a row index i, and a row index j. It destructively modify the input matrix by swapping the i th row and the j th row
def swapRow(a, i, j):
    a[i], a[j] = a[j], a[i]
    return a
# this function takes in the number of rows and cols, n, and return a square indentity matrix of the specified dimension
def makeIdentity(n):
    identity = [ ([0] * n) for row in range(n) ]
    for i in range(n):
        for j in range(n):
            if i == j:
                identity[i][j] = 1
    return identity
# this function takes in a matrix and a key and destructively removes the specified column from the matrix
def deleteCol(a, key):
    row = len(a)
    for i in range(row):
        del a[i][key]
# this function takes in a matrix, a row index, and a column index to see if only zeros exist at or below row i in col j
def checkForZeros(a, i, j):
    rows = len(a)
    cols = len(a[0])
    nonZeros = []
    firstNonZero = -1
    for m in range(i, rows):
        nonZero = a[m][j]!=0
        nonZeros.append(nonZero)
        if firstNonZero == -1 and nonZero:
            firstNonZero = m
    zeroSum = sum(nonZeros)
    return zeroSum, firstNonZero
# this function takes in a matrix and returns false if the matrix is not square or invertible, else returns the inverse matrix
# this function solves the inverse of the matrix by performing Gaussian-Jordan elimination
def inverse(a):
    b = copy.deepcopy(a)
    rows = len(b)
    cols = len(b[0])
    # if matrix not square
    if rows != cols:
        # return error message
        return "Matrix is not square!"
    # if matrix not invertible
    if determinant(b) == 0:
        # return error message
        return "Matrix is not invertible!"
    else:
        identity = makeIdentity(rows)
        # append identity to the right side
        for i in range(rows):
            b[i] += identity[i]
        # this is the standard row reduced procedure
        i = 0
        for j in range(cols):
            zeroSum, firstNonZero = checkForZeros(b, i, j)
            if zeroSum == 0:
                if j == cols:
                    return formatted(b)
            if firstNonZero != i:
                b = swapRow(b, i, firstNonZero)
            b[i] = [m/b[i][j] for m in b[i]]
            for q in range(rows):
                if q != i:
                    scaledRow = [b[q][j] * m for m in b[i]]
                    b[q] = [b[q][m] - scaledRow[m] for m in range(len(scaledRow))]
            if i == rows or j == cols:
                break
            i += 1
        # return the right side of the matrix
        for i in range(rows):
            b[i] = b[i][cols:len(b[i])]
    return formatted(b)
# this function takes in a matrix and outputs a formatted matrix
def formatted(a):
    b = copy.deepcopy(a)
    rows = len(b)
    cols = len(b[0])
    for i in range(rows):
        for j in range(cols):
            # if the entry is an integer, convert to int type
            if almostEqual(int(b[i][j]), b[i][j]):
                b[i][j] = int(b[i][j])
            # if the entry is a float, convert to two decimal float
            if not almostEqual(int(b[i][j]), b[i][j]):
                b[i][j] = roundHalfUp(b[i][j]*100)/100
    return b
# Sympy Implementation of rref
def rrefSym(a):
    b = copy.deepcopy(a)
    m = Matrix(b)
    l = m.rref()[0]
    new = np.array(l).astype(np.float64).tolist()
    return formatted(new)
# this customized rref function takes in a matrix and returns the reduced row echelon form of the matrix
def rrefCus(a):
    b = copy.deepcopy(a)
    lead = 0
    row = len(b)
    col = len(b[0])
    for r in range(row):
        if lead >= col:
            new = formatted(b)
            return new
        i = r
        while b[i][lead] == 0:
            i += 1
            if i == row:
                i = r
                lead += 1
                if col == lead:
                    new = formatted(b)
                    return new
        swapRow(b, i, r)
        leadVar = b[r][lead]
        b[r] = [ rowElem / float(leadVar) for rowElem in b[r]]
        for i in range(row):
            if i != r:
                leadVar = b[i][lead]
                b[i] = [ iVar - leadVar * rVar for rVar,iVar in zip(b[r],b[i])]
        lead += 1
    new = formatted(b)
    return new
# this function takes in two vectors as 1D lists. It returns False if two vectors have different dimensions, else adds two vectors
def vectAdd(a, b):
    if len(a) != len(b):
        return False
    else:
        new = []
        for i in range(len(a)):
            new.append(a[i] + b[i])
    return new
# this function takes in two vectors as 1D lists. It returns False if two vectors have different dimensions, else subtracts two vectors
def vectSub(a, b):
    if len(a) != len(b):
        return False
    else:
        new = []
        for i in range(len(a)):
            new.append(a[i] - b[i])
    return new
# this function takes a possibly-0 multiplier and a vector. It returns a new vector whose entries are scaled by the multiplier
def vectorScal(num, a):
    new = []
    for i in range(len(a)):
        new.append(num * a[i])
    return new
# this function takes in two vectors as 1D lists. It returns False if two vectors have different dimensions, else returns the dot product of two vectors
def dotProduct(a, b):
    if len(a) != len(b):
        return False
    else:
        dotProduct = 0
        for i in range(len(a)):
            dotProduct += a[i]*b[i]
    return dotProduct
# this function takes in a matrix whose rows are linearly independent vectors and returns a matrix whose rows are a set of orthogonalized vectors
def gramSchmidt(a):
    copyA = copy.deepcopy(a)
    # if condition not met
    if linearDep(a) == "linearly dependent":
        # return error message
        return "Not linearly independent vectors!"
    else:
        a = copyA
        rows = len(a)
        cols = len(a[0])
        Y = [0] * rows
        Q = [[0] * cols for row in range(rows)]
        # set X1 to V1
        productX1 = 1.0 / math.sqrt(dotProduct(a[0],a[0]))
        Q[0] = vectorScal(productX1, a[0])
        # find X2, X3,...
        for j in range(1, rows):
            Y = a[j]
            for i in range(0, j):
                Y = vectSub(Y, vectorScal(dotProduct(a[j], Q[i]), Q[i]))
            productYj = 1.0 / math.sqrt(dotProduct(Y, Y))
            Q[j] = vectorScal(productYj, Y)
    return formatted(Q)
# this function takes in a matrix and returns the rank of the matrix
def rank(a):
    RREF = rrefSym(a)
    rows = len(RREF)
    cols = len(RREF[0])
    # count rows of zeros
    count = 0
    for row in RREF:
        if row.count(0) == cols:
            count += 1
    # num of non-zero rows
    return rows - count
# this function takes in a matrix whose rows are a set of spanning vectors and the dimension n of R^n. It returns True if the vector set spans R^n, else returns False
def spanSpace(a, n):
    if rank(a) == n:
        return "the vector set spans R^n"
    else:
        return "the vector set does not span R^n"
# this function takes in a matrix whose rows are a set of vectors. It returns True if the set of vectors are linearly dependent, else returns False
def linearDep(a):
    RREF = rrefSym(a)
    rows = len(RREF)
    cols = len(RREF[0])
    # count rows of zeros
    count = 0
    for row in RREF:
        if row.count(0) == cols:
            count += 1
    if count != 0:
        return "linearly dependent"
    elif count == 0:
        return "linearly independent"
# this function takes in a matrix and returns a matrix whose rows are the bases for the row space of the original matrix
def rowSpaceBasis(a):
    bases = []
    original = copy.deepcopy(a)
    RREF = rrefSym(a)
    cols = len(RREF[0])
    count = 0
    for i in range(len(RREF)):
        if RREF[i].count(0) != cols:
            bases.append(original[i])
    return formatted(bases)
# this function takes in a matrix and returns a matrix whose rows are the bases for the row space of the original matrix
def colSpaceBasis(a):
    bases = []
    originalTrans = transposed(copy.deepcopy(a))
    RREF = rrefSym(a)
    RREFtrans = transposed(RREF)
    r = len(RREFtrans)
    count = 0
    for i in range(len(RREFtrans)):
        if RREFtrans[i].count(1) == 1 and RREFtrans[i].count(0) == (r - 1):
            bases.append(originalTrans[i])
    return formatted(bases)
# this function takes in a matrix and returns a matrix whose rows are the bases for the row space of the original matrix
def nullSpaceBasis(a):
    m = Matrix(a)
    # the sympy implementation of nullspace
    l = m.nullspace()
    new = np.array(l).astype(np.float64).tolist()
    if len(new) == 0:
        return "Nullspace is empty!"
    else:
        return formatted(new)
# this function takes in a matrix whose rows are a set of vectors that spann a vector space. It returns a matrix whose rows form a basis for that vector space
def basisOfSpaceSpannedBySet(a):
    # the same as finding the basis for the row space
    return rowSpaceBasis(a)