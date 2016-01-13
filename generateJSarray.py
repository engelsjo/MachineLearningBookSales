'''
 @Title Machine Learning Project # 1
 @Description: program to analyze data from book sales, and make predictions
 @Authors: Michael Baldwin, Josh Engelsma, Adam Terwilliger
 @Date: January 13, 2016
 @Version 1.0
'''

# @return list of lists
def readFile(textFile):
    with open(textFile, 'rb') as file:
        data = list()
        for line in file:
            tokens = line.strip('\n').split(',')
            # ignore NANs for now
            try:
                data.append(map(int, tokens))
            except Exception, e:
                continue
    return data

# dataArray is list of lists
def writeFile(javascriptFile, dataArray):
    with open(javascriptFile, 'wb') as file:
        file.write('var dataset = [\n')
        numItems = len(dataArray)
        for index, value in enumerate(dataArray):
            if index < numItems - 1:
                file.write(str(value) + ',\n')
            else:
                file.write(str(value) + '\n')
        file.write('];\n')

def generateArray(textFile, javascriptFile):
    writeFile(javascriptFile, readFile(textFile))

def main():
    textFile = 'downloads.txt'
    javascriptFile = 'dataset.js'
    generateArray(textFile, javascriptFile)

if __name__ == '__main__':
    main()
