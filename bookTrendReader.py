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

		self.slope = 0
		self.intercept = 0

		self.nanIndices = []
		self.linearCoefficients = {}
		self.cubicCoefficients = {}
		self.predictedLinearValues = []
		self.predictedQuadraticValues = []
		self.predictedCubicValues = []
		self.cubicAndLinearAvgValues = []
		self.nanPredictedValues = {}

	def readDataFile(self):
		"""
		@summary: read in lines from downloads.txt into self.dataFile
		"""
		with open(self.dataFile) as fh:
			for i, line in enumerate(fh):
				line = line.strip()
				lineParts = line.split(',')
				downloads = lineParts[1]
				if downloads != "nan":
					downloads = int(downloads)
				else:
					self.nbrOfNans += 1
					self.nanIndices.append(i)
				self.fileLines.append(downloads)

	def generateSimpleLinearRegression(self):
		sumXvalues = sumYvalues = sumXYpairs = sumXsquared = sumYsquared = nbrOfNans = 0
		for hour, downloads in enumerate(self.fileLines):
			if downloads == "nan":
				nbrOfNans += 1
				continue
			hour += 1
			sumXvalues += hour
			sumYvalues += downloads
			sumXYpairs += (hour * downloads)
			sumXsquared += (hour * hour)
			sumYsquared += (downloads * downloads)

		nbrOfValues = len(self.fileLines) - nbrOfNans

		cov1 = nbrOfValues * sumXYpairs
		cov2 = sumXvalues * sumYvalues
		var1 = nbrOfValues * sumXsquared
		var2 = sumXvalues * sumXvalues

		covXY = cov1 - cov2
		varX = var1 - var2

		slope = float(covXY) / float(varX)

		intercept = (float(sumYvalues) - (slope * float(sumXvalues))) / float(nbrOfValues)

		# assign to the instance
		self.slope = slope
		self.intercept = intercept
		print("Linear Regression calculated by hand: ")
		print("\ny = {}x + {}\n".format(slope, intercept))

	def generatePolynomialRegression(self, degree, data):
		"""
		@param degree: the integer degree
		@param data: a list of file lines where each line is a comma separated x y coord
		@return: a list of coefficients
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
		print("\nLinear Regression using Matrix Solver:\ny = {}x + {}\n".format(coefficients[0], coefficients[1]))

	def generateQuadraticRegression(self):
		"""
		@summary: method to generate a linear regression from our data
		"""
		degree = 2
		coefficients = self.generatePolynomialRegression(degree, self.fileLines)
		print("\nQuadratic Regression using Matrix Solver:\ny = {}x^2 + {}x + {}\n".format(coefficients[0], coefficients[1], coefficients[2]))

	def generateCubicRegression(self):
		"""
		@summary: method to generate a cubic regression from our data
		"""
		degree = 3
		cubicCoefficients = self.generatePolynomialRegression(degree, self.fileLines)
		print("\nCubic Regression using Matrix Solver:\ny = {}x^3 + {}x^2 + {}x + {}\n".format(cubicCoefficients[0], cubicCoefficients[1], cubicCoefficients[2], cubicCoefficients[3]))

	def generateLinearPredictedValues(self):
		"""
		@summary: method to generate the predicted values in our linear regression
		"""
		self.predictedLinearValues = []
		degree = 1
		coefficients = self.generatePolynomialRegression(degree, self.fileLines)
		for hourIndex in range(1, len(self.fileLines) + 1):
			predictedValue = coefficients[0] * hourIndex + coefficients[1]
			self.predictedLinearValues.append(predictedValue)

	def generateQuadraticPredictedValues(self):
		"""
		@summary: method to generate the predicted values in our quadratic regression
		"""
		self.predictedQuadraticValues = []
		degree = 2
		coefficients = self.generatePolynomialRegression(degree, self.fileLines)
		for hourIndex in range(1, len(self.fileLines) + 1):
		    predictedValue = coefficients[0] * pow(hourIndex, 2) + coefficients[1] * hourIndex + coefficients[2]
		    self.predictedQuadraticValues.append(predictedValue)

	def generateCubicPredictedValues(self):
		"""
		@summary: method to generate the predicted values in our cubic regression model
		"""
		self.predictedCubicValues = []
		degree = 3
		coefficients = self.generatePolynomialRegression(degree, self.fileLines)
		for hourIndex in range(1, len(self.fileLines) + 1):
			predictedValue = coefficients[0] * pow(hourIndex, 3) + coefficients[1] * pow(hourIndex, 2) + coefficients[2] * pow(hourIndex, 1) + coefficients[3]
			self.predictedCubicValues.append(predictedValue)

	def generateNanPredictedValues(self):
		"""
		@summary: method to generate the predicted values of the nan points
		"""
		self.generateQuadraticPredictedValues()
		self.nanPredictedValues = {}
		for nanXValue in self.nanIndices:
			self.nanPredictedValues[nanXValue + 1] = self.predictedQuadraticValues[nanXValue]

	def printNanValues(self):
		dataSet = "var nans = [\n"
		for key in self.nanPredictedValues.keys():
			value = self.nanPredictedValues[key]
			dataSet += "[{}, {}],\n".format(str(key), value)
		# trim off the last comma
		dataSet = dataSet[:-2]
		dataSet += "\n];"
		with open("nansData.js", "w") as fh:
			fh.write(dataSet)

	def getLinearPredictedValues(self):
		return self.predictedLinearValues

	def getQuadraticPredictedValues(self):
		return self.predictedQuadraticValues
	
	def getCubicPredictedValues(self):
		return self.predictedCubicValues

	def getAvgPredictedValues(self):
		return self.cubicAndLinearAvgValues

	def getNanPredictedValues(self):
		return self.nanPredictedValues

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

	reader.generateSimpleLinearRegression()
	# create a linear regression from our data - prints out the equation
	reader.generateLinearRegression()
	# create a quad regresssion
	reader.generateQuadraticRegression()
	# create a cubic regression from our data - prints out the equation
	reader.generateCubicRegression()
	# get the points for our nan coords
	reader.generateNanPredictedValues()
	# format the nan values
	reader.printNanValues()


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
