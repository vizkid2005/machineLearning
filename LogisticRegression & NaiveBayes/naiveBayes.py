#!/usr/bin/python
import sys
import csv
import math

trainingSetFileName="zoo-trainSimplified.csv"
testSetFileName="zoo-testSimplified.csv"
numFeatures=-1
classIndex=-1

#this method is used to read the csv file and save it in a list of lists.
def readData(fileName):
	data = []
	myFile = open(fileName, 'r')
	try:
		reader = csv.reader(myFile)
		for row in reader:
			data.append(row)
	except:
		print "Error opening File: "+fileName
		exit()
	finally:
		myFile.close()
	return data	

#w is the weight vector
#row is a sample
def predictLabel(row):
#TODO
	return "1"
'''
	#computing dot product here
	for i in range(numFeatures):
		dotProduct+=(w[i]*row[i])
	if dotProduct >= 0:
		return "1"
	return "0"
'''

#inputFileName - file name of the test set
# w is the weight vector.
#outputFileName - file name for the output.
#consider 1 as + 
# ans o as -ve
def handleTestData(inputFileName,w,outputFileName):
	tp=0
	fp=0
	tn=0
	fn=0
	samples=readData(inputFileName)
	totalCount=len(samples)
	if totalCount <=0:
		print "Test data set is empty"
		exit()
	print "Printing (actual, predicted)"
	for row in samples:
		pLabel = predictLabel(row)
		aLabel = row[classIndex] 
		print aLabel,pLabel
		if(aLabel=="1"):
			if(pLabel=="1"):
				tp+=1
			else:
				fn+=1			
		else:
			if (pLabel=="1"):
				fp+=1
			else:
				tn+=1
				
	print "Total True positives is ",tp
	print "Total True Negatives is ",tn
	print "Total False Positives is ",fp
	print "Total False Negatives is ",fn

def main():

	trainingSet=readData(trainingSetFileName)
	if len(trainingSet) <=0:
		print "No data in training set"
		exit()

	numFeatures=len(trainingSet[0])-1
	classIndex=numFeatures

	
#Execution begins here
if __name__ == "__main__" : main()	
