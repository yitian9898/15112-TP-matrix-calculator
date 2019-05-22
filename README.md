Overview of Matrix Calculator:

Matrix calculator has two modes: calculation and practice. The calculation mode allows the user to select a matrix operation from the menu screen, take a picture of the matrix, confirm or edit the input matrix, and get the result of the operation. The practice mode allows the user to select a matrix operation to practice with. It shows the user the matrices to solve in the order of increasing difficulty levels. Depending on the type of operation, the user can either take a picture of the matrix to confirm the results, or the user can directly type the matrix in. If the user has a wrong result of computation, the program will keep presenting problems of the same difficulty level until the user has it correct. The program will then progress to the next difficulty level. The “reinforcement learning” feature gives the user ample amount of practice so that the user will become proficient matrix solvers.

Mac Installation Guide:

1. install openCV2
	#1, open mac terminal
	#2, install homebrew by copying & pasting the following into the terminal:

		ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

	#3, install openCV after homebrew is installed successfully by copying the following into the terminal:

		brew tap homebrew/science
		brew install opencv

2. install numpy
	#1, open mac terminal
	#2, install numpy by copying & pasting the following into the terminal:

		pip install numpy

3. install sklearn
	#1, open mac terminal
	#2, install sklearn by copying & pasting the following into the terminal:

		pip install sklearn

4. install skimage
	#1, open mac terminal
	#2, install skimage by copying & pasting the following into the terminal:

		pip install scikit-image

5. check shell configuration and make sure that the shell is running python 2.7 version

How-to-run:

1. open “opencvTkinter.py” in the file directory
2. press “command” & “shift” & “e” to run the file as a script

Important Notes:
	When capturing the matrix with the webcam, write down the matrix (ideally with a sharpie) on a piece of white paper and make sure there is only the matrix in the camera frame. The recognition performance is optimal when there is no shadow, no paper wrinkle, no paper edge, and no other objects in the frame. See sample.jpeg in the file directory for a sample photo that can be easily recognized by the system.
