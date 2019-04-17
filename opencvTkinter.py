######
# this user interface is solely developed and written by Tianyi Zhu
# important note:
# the run function and the drawCamera function are modified from 15-112 openCV github code snippets, written by Vasu Agrawal
######
# fix python 2.7 division issues by importing python 3.6 division module
from __future__ import division
# import all necessary modules
import time
import os
import sys
import random
# import customized functions from local path
from withoutFormatted import*
from matrixOperations import*
from recognition import*
from generator import*
from bank import*
# Tkinter selector based on python versions
# in this project, default python version is 2.7 for openCV2 compatibility
if sys.version_info[0] < 3:
    from Tkinter import *
    import Tkinter as tk
else:
    from tkinter import *
    import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
####################################
# init
####################################
def init(data):
    # Initialize the webcam
    camera = cv2.VideoCapture(data.camera_index)
    data.camera = camera
    # default startScreen mode
    data.mode = "startScr"
    data.opType = ""
    # default: no recognition error
    data.error = False
    data.errorM1 = False
    data.errorM2 = False
    # initialize matrices
    data.matrix1 = []
    data.matrix2 = []
    # "practice" hypermode: data fields
    data.diffLevel = 0
    data.currentProblemNum = 0
    data.correct = 0
    data.wrong = 0
    data.problem = []
    data.averageScore = 0
    data.correctAnswer = []
    data.userAnswer = []
    data.status = True
    data.entryList = []
    # problem bank for gramSchmidt problems
    data.gramBank1 = bank1()
    data.gramBank2 = bank2()
    data.gramBank3 = bank3()
    data.gramBank4 = bank4()
####################################
# mode dispatcher
####################################
def mousePressed(event, data):
    if (data.mode == "startScr"): startScrMousePressed(event, data)
    elif (data.mode == "camScr"):   camScrMousePressed(event, data)
    elif (data.mode == "menuScr"):  menuScrMousePressed(event, data)
    elif (data.mode == "confirmScr"):  confirmScrMousePressed(event, data)
    elif (data.mode == "resultScr"): resultScrMousePressed(event, data)
    elif (data.mode == "showProblem"): showProblemMousePressed(event, data)
    elif (data.mode == "showResult"): showResultMousePressed(event, data)
    elif (data.mode == "showScore"): showScoreMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "startScr"): startScrKeyPressed(event, data)
    elif (data.mode == "camScr"):   camScrKeyPressed(event, data)
    elif (data.mode == "menuScr"):       menuScrKeyPressed(event, data)
    elif (data.mode == "confirmScr"):    confirmScrKeyPressed(event, data)
    elif (data.mode == "resultScr"):       resultScrKeyPressed(event, data)
    elif (data.mode == "showProblem"): showProblemKeyPressed(event, data)
    elif (data.mode == "showResult"): showResultKeyPressed(event, data)
    elif (data.mode == "showScore"): showScoreKeyPressed(event, data)

def redrawAll(canvas, data):
    if (data.mode == "startScr"): startScrRedrawAll(canvas, data)
    elif (data.mode == "camScr"):   camScrRedrawAll(canvas, data)
    elif (data.mode == "menuScr"):  menuScrRedrawAll(canvas, data)
    elif (data.mode == "confirmScr"):  confirmScrRedrawAll(canvas, data)
    elif (data.mode == "resultScr"):  resultScrRedrawAll(canvas, data)
    elif (data.mode == "showProblem"): showProblemRedrawAll(canvas, data)
    elif (data.mode == "showResult"): showResultRedrawAll(canvas, data)
    elif (data.mode == "showScore"): showScoreRedrawAll(canvas, data)

####################################
# showProblem mode
####################################
def showProblemMousePressed(event, data):
    pass
def showProblemKeyPressed(event, data):        
    if event.keysym == "m":
        data.problem = []
        data.mode = "menuScr"

    if event.keysym == "p":
        if data.opType == "inv" or data.opType == "gram" or data.opType == "nullBasis" or data.opType == "det" or data.opType == "rank" or data.opType == "lineDep":
            collectInput(data)
        else:
            data.mode = "camScr"

def collectInput(data):
    def retrieveSingleTextInput():
        input = text.get("1.0","end-1c")
        if data.opType == "rank" or data.opType == "det":
            data.userAnswer = int(input)
        if data.opType == "lineDep":
            data.userAnswer = input

    def retrieveEntrieInput():
        entries = [ [0] * cols for r in range(rows)]
        for i in range(rows):
            for j in range(cols):
                entries[i][j] = float(newList[i][j].get())
        data.userAnswer = entries

    def destroySingle():
        updateResult(data)
        single.destroy()
        data.mode = "showResult"
    def destroyEnt():
        updateResult(data)
        ent.destroy()
        data.mode = "showResult"

    if data.opType == "det" or data.opType == "rank" or data.opType == "lineDep":
        
        single = Tk()
        single.title("Value")
        # initialize textfield
        text = Text(single, height=30, width=30)
        # set default value of textField
        if data.opType == "lineDep":
            text.insert(END, "'linearly dependent' or 'linearly independent'")
        # create buttons
        buttonEnter = Button(single, text="Enter", command=retrieveSingleTextInput)
        buttonExit = Button(single, text="Exit", command=destroySingle)
        # pack the buttons and text
        buttonExit.pack()
        buttonEnter.pack()
        text.pack()

    if data.opType == "inv" or data.opType == "gram" or data.opType == "nullBasis":
        
        ent = Tk()
        rows = len(data.correctAnswer)
        cols = len(data.correctAnswer[0])
        newList = [ [0] * cols for r in range(rows)]
        
        for i in range(rows):
            for j in range(cols):
                newList[i][j] = Entry(ent)
                newList[i][j].grid(row=i, column=j)

        buttonEnter = Button(ent, text="Enter", command=retrieveEntrieInput)
        buttonExit = Button(ent, text="Exit", command=destroyEnt)

        buttonEnter.grid(columnspan=(rows+1))
        buttonExit.grid(columnspan=(rows+2))
        
def showProblemDrawText(canvas, data):
    canvas.create_text(data.width/2, 40, text="You are on problem %s" % str(data.currentProblemNum), font="Arial 40")
    canvas.create_text(data.width/2, 80, text="Press 'm' to show menu", font="Arial 20")
    canvas.create_text(data.width/2, data.height - 100, text="Press 'p' to scan or enter result", fill="dark blue", font="Arial 20")
    canvas.create_text(100, 40, text="%s right / %s wrong" % (str(data.correct),str(data.wrong)), font="Arial 20")
    if len(data.problem) != 0 and isinstance(data.problem[0][0], list):

        canvas.create_text(data.width/3, 170, text="Matrix #1", font="Arial 40")
        j = 230
        for row in data.problem[0]:
            canvas.create_text(data.width/3, j, text=str(row), font="Arial 40")
            j += 40
        
        canvas.create_text(data.width/3*2, 170, text="Matrix #2", font="Arial 40")
        k = 230
        for row in data.problem[1]:
            canvas.create_text(data.width/3*2, k, text=str(row), font="Arial 40")
            k += 40

    elif len(data.problem) != 0:
        i = 230
        for row in data.problem:
            canvas.create_text(data.width/2, i, text=str(row), font="Arial 40")
            i += 40

def makeProblem(data):
    if data.diffLevel != 4:
        if data.opType == "add":
            if data.diffLevel == 0:
                data.problem = callWithLargeStack(addGen,2,2)
                data.correctAnswer = addition(data.problem[0], data.problem[1])
            if data.diffLevel == 1:
                data.problem = callWithLargeStack(addGen,random.randint(2,3),random.randint(2,3))
                data.correctAnswer = addition(data.problem[0], data.problem[1])
            if data.diffLevel == 2:
                data.problem = callWithLargeStack(addGen,3,3)
                data.correctAnswer = addition(data.problem[0], data.problem[1])
            if data.diffLevel == 3:
                data.problem = callWithLargeStack(addGen,random.randint(2,4),random.randint(2,4))
                data.correctAnswer = addition(data.problem[0], data.problem[1])
        if data.opType == "trans":
            if data.diffLevel == 0:
                data.problem = randomMatrixGenerator(random.randint(2,3),random.randint(2,3))
                data.correctAnswer = transposed(data.problem)
            if data.diffLevel == 1:
                data.problem = randomMatrixGenerator(random.randint(2,3),random.randint(3,4))
                data.correctAnswer = transposed(data.problem)
            if data.diffLevel == 2:
                data.problem = randomMatrixGenerator(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = transposed(data.problem)
            if data.diffLevel == 3:
                data.problem = randomMatrixGenerator(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = transposed(data.problem)
        if data.opType == "rref":
            if data.diffLevel == 0:
                data.problem = rrefGen(random.randint(2,3),random.randint(2,3))
                data.correctAnswer = rrefSymNoFormat(data.problem)
                print("correct: "+str(data.correctAnswer))

            if data.diffLevel == 1:
                data.problem = rrefGen(random.randint(2,3),random.randint(3,4))
                data.correctAnswer = rrefSymNoFormat(data.problem)
                print("correct: "+str(data.correctAnswer))

            if data.diffLevel == 2:
                data.problem = rrefGen(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = rrefSymNoFormat(data.problem)
                print("correct: "+str(data.correctAnswer))

            if data.diffLevel == 3:
                data.problem = rrefGen(random.randint(4,5),random.randint(5,6))
                data.correctAnswer = rrefSymNoFormat(data.problem)
                print("correct: "+str(data.correctAnswer))
        if data.opType == "lineDep":
            if data.diffLevel == 0:
                data.problem = randomMatrixGenerator(2,2)
                data.correctAnswer = linearDep(data.problem)
            if data.diffLevel == 1:
                data.problem = randomMatrixGenerator(random.randint(2,3),random.randint(3,4))
                data.correctAnswer = linearDep(data.problem)
            if data.diffLevel == 2:
                data.problem = randomMatrixGenerator(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = linearDep(data.problem)
            if data.diffLevel == 3:
                data.problem = randomMatrixGenerator(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = linearDep(data.problem)
        if data.opType == "nullBasis":
            if data.diffLevel == 0:
                data.problem = randomMatrixGenerator(random.randint(2,3),random.randint(2,3))
                data.correctAnswer = nullSpaceBasisNoFormat(data.problem)
            if data.diffLevel == 1:
                data.problem = randomMatrixGenerator(random.randint(2,3),random.randint(3,4))
                data.correctAnswer = nullSpaceBasisNoFormat(data.problem)
            if data.diffLevel == 2:
                data.problem = randomMatrixGenerator(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = nullSpaceBasisNoFormat(data.problem)
            if data.diffLevel == 3:
                data.problem = randomMatrixGenerator(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = nullSpaceBasisNoFormat(data.problem)
        if data.opType == "sub":
            if data.diffLevel == 0:
                data.problem = callWithLargeStack(subGen,2,2)
                data.correctAnswer = subtraction(data.problem[0], data.problem[1])
            if data.diffLevel == 1:
                data.problem = callWithLargeStack(subGen,random.randint(2,3),random.randint(2,3))
                data.correctAnswer = subtraction(data.problem[0], data.problem[1])
            if data.diffLevel == 2:
                data.problem = callWithLargeStack(subGen,3,3)
                data.correctAnswer = subtraction(data.problem[0], data.problem[1])
            if data.diffLevel == 3:
                data.problem = callWithLargeStack(subGen,random.randint(2,4),random.randint(2,4))
                data.correctAnswer = subtraction(data.problem[0], data.problem[1])
        if data.opType == "det":
            if data.diffLevel == 0:
                data.problem = squareMatrixGenerator(2)
                data.correctAnswer = determinant(data.problem)
            if data.diffLevel == 1:
                data.problem = squareMatrixGenerator(3)
                data.correctAnswer = determinant(data.problem)
            if data.diffLevel == 2:
                data.problem = squareMatrixGenerator(4)
                date.correctAnswer = determinant(data.problem)
            if data.diffLevel == 3:
                data.problem = squareMatrixGenerator(5)
                data.correctAnswer = determinant(data.problem)

        if data.opType == "gram":
            if data.diffLevel == 0:
                data.problem = data.gramBank1[random.randint(0, len(data.gramBank1)-1)]
                data.correctAnswer = gramSchmidtNoFormat(data.problem)
            if data.diffLevel == 1:
                data.problem = data.gramBank2[random.randint(0, len(data.gramBank2)-1)]
                data.correctAnswer = gramSchmidtNoFormat(data.problem)
            if data.diffLevel == 2:
                data.problem = data.gramBank3[random.randint(0, len(data.gramBank3)-1)]
                data.correctAnswer = gramSchmidtNoFormat(data.problem)
            if data.diffLevel == 3:
                data.problem = data.gramBank4[random.randint(0, len(data.gramBank4)-1)]
                data.correctAnswer = gramSchmidtNoFormat(data.problem)

        if data.opType == "rowBasis":
            if data.diffLevel == 0:
                data.problem = randomMatrixGenerator(random.randint(2,3),random.randint(2,3))
                data.correctAnswer = rowSpaceBasisNoFormat(data.problem)
            if data.diffLevel == 1:
                data.problem = randomMatrixGenerator(random.randint(2,3),random.randint(3,4))
                data.correctAnswer = rowSpaceBasisNoFormat(data.problem)
            if data.diffLevel == 2:
                data.problem = randomMatrixGenerator(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = rowSpaceBasisNoFormat(data.problem)
            if data.diffLevel == 3:
                data.problem = randomMatrixGenerator(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = rowSpaceBasisNoFormat(data.problem)
        if data.opType == "multi":
            if data.diffLevel == 0:
                data.problem = multiGen(random.randint(2,3),random.randint(2,3),random.randint(2,3))
                data.correctAnswer = multiplication(data.problem[0], data.problem[1])
                # debug
                print("correct: "+ str(data.correctAnswer))

            if data.diffLevel == 1:
                data.problem = multiGen(random.randint(2,3),random.randint(3,4),random.randint(2,3))
                data.correctAnswer = multiplication(data.problem[0], data.problem[1])
                # debug
                print("correct: "+ str(data.correctAnswer))

            if data.diffLevel == 2:
                data.problem = multiGen(random.randint(3,4),random.randint(3,4),random.randint(3,4))
                data.correctAnswer = multiplication(data.problem[0], data.problem[1])
                # debug
                print("correct: "+ str(data.correctAnswer))

            if data.diffLevel == 3:
                data.problem = multiGen(random.randint(3,4),random.randint(3,4),random.randint(3,4))
                data.correctAnswer = multiplication(data.problem[0], data.problem[1])
                # debug
                print("correct: "+ str(data.correctAnswer))

        if data.opType == "inv":
            if data.diffLevel == 0:
                data.problem = inverseGenerator(2)
                data.correctAnswer = inverseNoFormat(data.problem)
                print("correct: "+ str(formatted(data.correctAnswer)))
            if data.diffLevel == 1:
                data.problem = inverseGenerator(3)
                data.correctAnswer = inverseNoFormat(data.problem)
                print("correct: "+ str(formatted(data.correctAnswer)))
            if data.diffLevel == 2:
                data.problem = inverseGenerator(4)
                data.correctAnswer = inverseNoFormat(data.problem)
                print("correct: "+ str(formatted(data.correctAnswer)))
            if data.diffLevel == 3:
                data.problem = inverseGenerator(4)
                data.correctAnswer = inverseNoFormat(data.problem)
                print("correct: "+ str(formatted(data.correctAnswer)))

        if data.opType == "rank":
            if data.diffLevel == 0:
                data.problem = randomMatrixGenerator(random.randint(2,3),random.randint(2,3))
                data.correctAnswer = rank(data.problem)
            if data.diffLevel == 1:
                data.problem = randomMatrixGenerator(random.randint(2,3),random.randint(3,4))
                data.correctAnswer = rank(data.problem)
            if data.diffLevel == 2:
                data.problem = randomMatrixGenerator(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = rank(data.problem)
            if data.diffLevel == 3:
                data.problem = randomMatrixGenerator(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = rank(data.problem)
        if data.opType == "colBasis":
            if data.diffLevel == 0:
                data.problem = randomMatrixGenerator(random.randint(2,3),random.randint(2,3))
                data.correctAnswer = colSpaceBasisNoFormat(data.problem)
            if data.diffLevel == 1:
                data.problem = randomMatrixGenerator(random.randint(2,3),random.randint(3,4))
                data.correctAnswer = colSpaceBasisNoFormat(data.problem)
            if data.diffLevel == 2:
                data.problem = randomMatrixGenerator(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = colSpaceBasisNoFormat(data.problem)
            if data.diffLevel == 3:
                data.problem = randomMatrixGenerator(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = colSpaceBasisNoFormat(data.problem)
        if data.opType == "spaceBasis":
            if data.diffLevel == 0:
                data.problem = randomMatrixGenerator(random.randint(2,3),random.randint(2,3))
                data.correctAnswer = basisOfSpaceSpannedBySetNoFormat(data.problem)
            if data.diffLevel == 1:
                data.problem = randomMatrixGenerator(random.randint(2,3),random.randint(3,4))
                data.correctAnswer = basisOfSpaceSpannedBySetNoFormat(data.problem)
            if data.diffLevel == 2:
                data.problem = randomMatrixGenerator(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = basisOfSpaceSpannedBySetNoFormat(data.problem)
            if data.diffLevel == 3:
                data.problem = randomMatrixGenerator(random.randint(3,4),random.randint(4,5))
                data.correctAnswer = basisOfSpaceSpannedBySetNoFormat(data.problem)
def showProblemRedrawAll(canvas, data):
    showProblemDrawText(canvas, data)
####################################
# showScore mode
####################################
def showScoreMousePressed(event, data):
    pass
def showScoreKeyPressed(event, data):
    if event.keysym == "r":
        # try remove the image files from the local path if they exist
        try:
            os.remove("1.jpeg")
            os.remove("2.jpeg")
        # pass if the image files do not exist in the local path
        except:
            pass
        init(data)

def calcScore(data):
    data.averageScore = data.correct / data.currentProblemNum

def showScoreDrawText(canvas, data):
    canvas.create_text(data.width/2, 50, text="Here is your final score", font="Arial 40 bold")
    canvas.create_text(data.width/2, 150, text="You have %s right / %s wrong" % (str(data.correct),str(data.wrong)), font = "Arial 30")
    canvas.create_text(data.width/2, 200, text="You scored %s percent correctly" % str(roundHalfUp(data.averageScore*100)), font="Arial 25")
    canvas.create_text(data.width/2, data.height-200, text="Press 'r' to restart", font="Arial 35 bold")

def showScoreRedrawAll(canvas, data):
    showScoreDrawText(canvas, data)
####################################
# showResult mode
####################################
def showResultMousePressed(event, data):
    pass
def showResultKeyPressed(event, data):
    if event.keysym == "p":
        if data.diffLevel == 4:
            calcScore(data)
            data.mode = "showScore"
        else:
            makeProblem(data)
            data.mode = "showProblem"
def checkMatrixResult(data):
    if len(data.userAnswer) != len(data.correctAnswer) or len(data.userAnswer[0]) != len(data.correctAnswer[0]):
        data.status = False
    else:
        for i in range(len(data.userAnswer)):
            for j in range(len(data.userAnswer[0])):
                if not almostEqual(data.userAnswer[i][j], data.correctAnswer[i][j]):
                    data.status = False
def checkOtherResult(data):
    if data.userAnswer == data.correctAnswer:
        data.status = True
    else:
        data.status = False
def updateResult(data):
    data.status = True
    if data.opType == "det" or data.opType == "rank" or data.opType == "lineDep":
        checkOtherResult(data)
    else:
        checkMatrixResult(data)
    if data.status == True:
        data.currentProblemNum += 1
        data.correct += 1
        data.diffLevel += 1
    else:
        data.currentProblemNum += 1
        data.wrong += 1
def showResultDrawText(canvas, data):
    canvas.create_text(data.width/2, data.height-120, text="Press 'p' to proceed", font="Arial 20")
    canvas.create_text(data.width/2, 50, text="How did you do on the last problem?", font="Arial 40 bold")
    if data.status == True:
        canvas.create_text(data.width/2, data.height/2-70, text="Yes, you got it right!", fill="dark green", font="Arial 50 bold")
        canvas.create_text(data.width/2, data.height/2, text="You have %s right / %s wrong" % (str(data.correct),str(data.wrong)), font = "Arial 30")
    else:
        canvas.create_text(data.width/2, data.height/2-70, text="Sorry, you got it wrong!", fill="dark red", font="Arial 50 bold")
        canvas.create_text(data.width/2, data.height/2, text="You have %s right / %s wrong" % (str(data.correct),str(data.wrong)), font = "Arial 30")
def showResultRedrawAll(canvas, data):
    showResultDrawText(canvas, data)
####################################
# startScreen mode
####################################
def startScrMousePressed(event, data):
    x = event.x
    y = event.y
    for i in range(len(data.startScrButtons)):
        if data.startScrButtons[i][0] <= x <= data.startScrButtons[i][2] and \
                data.startScrButtons[i][1] <= y <= data.startScrButtons[i][3]:
            if i == 0:
                data.hyperMode = "calculate"
                data.mode = "menuScr"
            if i == 1:
                data.hyperMode = "practice"
                data.mode = "menuScr"
# keypress events on startScreen
def startScrKeyPressed(event, data):
    pass
def drawCalcModeText(canvas, data):
    canvas.create_text(data.width/2, 0.05*data.height+40,
                       text="Welcome to Matrix Calculator!", font="Arial 50 bold")
    canvas.create_text(212, 0.05*data.height+270,
                        text= "1: Select a matrix operation", fill="blue", font="Arial 25")
    canvas.create_text(270, 0.05*data.height+340,
                        text= "2: Take a photo of the handwritten matrix", fill="dark green",font="Arial 23")
    canvas.create_text(225, 0.05*data.height+410,
                        text= "3: Confirm or edit input matrix", fill="red", font="Arial 25")                        
    canvas.create_text(128, 0.05*data.height+480,
                        text= "4: Get result", fill="orange red", font="Arial 25")
def drawPracModeText(canvas, data):
    canvas.create_text(720, 0.05*data.height+270,
                        text= "1: Select a matrix operation", fill="orange red", font="Arial 25")
    canvas.create_text(705, 0.05*data.height+340,
                        text= "2: Solve the given matrix", fill="red",font="Arial 25")
    canvas.create_text(764, 0.05*data.height+410,
                        text= "3: Take a photo of the solved matrix", fill="dark green",font="Arial 25")
    canvas.create_text(733, 0.05*data.height+480,
                        text= "4: Confirm or edit input matrix", fill="purple", font="Arial 25")                        
    canvas.create_text(650, 0.05*data.height+550,
                        text= "5: Check score", fill="blue", font="Arial 25")
def drawStartScrButtons(canvas, data):
    data.startScrButtons = [(150,160,380,250), (610,160,840,250)]
    for rect in data.startScrButtons:
        canvas.create_rectangle(rect, fill="white", width = 5)
def drawStartScrButtonsText(canvas, data):
    for i in range(len(data.startScrButtons)):
        x = (data.startScrButtons[i][0] + data.startScrButtons[i][2]) / 2
        y = (data.startScrButtons[i][1] + data.startScrButtons[i][3]) / 2
        if i == 0:
            canvas.create_text(x, y, text="Calculate", font="Arial 30 bold")
        if i == 1:
            canvas.create_text(x, y, text="Practice", font="Arial 30 bold")
# draws the step-by-step instructions on canvas
def startScrRedrawAll(canvas, data):
    drawStartScrButtons(canvas, data)
    drawStartScrButtonsText(canvas, data)
    drawCalcModeText(canvas, data)
    drawPracModeText(canvas, data)
####################################
# menuScreen mode
####################################
# menuScreen mouseclick events
def menuScrMousePressed(event, data):
    # get mouseclick positions on canvas
    x = event.x
    y = event.y
    # record type of matrix operation based on mouse click positions
    # go to cameraScreen after mouseclick
    for i in range(len(data.menuRects)):
        if data.menuRects[i][0] <= x <= data.menuRects[i][2] and \
           data.menuRects[i][1] <= y <= data.menuRects[i][3]:
            if i == 0 and data.hyperMode == "calculate":
                data.opType = "add"
                data.mode = "camScr"
            if i == 0 and data.hyperMode == "practice":
                data.opType = "add"
                makeProblem(data)
                data.mode = "showProblem"
            if i == 1 and data.hyperMode == "calculate":
                data.opType = "trans"
                data.mode = "camScr"
            if i == 1 and data.hyperMode == "practice":
                data.opType = "trans"
                makeProblem(data)
                data.mode = "showProblem"

            if i == 2 and data.hyperMode == "calculate":
                data.opType = "rref"
                data.mode = "camScr"
            if i == 2 and data.hyperMode == "practice":
                data.opType = "rref"
                makeProblem(data)
                data.mode = "showProblem"

            if i == 3 and data.hyperMode == "calculate":
                data.opType = "lineDep"
                data.mode = "camScr"
            if i == 3 and data.hyperMode == "practice":
                data.opType = "lineDep"
                makeProblem(data)
                data.mode = "showProblem"

            if i == 4 and data.hyperMode == "calculate":
                data.opType = "nullBasis"
                data.mode = "camScr"
            if i == 4 and data.hyperMode == "practice":
                data.opType = "nullBasis"
                makeProblem(data)
                data.mode = "showProblem"

            if i == 5 and data.hyperMode == "calculate":
                data.opType = "sub"
                data.mode = "camScr"
            if i == 5 and data.hyperMode == "practice":
                data.opType = "sub"
                makeProblem(data)
                data.mode = "showProblem"

            if i == 6 and data.hyperMode == "calculate":
                data.opType = "det"
                data.mode = "camScr"
            if i == 6 and data.hyperMode == "practice":
                data.opType = "det"
                makeProblem(data)
                data.mode = "showProblem"

            if i == 7 and data.hyperMode == "calculate":
                data.opType = "gram"
                data.mode = "camScr"
            if i == 7 and data.hyperMode == "practice":
                data.opType = "gram"
                makeProblem(data)
                data.mode = "showProblem"

            if i == 8 and data.hyperMode == "calculate":
                data.opType = "rowBasis"
                data.mode = "camScr"
            if i == 8 and data.hyperMode == "practice":
                data.opType = "rowBasis"
                makeProblem(data)
                data.mode = "showProblem"

            if i == 9 and data.hyperMode == "calculate":
                data.opType = "multi"
                data.mode = "camScr"
            if i == 9 and data.hyperMode == "practice":
                data.opType = "multi"
                makeProblem(data)
                data.mode = "showProblem"

            if i == 10 and data.hyperMode == "calculate":
                data.opType = "inv"
                data.mode = "camScr"
            if i == 10 and data.hyperMode == "practice":
                data.opType = "inv"
                makeProblem(data)
                data.mode = "showProblem"

            if i == 11 and data.hyperMode == "calculate":
                data.opType = "rank"
                data.mode = "camScr"
            if i == 11 and data.hyperMode == "practice":
                data.opType = "rank"
                makeProblem(data)
                data.mode = "showProblem"

            if i == 12 and data.hyperMode == "calculate":
                data.opType = "colBasis"
                data.mode = "camScr"
            if i == 12 and data.hyperMode == "practice":
                data.opType = "colBasis"
                makeProblem(data)
                data.mode = "showProblem"

            if i == 13 and data.hyperMode == "calculate":
                data.opType = "spaceBasis"
                data.mode = "camScr"
            if i == 13 and data.hyperMode == "practice":
                data.opType = "spaceBasis"
                makeProblem(data)
                data.mode = "showProblem"

# menuScreen keypress events
def menuScrKeyPressed(event, data):
    # if "b" is pressed
    if event.keysym == "b":
        # go to startScreen
        data.mode = "startScr"

# draw buttons for different operation types
def drawMenuButtons(canvas, data):
    # a list of tuples that has all the positional information of the buttons as rectangles on canvas
    # the first column of buttons
    data.menuRects = [(80,70,306,140),(80,210,306,280),(80,350,306,420),(80,490,306,560),(80,630,370,700),
    # the second column of buttons
             (386,70,612,140),(386,210,612,280),(386,350,612,420),(386,490,612,560),
    # the third column of buttons
             (692,70,918,140),(692,210,918,280),(692,350,918,420),(692,490,918,560),(450,630,918,700)]
    # draw buttons as rectangles on canvas
    for rect in data.menuRects:
        canvas.create_rectangle(rect,fill="white",width=3)
    # draw centered texts in the rectangle corresponding to buttons
    for i in range(len(data.menuRects)):
        # center the x and y positions of the text
        x = (data.menuRects[i][0] + data.menuRects[i][2]) / 2
        y = (data.menuRects[i][1] + data.menuRects[i][3]) / 2
        # given the tuple index in the list, draw the corresponding text
        if i == 0:
            canvas.create_text(x, y, text="addition", font="Arial 20")
        if i == 1:
            canvas.create_text(x, y, text="transpose", font="Arial 20")
        if i == 2:
            canvas.create_text(x, y, text="RREF", font="Arial 20")
        if i == 3:
            canvas.create_text(x, y, text="linear dependence", font="Arial 20")
        if i == 4:
            canvas.create_text(x, y, text="basis for null(A)", font="Arial 20")
        if i == 5:
            canvas.create_text(x, y, text="subtraction", font="Arial 20")
        if i == 6:
            canvas.create_text(x, y, text="determinant", font="Arial 20")
        if i == 7:
            canvas.create_text(x, y, text="gram-schmidt", font="Arial 20")
        if i == 8:
            canvas.create_text(x, y, text="basis for row(A)", font="Arial 20")
        if i == 9:
            canvas.create_text(x, y, text="multiplication", font="Arial 20")
        if i == 10:
            canvas.create_text(x, y, text="inverse", font="Arial 20")
        if i == 11:
            canvas.create_text(x, y, text="rank", font="Arial 20")
        if i == 12:
            canvas.create_text(x, y, text="basis for col(A)", font="Arial 20")
        if i == 13:
            canvas.create_text(x, y, text="basis for a space spanned by a set of vectors", font="Arial 20")
# draw eveything in the menuScreen
def menuScrRedrawAll(canvas, data):
    # press 'b' to go to startScreen
    canvas.create_text(125, 40, text="Press 'b' to go back to start page", font="Arial 15")
    # draw the centered page title
    canvas.create_text(data.width/2, 35, text="Select a Matrix Operation", font="Arial 30 bold")
    # draw all the buttons on the menuScreen
    drawMenuButtons(canvas, data)
####################################
# resultScreen mode
####################################
def resultScrMousePressed(event, data):
    pass
# keypress events on resultScreen
def resultScrKeyPressed(event, data):
    # if 's' is pressed
    if event.keysym == 's':
        # try remove the image files from the local path if they exist
        try:
            os.remove("1.jpeg")
            os.remove("2.jpeg")
        # pass if the image files do not exist in the local path
        except:
            pass
        init(data)
# set the result of computation according to different types of matrix operations
def computation(data):
    if data.opType == "add":
        # addition from matrixOperations
        data.result = addition(data.matrix1, data.matrix2)
    if data.opType == "trans":
        # transpose from matrixOperations
        data.result = transposed(data.matrix1)
    if data.opType == "rref":
        # reduced row echelon form from matrixOperations
        data.result = rrefSym(data.matrix1)
    if data.opType == "lineDep":
        # linear dependence check from matrixOperations
        data.result = linearDep(data.matrix1)
    if data.opType == "nullBasis":
        # give a basis for the nullspace from matrixOperations
        data.result = nullSpaceBasis(data.matrix1)
    if data.opType == "sub":
        # subtraction from matrixOperations
        data.result = subtraction(data.matrix1, data.matrix2)
    if data.opType == "det":
        # determinant from matrixOperations
        data.result = determinant(data.matrix1)
    if data.opType == "gram":
        # applying the gram-schmidt process to a set of vector from matrixOperations
        data.result = gramSchmidt(data.matrix1)
    if data.opType == "rowBasis":
        # give a basis for the rowspace from matrixOperations
        data.result = rowSpaceBasis(data.matrix1)
    if data.opType == "multi":
        # multiplication from matrixOperations
        data.result = multiplication(data.matrix1, data.matrix2)
    if data.opType == "inv":
        # using Gaussian-Jordan eliminantion to find inverse from matrixOperations
        data.result = inverse(data.matrix1)
    if data.opType == "rank":
        # rank from matrixOperations
        data.result = rank(data.matrix1)
    if data.opType == "colBasis":
        # give a basis for the column space from matrixOperations
        data.result = colSpaceBasis(data.matrix1)
    if data.opType == "spaceBasis":
        # give a basis for the space spanned by a set of vectors from matrixOperations
        data.result = basisOfSpaceSpannedBySet(data.matrix1)
# draw the result of the matrix operation
def drawResultText(canvas, data):
    # draw the centered title of the page
    canvas.create_text(data.width/2, 30, text="The result is:", font="Arial 30 bold")
    # draw the command
    canvas.create_text(data.width/4, 30, text="Press 's' to to restart", fill="blue", font="Arial 20")
    # if the result is a matrix
    if isinstance(data.result, list):
        # draw the result matrix row by row, centered on the screen
        i = 200
        for row in data.result:
            canvas.create_text(data.width/2, i, text=str(row), font="Arial 40")
            i += 80
    # if the result if not a matrix
    else:
        # draw the result directly
        canvas.create_text(data.width/2, data.height/2, text=str(data.result), font="Arial 40")
# draw everything on the resultScreen
def resultScrRedrawAll(canvas, data):
    # draw result as text
    drawResultText(canvas, data)
####################################
# confirmScreen mode
####################################
def confirmScrMousePressed(event, data):
    pass
# keypress events on confirmScreen
def confirmScrKeyPressed(event, data):
    # if 'c' is pressed
    if event.keysym == "c":
        if data.hyperMode == "calculate":
            # compute the result
            computation(data)
            # go to resultScreen
            data.mode = "resultScr"
        if data.hyperMode == "practice":
            updateResult(data)
            data.mode = "showResult"
    # 'b' is pressed
    if event.keysym == "b":
        # go to cameraScreen
        data.mode = "camScr"
    ######################## Customized Helper functions for confirmScrKeyPressed
    # this parser takes in a string representation of a matrix and return a 2D list represented by the string
    def stringTo2DList(str):
        noBuns = str[1:-1]
        row = noBuns.count("[")
        firstRow = noBuns[1:noBuns.index("]")]
        col = firstRow.count(",") + 1
        newList = [ ([0] * col) for i in range(row) ]
        nums = []
        for item in noBuns.split(","):
            item = item.strip()
            if "[" in item or "]" in item:
                if item[0] == "[":
                    nums.append(int(item[1:]))
                if item[-1] == "]":
                    nums.append(int(item[:-1]))
            else:
                nums.append(int(item))
        index = 0
        for i in range(len(newList)):
            for j in range(len(newList[0])):
                newList[i][j] = nums[index]
                index += 1
        return newList
    # this function retrieves text input from the Text widget as a string
    def retrieveTextInput():
        input = text.get("1.0","end-1c")
        # converts the string to a 2D list and set matrix1
        data.matrix1 = stringTo2DList(input)
    # this function retrieves text input from the Text widget as a string
    def retrieveM1Input():
        input = textM1.get("1.0","end-1c")
        # converts the string to a 2D list and set matrix1
        data.matrix1 = stringTo2DList(input)
    # this function retrieves text input from the Text widget as a string
    def retrieveM2Input():
        input = textM2.get("1.0","end-1c")
        # converts the string to a 2D list and set matrix2
        data.matrix2 = stringTo2DList(input)
    def retrievePracticeInput():
        input = text.get("1.0","end-1c")
        # converts the string to a 2D list and set matrix2
        data.userAnswer = stringTo2DList(input)
        print("user input: " + str(data.userAnswer))
    # destroys master Tk object
    def destroy():
        master.destroy()
    # destroys masterM Tk object
    def destroyM():
        masterM.destroy()
    ######################### Customized Helper functions for confirmScrKeyPressed end here
    # if 'e' is pressed
    if event.keysym == "e":
        if data.hyperMode == "calculate":
            # if the matrix operation is add, sub, or multi
            if data.opType == "add" or data.opType == "sub" or data.opType == "multi":
                # open a new Tk window
                masterM = Tk()
                masterM.title("2")
                # textField for matrix 1
                textM1 = Text(masterM, height=len(data.matrix1), width=len(str(data.matrix1))//len(data.matrix1))
                # set default value of textField
                textM1.insert(END, data.matrix1)
                # textField for matrix 2
                textM2 = Text(masterM, height=len(data.matrix2), width=len(str(data.matrix2))//len(data.matrix2))
                # set default value of textField
                textM2.insert(END, data.matrix2)
                # create button widgets
                buttonM1C = Button(masterM, text="Change M1", command=retrieveM1Input)
                buttonM2C = Button(masterM, text="Change M2", command=retrieveM2Input)
                buttonExitM = Button(masterM, text="Exit", command=destroyM)
                # lay out the buttons and texts in a grid
                buttonM1C.grid(row = 0, column = 0)
                buttonM2C.grid(row = 0, column = 1)
                textM1.grid(row = 1, column = 0)
                textM2.grid(row = 1, column = 1)
                buttonExitM.grid(columnspan=2)
            # if the matrix operation is not add, sub, or multi
            else:
                # create a new Tk window
                master = Tk()
                master.title("M")
                # initialize textfield
                text = Text(master, height=len(data.matrix1), width=len(str(data.matrix1))//len(data.matrix1))
                # set default value of textField
                text.insert(END, data.matrix1)
                # create buttons
                buttonC = Button(master, text="Change", command=retrieveTextInput)
                buttonExit = Button(master, text="Exit", command=destroy)
                # pack the buttons and text
                buttonExit.pack()
                buttonC.pack()
                text.pack()
        elif data.hyperMode == "practice":
            # create a new Tk window
            master = Tk()
            master.title("P")
            # initialize textfield
            text = Text(master, height=len(data.userAnswer), width=len(str(data.userAnswer))//len(data.userAnswer))
            # set default value of textField
            text.insert(END, data.userAnswer)
            # create buttons
            buttonC = Button(master, text="Change", command=retrievePracticeInput)
            buttonExit = Button(master, text="Exit", command=destroy)
            # pack the buttons and text
            buttonExit.pack()
            buttonC.pack()
            text.pack()
# draws text on confirmScreen
def drawConfirmText(canvas, data):
    if data.hyperMode == "calculate":
        # if the operation is add, sub, or multi
        if data.opType == "add" or data.opType == "sub" or data.opType == "multi":
            # draw instruction
            canvas.create_text(data.width/2, 30, text="Confirm your input matrices:", font="Arial 30 bold")
            canvas.create_text(100,50, text="press 'e' to edit", font="Arial 20")
            canvas.create_text(114,70, text="press 'c' to confirm", font="Arial 20")
            canvas.create_text(110,90, text="press 'b' to retake", fill="blue",font="Arial 20")
            # draw the input matrices 1 & 2
            canvas.create_text(data.width/3, 150, text="Matrix #1", font="Arial 50 bold")
            canvas.create_text(data.width/3*2, 150, text="Matrix #2", font="Arial 50 bold")
            # draw matrix 1 row by row
            i = 220
            for rowM1 in data.matrix1:
                canvas.create_text(data.width/3, i, text=str(rowM1), font="Arial 60")
                i += 80
            # draw matrix 2 row by row
            j = 220
            for rowM2 in data.matrix2:
                canvas.create_text(data.width/3*2, j, text=str(rowM2), font="Arial 60")
                j += 80
        # if the operation is not add, sub, or multi
        else:
            # draw instructions
            canvas.create_text(data.width/2, 30, text="Confirm your input matrix:", font="Arial 30 bold")
            canvas.create_text(100,50, text="press 'e' to edit", font="Arial 20")
            canvas.create_text(114,70, text="press 'c' to confirm", font="Arial 20")
            canvas.create_text(110,90, text="press 'b' to retake", fill="blue",font="Arial 20")
            # only draw matrix 1 row by row
            k = 200
            for row in data.matrix1:
                canvas.create_text(data.width/2, k, text=str(row), font="Arial 80")
                k += 100
    elif data.hyperMode == "practice":
            # draw instructions
            canvas.create_text(data.width/2, 30, text="Confirm your input matrix:", font="Arial 30 bold")
            canvas.create_text(100,50, text="press 'e' to edit", font="Arial 20")
            canvas.create_text(114,70, text="press 'c' to confirm", font="Arial 20")
            canvas.create_text(110,90, text="press 'b' to retake", fill="blue",font="Arial 20")
            # only draw matrix 1 row by row
            m = 200
            for row in data.userAnswer:
                canvas.create_text(data.width/2, m, text=str(row), font="Arial 80")
                m += 100
# draw everything on confirmScreen
def confirmScrRedrawAll(canvas, data):
    # draw confirmScreen texts
    drawConfirmText(canvas, data)
####################################
# camScreen mode
####################################
# this function is modified based on opencvTkinter template from 15-112 openCV github page
# added resize feature for the camera image
def opencvToTk(data, frame):
    # Convert an opencv image to a tkinter image, to display in canvas
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # resize the camera image to 640x640
    pil_img = Image.fromarray(rgb_image).resize((1137,640))
    # save the resized image to data
    data.pil_img = pil_img.crop((249,0,889,640))
    tk_image = ImageTk.PhotoImage(image=data.pil_img)
    return tk_image
# keypress events for cameraScreen
def camScrKeyPressed(event, data):
    # print("Releasing camera!")
    # data.camera.release()
    # if 'b' is pressed
    if event.keysym == "b":
        if data.hyperMode == "calculate":
            # go to menuScreen
            data.mode = "menuScr"
        if data.hyperMode == "practice":
            # doesn't need to make a new problem, just switching modes
            data.mode = "showProblem"
    # if 'p' is pressed
    if event.keysym == "p":
        # if the matrix operation is add, sub, or multi
        if data.hyperMode == "calculate":
            if data.opType == "add" or data.opType == "sub" or data.opType == "multi":
                # try recognize matrices 1 & 2
                try:
                    # unset error flags when trying
                    data.errorM1 = False
                    data.errorM2 = False
                    # read matrices 1 & 2 from recog function
                    data.matrix1 = recog("1.jpeg")
                    data.matrix2 = recog("2.jpeg")
                    # for debugging purposes
                    print("matrix1: " + str(data.matrix1))
                    print("matrix2: " + str(data.matrix2))
                    # check if the 2D list read from recog is valid
                    for row1 in range(len(data.matrix1)):
                        cols1 = len(data.matrix1[row1])
                        for col1 in range(cols1):
                            # if there is a tuple in the list
                            if not isinstance(data.matrix1[row1][col1], int):
                                # set error flag for matrix 1
                                data.errorM1 = True
                    # check if the 2D list read from recog is valid
                    for row2 in range(len(data.matrix2)):
                        cols2 = len(data.matrix2[row2])
                        for col2 in range(cols2):
                            # if there is a tuple in the list
                            if not isinstance(data.matrix2[row2][col2], int):
                                # set error flag for matrix 2
                                data.errorM2 = True
                    # for debugging purposes
                    print("errorM1: " + str(data.errorM1))
                    print("errorM2: " + str(data.errorM2))
                    # check error flags, if neither m1 nor m2 has error,
                    if data.errorM1 == False and data.errorM2 == False:
                        # proceed to confirmScreen
                        data.mode = "confirmScr"
                # if recognition fails, update error flags
                except:
                    # set error flag for matrix 1
                    data.errorM1 = True
                    # set error flag for matrix 2
                    data.errorM2 = True
            else:
                # try recognize matrix
                try:
                    # unset error flag
                    data.error = False
                    # read matrix from recognition
                    data.matrix1 = recog("1.jpeg")
                    # for debugging purposes
                    print("matrix1: " + str(data.matrix1))
                    # check if the matrix read from recog is valid
                    for row in range(len(data.matrix1)):
                        cols = len(data.matrix1[row])
                        for col in range(cols):
                            # if there is tuple in the list
                            if not isinstance(data.matrix1[row][col], int):
                                # set the error flag
                                data.error = True
                    # for debugging purposes
                    print(data.error)
                    # if no error
                    if data.error == False:
                        # go to confirmScreen
                        data.mode = "confirmScr"
                # if recognition fails
                except:
                    # set error flag
                    data.error = True
        elif data.hyperMode == "practice":
            # try recognize matrix
            try:
                # unset error flag
                data.error = False
                # read matrix from recognition
                data.userAnswer = recog("1.jpeg")
                # for debugging purposes
                print("matrix: " + str(data.userAnswer))
                # check if the matrix read from recog is valid
                for row in range(len(data.userAnswer)):
                    cols = len(data.userAnswer[row])
                    for col in range(cols):
                        # if there is tuple in the list
                        if not isinstance(data.userAnswer[row][col], int):
                            # set the error flag
                            data.error = True
                # for debugging purposes
                print(data.error)
                # if no error
                if data.error == False:
                    # go to confirmScr
                    data.mode = "confirmScr"
            # if recognition fails
            except:
                # set error flag
                data.error = True
# mouseclick event for cameraScreen
def camScrMousePressed(event, data):
    # record x and y positions of mouseclick
    x = event.x
    y = event.y
    # check if "snap" buttons are clicked based on mouseclick positions
    for i in range(len(data.camRects)):
        # if click inside the button
        if data.camRects[i][0] <= x <= data.camRects[i][2] and \
           data.camRects[i][1] <= y <= data.camRects[i][3]:
            # when the first button is clicked
            if i == 0:
                # save the first camera image to local path
                data.pil_img.save("1.jpeg","jpeg")
                # read the first camera image
                im = cv2.imread("1.jpeg")
                # display the first camera image by opening a new openCV window
                cv2.imshow("Matrix #1", im)
            # when the second button is available and clicked 
            if i == 1 and (data.opType == "add" or data.opType == "sub" or data.opType == "multi"):
                # save the secondcamera image to local path
                data.pil_img.save("2.jpeg","jpeg")
                # read the second camera image
                im = cv2.imread("2.jpeg")
                # display the second camera image by opening a new openCV window
                cv2.imshow("Matrix #2", im)
# Called whenever new camera frames are available.
# Camera frame is available in data.frame. You could, for example, blur the image, and then store that back in data. Then, in drawCamera, draw the blurred frame (or choose not to).
def cameraFired(data):
    # For example, blurring the image.
    # data.frame = cv2.GaussianBlur(data.frame, (11, 11), 0)
    pass
# draw cameraScreen texts
def drawCamText(canvas, data):
    # draw instructions
    canvas.create_text(data.width/2, 55, text="Make sure lighting condition is good and digits are clearly visible", font="Arial 15")
    if data.hyperMode == "calculate":
        canvas.create_text(104, 20, text="Press 'b' to go back to menu", font="Arial 15")
    if data.hyperMode == "practice":
        canvas.create_text(112, 20, text="Press 'b' to go back to problem", font="Arial 15")
    canvas.create_text(76, 40, text="Press 'p' to proceed", font="Arial 15")
    # draw text corresponding to the buttons
    for i in range(len(data.camRects)):
        x = (data.camRects[i][0] + data.camRects[i][2]) / 2
        y = (data.camRects[i][1] + data.camRects[i][3]) / 2
        # for the first button
        if i == 0:
            # draw "snap it" text
            canvas.create_text(x, y, text="Snap it!", font="Arial 20")
        # for the second button
        if i == 1 and data.hyperMode == "calculate" and (data.opType == "sub" or data.opType == "add" or data.opType == "multi"):
            # only draw text it if the operation type is sub, add, or multi
            canvas.create_text(x, y, text="Second Matrix", font="Arial 15")
# draw buttons on the cameraScreen
def drawCamButtons(canvas, data):
    # the list contains tuples of positions of buttons as rectangles on canvas
    data.camRects = [(180,40,280,70),(720,40,820,70)]
    # for every button
    for i in range(len(data.camRects)):
        # for the first button
        if i == 0:
            # draw it
            canvas.create_rectangle(data.camRects[i], fill="white", width=2)
        # for the second button
        if i == 1 and data.hyperMode == "calculate" and (data.opType == "add" or data.opType == "sub" or data.opType == "multi"):
            # only draw it if the operation type is add, sub, or multi
            canvas.create_rectangle(data.camRects[i], fill="white", width=2)
# draw error messages on cameraScreen
def drawErrorMessage(canvas, data):
    if data.hyperMode == "calculate":
        # if there are two input matrices
        if data.opType == "add" or data.opType == "sub" or data.opType == "multi":
            # if recog for matrix 1 fails
            if data.errorM1 == True:
                # draw error message
                canvas.create_text(data.width/2, 15, text="M1 recognition failed! Please retake M1.", fill="red", font="Arial 15")
            # if recog for matrix 2 fails
            if data.errorM2 == True:
                # draw error message
                canvas.create_text(data.width/2, 35, text="M2 recognition failed! Please retake M2.", fill="red", font="Arial 15")
        # if there is one input matrix
        else:
            # if recog for matrix fails
            if data.error == True:
                # draw error message
                canvas.create_text(data.width/2, 25, text="Recognition failed! Please retake photo.", fill="red", font="Arial 15")
    elif data.hyperMode == "practice":
        if data.error == True:
            # draw error message
            canvas.create_text(data.width/2, 25, text="Recognition failed! Please retake photo.", fill="red", font="Arial 15")# draw the camera image on canvas
def drawCamera(canvas, data):
    # import the image from camera frame in data
    data.tk_image = opencvToTk(data, data.frame)
    canvas.create_image(data.width/2, data.height/2, image=data.tk_image)
# draw everything on cameraScreen
def camScrRedrawAll(canvas, data):
    # draw error message, if applicable
    drawErrorMessage(canvas, data)
    # draw cameraScreen buttons
    drawCamButtons(canvas, data)
    # draw cameraScreen texts
    drawCamText(canvas, data)
    # draw the camera frame
    drawCamera(canvas, data)
#################################################
# this run function is modified based on openCVTkinter template from 15-112 openCV github
# this function is edited to support multiple pages
#################################################
def run(width=300, height=300):
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    # initialize camera index, default value is 0
    data.camera_index = 0
    data.timer_delay = 100 # ms
    data.redraw_delay = 50 # ms
    # initialize all data fields, including the camera
    init(data)
    # Make tkinter window and canvas
    data.root = Tk()
    data.root.title("Matrix Calculator")
    canvas = Canvas(data.root, width=data.width, height=data.height)
    canvas.pack()
    # Basic bindings. Note that only timer events will redraw.
    data.root.bind("<Button-1>", lambda event: mousePressed(event, data))
    data.root.bind("<Key>", lambda event: keyPressed(event, data))
    # Timer fired needs a wrapper. This is for periodic events.
    def timerFiredWrapper(data):
        # Ensuring that the code runs at roughly the right periodicity
        start = time.time()
        # timerFired(data)
        end = time.time()
        diff_ms = (end - start) * 1000
        delay = int(max(data.timer_delay - diff_ms, 0))
        data.root.after(delay, lambda: timerFiredWrapper(data))
    # Wait a timer delay before beginning, to allow everything else to
    # initialize first.
    data.root.after(data.timer_delay, 
        lambda: timerFiredWrapper(data))
    # wrapper for redrawAll function
    def redrawAllWrapper(canvas, data):
        start = time.time()
        # Get the camera frame and get it processed.
        _, data.frame = data.camera.read()
        cameraFired(data)
        # Redrawing code
        canvas.delete(ALL)
        redrawAll(canvas, data)
        # Calculate delay accordingly
        end = time.time()
        diff_ms = (end - start) * 1000
        # Have at least a 5ms delay between redraw. Ideally higher is better.
        delay = int(max(data.redraw_delay - diff_ms, 5))
        data.root.after(delay, lambda: redrawAllWrapper(canvas, data))
    # Start drawing immediately
    data.root.after(0, lambda: redrawAllWrapper(canvas, data))
    # Loop tkinter
    data.root.mainloop()
# run it all!
if __name__ == "__main__":
    run(1000, 800)