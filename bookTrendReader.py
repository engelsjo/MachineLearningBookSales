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
		self.slope = 0
		self.intercept = 0
		self.predictedLinearValues = []
		self.predictedCubicValues = []

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
				self.fileLines.append(downloads)

	def generateLinearRegression(self):
		"""
		@summary: method to generate a linear regression from our data
		"""
		sumXvalues = sumYvalues = sumXYpairs = sumXsquared = sumYsquared = nbrOfNans = 0
		for hour, downloads in enumerate(self.fileLines):
			if downloads == "nan":
				nbrOfNans += 1
				continue
			sumXvalues += hour
			sumYvalues += downloads
			sumXYpairs += (hour * downloads)
			sumXsquared += pow(hour, 2)
			sumYsquared += pow(downloads, 2)
		nbrOfValues = len(self.fileLines) - nbrOfNans
		# calculate the slope
		slope = (1.0 * ((nbrOfValues * sumXYpairs) - (sumXvalues * sumYvalues))) / (1.0 * ((nbrOfValues * sumXsquared) - (sumXsquared)))
		# calculate the y intercept
		intercept = (1.0 * (sumYvalues - (slope * sumXvalues))) / (1.0 * nbrOfValues)

		# assign to the instance
		self.slope = slope
		self.intercept = intercept
		print("\nLinear Regression:\ny = {}x + {}\n".format(slope, intercept))

	def generateCubicRegression(self):
		"""
		@summary: method to generate a cubic regression from our data
		"""
		sumX6Values = sumX5Values = sumX4Values = sumX3Values = sumX2Values = sumX1Values = sumX2Y1Values = sumX3Y1Values = sumX1Y1Values = sumY1Values = nbrOfNans = 0
		for hour, downloads in enumerate(self.fileLines):
			if downloads == "nan":
				nbrOfNans += 1
				continue
			sumX1Values += hour
			sumX2Values += pow(hour, 2)
			sumX3Values += pow(hour, 3)
			sumX4Values += pow(hour, 4)
			sumX5Values += pow(hour, 5)
			sumX6Values += pow(hour, 6)
			sumX3Y1Values += pow(hour, 3) * downloads
			sumX2Y1Values += pow(hour, 2) * downloads
			sumX1Y1Values += hour * downloads
			sumY1Values += downloads
		nbrOfValues = len(self.fileLines) - nbrOfNans

		# build matrices to calculate the 4 coefficients
		coeffMatrix = [
						[sumX6Values, sumX5Values, sumX4Values, sumX3Values],
						[sumX5Values, sumX4Values, sumX3Values, sumX2Values],
						[sumX4Values, sumX3Values, sumX2Values, sumX1Values],
						[sumX3Values, sumX2Values, sumX1Values, nbrOfValues]
					  ]
		answeMatrix = [
						[sumX3Y1Values],
						[sumX2Y1Values],
						[sumX1Y1Values],
						[sumY1Values]
					  ]

		resultsMatrix = np.linalg.solve(np.array(coeffMatrix), np.array(answeMatrix))
		print("\nCubic Regression:\ny = {}x^3 + {}x^2 + {}x + {}\n".format(resultsMatrix[0][0], resultsMatrix[1][0], resultsMatrix[2][0], resultsMatrix[3][0]))


	def generateLinearPredictedValues(self):
		"""
		@summary: method to generate the predicted values in our linear regression
		"""
		for hourIndex in range(1, len(self.fileLines) + 1):
			predictedValue = self.slope * hourIndex + self.intercept
			self.predictedLinearValues.append(predictedValue)

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
