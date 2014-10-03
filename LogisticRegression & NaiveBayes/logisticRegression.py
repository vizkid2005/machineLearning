#!/usr/bin/python
import sys
import csv
import math

trainingSetFileName="zoo-trainSimplified.csv"
testSetFileName="zoo-testSimplified.csv"
numFeatures=-1
classIndex=-1
learningRate=0.5


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
#x is the feature vecotor
#returns 1/(1+exp(w.x))
def maxLikelyHood(w,x):
	dotProduct=0
	for i in range(0,numFeatures):
		dotProduct+=(w[i]*x[i])
	return float(1)/(1+math.exp(dotProduct))

def main():

	trainingSet=readData(trainingSetFileName)
	if len(trainingSet) <=0:
		print "No data in training set"
		exit()

	numFeatures=len(trainingSet[0])-1
	classIndex=numFeatures

	#initialize the weight vector to be 0's
	weightVector = [0 for i in range(0,numFeatures)]	
		
	while True: #whats the condition to break???
		gradientVector = [0 for i in range(0,numFeatures)]
		for sample in trainingSet:
			error = float(sample[classIndex]) - maxLikelyHood(weightVector,sample)
			for j in range(0,numFeatures):
				gradientVector[j]+=gradientVector[j]+error*float(sample[j])
				weightVector[j]+=learningRate*gradientVector[j]				
		print weightVector
		break #for now...
		
#Execution begins here
if __name__ == "__main__" : main()	
