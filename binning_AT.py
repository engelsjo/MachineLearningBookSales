"""
Python backend for Machine Learning project 1
Binning into days, weeks, and time of day

@author: Adam Terwilliger
"""

import sys
import os
import numpy as np


np.set_printoptions(threshold='nan')

file = "downloads.txt"

fileLines = []

with open(file) as fh:
	for i, line in enumerate(fh):
		line = line.strip()
		lineParts = line.split(',')
		downloads = lineParts[1]
		if downloads != "nan":
			downloads = int(downloads)
		else:
			downloads = 0
		fileLines.append(downloads)
		
#print fileLines

downloadArray = np.empty([len(fileLines),2]).astype(int)




def binning(mod, mod2, mod3):
	for hour, downloads in enumerate(fileLines):
		downloadArray[hour] = int(hour % mod / mod2 % mod3), downloads
		#print downloadArray[hour]

	binCountArray = np.bincount(downloadArray[:,0])
	binnedArray = np.bincount(downloadArray[:,0],weights=downloadArray[:,1])
	
	print binCountArray
	print binnedArray
	
	return binnedArray / binCountArray

print binning(24, 1, len(fileLines))

print binning(len(fileLines), 24, len(fileLines))

print binning(len(fileLines), 24, 7)
'''

class TrendReader(object):

	def __init__(self, dataFile):
		self.dataFile = dataFile
		self.fileLines = []
		self.nbrOfNans = 0
		self.nanIndices = []
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
		self.predictedLinearValues = []
		degree = 1
		coefficients = self.generatePolynomialRegression(degree, self.fileLines)
		for hourIndex in range(1, len(self.fileLines) + 1):
			predictedValue = coefficients[0] * hourIndex + coefficients[1]
			self.predictedLinearValues.append(predictedValue)

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

	def generateAvgPredictedValues(self):
		"""
		@summary: method to generate an average of the cubic and linear function
		"""
		self.cubicAndLinearAvgValues = []
		self.generateLinearPredictedValues()
		self.generateCubicPredictedValues()
		for x in range(len(self.predictedLinearValues)):
			linearVal = self.predictedLinearValues[x]
			cubicVal = self.predictedCubicValues[x]
			avgVal = (linearVal + cubicVal) / 2.0
			self.cubicAndLinearAvgValues.append(avgVal)

	def generateNanPredictedValues(self):
		"""
		@summary: method to generate the predicted values of the nan points
		"""
		self.nanPredictedValues = {}
		self.generateAvgPredictedValues()
		for nanXValue in self.nanIndices:
			self.nanPredictedValues[nanXValue + 1] = self.cubicAndLinearAvgValues[nanXValue]

	def getLinearPredictedValues(self):
		return self.predictedLinearValues

	def getCubicPredictedValues(self):
		return self.predictedCubicValues

	def getAvgPredictedValues(self):
		return self.cubicAndLinearAvgValues

	def getNanPredictedValues(self):
		return self.nanPredictedValues


	def binning(self):
		

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
	# create a linear regression from our data - prints out the equation
	reader.generateLinearRegression()
	# create a cubic regression from our data - prints out the equation
	reader.generateCubicRegression()
	# get the points for our nan coords
	reader.generateNanPredictedValues()
	# print(reader.nanPredictedValues)


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

'''
