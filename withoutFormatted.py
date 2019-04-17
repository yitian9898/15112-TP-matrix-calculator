######
# this script containing unformatted matrix operations is solely developed and written by Tianyi Zhu
######
# fix python 2.7 division issues by importing python 3.6 division module
from __future__ import division
# import all modules
import math
import copy
import decimal
from sympy import*
from matrixOperations import*
import numpy as np

# this function takes in a matrix and returns false if the matrix is not square or invertible, else returns the inverse matrix
# this function solves the inverse of the matrix by performing Gaussian-Jordan elimination
def inverseNoFormat(a):
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
                    return b
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
    return b
# Sympy Implementation of rref
def rrefSymNoFormat(a):
    b = copy.deepcopy(a)
    m = Matrix(b)
    l = m.rref()[0]
    new = np.array(l).astype(np.float64).tolist()
    return new
# this function takes in a matrix whose rows are linearly independent vectors and returns a matrix whose rows are a set of orthonormalized vectors
def gramSchmidtNoFormat(a):
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
    return Q
# this function takes in a matrix and returns a matrix whose rows are the bases for the row space of the original matrix
def rowSpaceBasisNoFormat(a):
    bases = []
    original = copy.deepcopy(a)
    RREF = rrefSymNoFormat(a)
    cols = len(RREF[0])
    count = 0
    for i in range(len(RREF)):
        if RREF[i].count(0) != cols:
            bases.append(original[i])
    return bases
# this function takes in a matrix and returns a matrix whose rows are the bases for the row space of the original matrix
def colSpaceBasisNoFormat(a):
    bases = []
    originalTrans = transposed(copy.deepcopy(a))
    RREF = rrefSymNoFormat(a)
    RREFtrans = transposed(RREF)
    r = len(RREFtrans)
    count = 0
    for i in range(len(RREFtrans)):
        if RREFtrans[i].count(1) == 1 and RREFtrans[i].count(0) == (r - 1):
            bases.append(originalTrans[i])
    return bases
# this function takes in a matrix and returns a matrix whose rows are the bases for the row space of the original matrix
def nullSpaceBasisNoFormat(a):
    m = Matrix(a)
    # the sympy implementation of nullspace
    l = m.nullspace()
    new = np.array(l).astype(np.float64).tolist()
    if len(new) == 0:
        return "Nullspace is empty!"
    else:
        return new
# this function takes in a matrix whose rows are a set of vectors that spann a vector space. It returns a matrix whose rows form a basis for that vector space
def basisOfSpaceSpannedBySetNoFormat(a):
    # the same as finding the basis for the row space
    return rowSpaceBasisNoFormat(a)