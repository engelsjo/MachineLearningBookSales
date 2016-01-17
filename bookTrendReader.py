"""
Python backend for Machine Learning project 1

@author: Joshua Engelsma
"""

import sys
import os
import numpy as np

class TrendReader(object):

	def __init__(self, dataFile):
		self.dataFile = dataFile
		self.fileLines = []
		self.nbrOfNans = 0
		self.linearCoefficients = {}
		self.cubicCoefficients = {}
		self.predictedLinearValues = []
		self.predictedCubicValues = []
		self.cubicAndLinearAvgValues = []
		self.nanPredictedValues = {}

	def readDataFile(self):
		"""
		@summary: read in lines from downloads.txt into self.dataFile
		"""
		with open(self.dataFile) as fh:
			for line in fh:
				line = line.strip()
				lineParts = line.split(',')
				downloads = lineParts[1]
				if downloads != "nan":
					downloads = int(downloads)
				else:
					self.nbrOfNans += 1
				self.fileLines.append(downloads)

	def generatePolynomialRegression(self, degree, data):
		"""
		@param degree: the integer degree
		@param data: a list of file lines where each line is a comma separated x y coord
		Method that returns the coefficients of the n degree polynomial 
		"""
		xSummations = [0] * degree * 2
		xySummations = [0] * (degree + 1)
		nbrOfNans = 0
		for hour, downloads in enumerate(data):
			if downloads == "nan": 
				nbrOfNans += 1
				continue
			for exponent in range(1, len(xSummations) + 1): xSummations[exponent - 1] += pow(hour, exponent)
			for exponent in range(degree + 1): xySummations[exponent] += pow(hour, exponent) * downloads
		nbrOfValues = len(data) - nbrOfNans

		# build coefficent matrix
		coeffMatrix = []
		for row in range(degree + 1):
			matrixRow = []
			for col in range(degree + 1):
				if row == degree and col == degree: matrixRow.append(nbrOfValues)
				else: matrixRow.append(xSummations[len(xSummations) - 1 - row - col])
			coeffMatrix.append(matrixRow)

		# build the answers matrix
		answeMatrix = []
		for row in range(degree + 1):
			rowMatrix = [xySummations[len(xySummations) - 1 - row]]
			answeMatrix.append(rowMatrix)

		# use numpy to solve the matrix equation, and store off our data
		resultsMatrix = np.linalg.solve(np.array(coeffMatrix), np.array(answeMatrix))
		finalRetVal = [resultsMatrix[i][0] for i in range(degree + 1)]
		return finalRetVal

	def generateLinearRegression(self):
		"""
		@summary: method to generate a linear regression from our data
		"""
		degree = 1
		coefficients = self.generatePolynomialRegression(degree, self.fileLines)
		print("\nLinear Regression:\ny = {}x + {}\n".format(coefficients[0], coefficients[1]))

	def generateCubicRegression(self):
		"""
		@summary: method to generate a cubic regression from our data
		"""
		degree = 3
		cubicCoefficients = self.generatePolynomialRegression(degree, self.fileLines)
		print("\nCubic Regression:\ny = {}x^3 + {}x^2 + {}x + {}\n".format(cubicCoefficients[0], cubicCoefficients[1], cubicCoefficients[2], cubicCoefficients[3]))

	def generateLinearPredictedValues(self):
		"""
		@summary: method to generate the predicted values in our linear regression
		"""
		for hourIndex in range(1, len(self.fileLines) + 1):
			predictedValue = self.slope * hourIndex + self.intercept
			self.predictedLinearValues.append(predictedValue)

	def generateCubicPredictedValues(self):
		"""
		@summary: method to generate the predicted values in our cubic regression model
		"""
		for hourIndex in range(1, len(self.fileLines) + 1):
			predictedValue = 0

	def getLinearPredictedValues(self):
		return self.predictedLinearValues

def main(argv):
	"""
	@param argv: a python list of command line arguments
	@summary: Main driver for the program
	"""
	# verify we have command line args passed
	if len(argv) != 2:
		print(usage())
		sys.exit(1)

	# verify that a valid file was passed
	if not os.path.isfile(argv[1]):
		print(usage())
		sys.exit(2)

	# init our model
	reader = TrendReader(argv[1])
	# read in our data
	reader.readDataFile()
	# create a linear regression from our data
	reader.generateLinearRegression()
	# create a cubic regression from our data
	reader.generateCubicRegression()
	


def usage():
	"""
	@summary: print out instructions regarding command line operation
	"""
	return """
	BOOK TREND READER

	Args:
		1.) FilePath - the path to the data file of the hours last month
	Exit Codes:
		0.) Success
		1.) Invalid Number of command line arguments
		2.) You failed to pass a file name on the command line.
	"""

if __name__ == "__main__":
	main(sys.argv)
