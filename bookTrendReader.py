"""
Python backend for Machine Learning project 1

@author: Joshua Engelsma
"""

import sys
import os

class TrendReader(object):

	def __init__(self, dataFile):
		self.dataFile = dataFile
		self.fileLines = []
		self.slope = 0
		self.intercept = 0
		self.predictedValues = []

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
			sumXsquared += (hour * hour)
			sumYsquared += (downloads * downloads)
		nbrOfValues = len(self.fileLines) - nbrOfNans
		# calculate the slope
		slope = (1.0 * ((nbrOfValues * sumXYpairs) - (sumXvalues * sumYvalues))) / (1.0 * ((nbrOfValues * sumXsquared) - (sumXsquared)))
		# calculate the y intercept
		intercept = (1.0 * (sumYvalues - (slope * sumXvalues))) / (1.0 * nbrOfValues)

		# assign to the instance
		self.slope = slope
		self.intercept = intercept
		print("\ny = {}x + {}\n".format(slope, intercept))

	def generatePredictedValues(self):
		"""
		@summary: method to generate the predicted values in our linear regression
		"""
		for hourIndex in range(1, self.dataFile + 1):
			predictedValue = self.slope * hourIndex + self.intercept
			self.predictedValues.append(predictedValue)

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
	# gather predicted values based upon our linear regression
	reader.generatePredictedValues()


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
