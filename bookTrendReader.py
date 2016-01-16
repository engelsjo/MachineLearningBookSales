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

	def generateLinearRegression(self):
		"""
		@summary: method to generate a linear regression from our data
		"""
		sumXvalues = sumYvalues = sumXYpairs = sumXsquared = sumYsquared = 0
		for hour, downloads in enumerate(self.fileLines):
			if downloads == "nan": continue
			sumXvalues += hour
			sumYvalues += downloads
			sumXYpairs += (hour * downloads)
			sumXsquared += pow(hour, 2)
			sumYsquared += pow(downloads, 2)
		nbrOfValues = len(self.fileLines) - self.nbrOfNans
		# calculate the slope
		slope = (1.0 * ((nbrOfValues * sumXYpairs) - (sumXvalues * sumYvalues))) / (1.0 * ((nbrOfValues * sumXsquared) - (sumXsquared)))
		# calculate the y intercept
		intercept = (1.0 * (sumYvalues - (slope * sumXvalues))) / (1.0 * nbrOfValues)

		# assign to the instance
		self.linearCoefficients["slope"] = slope
		self.linearCoefficients["intercept"] = intercept
		print("\nLinear Regression:\ny = {}x + {}\n".format(slope, intercept))

	def generateCubicRegression(self):
		"""
		@summary: method to generate a cubic regression from our data
		"""
		xSummations = [0, 0, 0, 0, 0, 0]
		xySummations = [0, 0, 0, 0]

		for hour, downloads in enumerate(self.fileLines):
			if downloads == "nan": continue
			for exponent in range(1, 7): xSummations[exponent - 1] += pow(hour, exponent)
			for exponent in range(0, 4): xySummations[exponent] += pow(hour, exponent) * downloads	
		nbrOfValues = len(self.fileLines) - self.nbrOfNans

		# build coefficient matrix
		coeffMatrix = []
		for row in range(4):
			matrixRow = []
			for col in range(4):
				if row == 3 and col == 3: matrixRow.append(nbrOfValues)
				else: matrixRow.append(xSummations[5 - row - col])
			coeffMatrix.append(matrixRow)

		# build the answers matrix
		answeMatrix = []
		for row in range(4):
			rowMatrix = [xySummations[3 - row]]
			answeMatrix.append(rowMatrix)

		# use numpy to solve the matrix equation, and store off our data
		resultsMatrix = np.linalg.solve(np.array(coeffMatrix), np.array(answeMatrix))
		keys = ["cubicCoeff", "squaredCoeff", "xCoeff", "intercept"]
		for i in range(4):
			self.cubicCoefficients[keys[i]] = resultsMatrix[i][0]
		print("\nCubic Regression:\ny = {}x^3 + {}x^2 + {}x + {}\n".format(resultsMatrix[0][0], resultsMatrix[1][0], resultsMatrix[2][0], resultsMatrix[3][0]))


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
