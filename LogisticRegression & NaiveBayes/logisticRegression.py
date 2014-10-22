#!/usr/bin/python
import sys
import csv
import math

trainingSetFileName="zoo-train.csv"
testSetFileName="zoo-test.csv"
numFeatures=-1
classIndex=-1
learningRate=0.0001
threshold   =0.001
classLabelToCompare="1"

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
def predictLabel(row,w):
	global numFeatures	
	#computing dot product here
	dotProduct=0
	for i in range(numFeatures):
		dotProduct+=(w[i]*long(row[i]))
		
	if dotProduct >= 0:
		   return "1"
	return "0"



#inputFileName - file name of the test set
# w is the weight vector.
#outputFileName - file name for the output.
#consider 1 as + 
# ans o as -ve
def handleTestData(inputFileName,w,outputFileName):
	global numFeatures
	global classIndex
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
		pLabel = predictLabel(row,w)
		aLabel = row[classIndex] 
		print aLabel,pLabel
		if(aLabel==classLabelToCompare):
			if(pLabel==classLabelToCompare):
				tp+=1
			else:
				fn+=1			
		else:
			if (pLabel==classLabelToCompare):
				fp+=1
			else:
				tn+=1
				
	print "Total True positives is ",tp
	print "Total True Negatives is ",tn
	print "Total False Positives is ",fp
	print "Total False Negatives is ",fn

#w is the weight vector
#x is the feature vecotor
#returns 1/(1+exp(w.x))
def maxLikelyHood(w,x):
	global numFeatures
	dotProduct=0
	for i in range(0,numFeatures):
		dotProduct-=(w[i]*long(x[i]))	#note the minus sign here...
	#print math.exp(dotProduct)
	return long(1)/(1+math.exp(dotProduct))
	#return 0
	
def main():
	#define global variables...
	global numFeatures
	global trainingSetFileName
	global testSetFileName
	global numFeatures
	global classIndex
	global learningRate
	global threshold
	
	#read the training file.
	trainingSet=readData(trainingSetFileName)
	if len(trainingSet) <=0:
		print "No data in training set"
		exit()

	numFeatures=len(trainingSet[0])-1
	classIndex=numFeatures
	
	#prune datasets...
	for i in range(len(trainingSet)):
		if trainingSet[i][classIndex]!=classLabelToCompare:
			trainingSet[i][classIndex]="0" #replace all other class labels with 0

	#initialize the weight vector to be 0's
	weightVector = [0 for i in range(0,numFeatures)]	
	weightVectorBackUp = [0 for i in range(0,numFeatures)]		
	iterations=0

	while True: 
		iterations+=1
		gradientVector = [0 for i in range(0,numFeatures)]
		for sample in trainingSet:
			error = long(sample[classIndex]) - maxLikelyHood(weightVectorBackUp,sample)
			for j in range(0,numFeatures):
				gradientVector[j]+=error*long(sample[j])
		
		#update weight vector..
		for j in range(numFeatures):		
			weightVector[j]+=learningRate*gradientVector[j]				
		#print weightVector
		#check whether the increment in weight vector is greater than the "threshold" for every feature...		
		shouldBreak=True
		for i in range(numFeatures):
			if math.fabs(weightVector[i] - weightVectorBackUp[i]) > threshold:
				shouldBreak=False		
			
		if shouldBreak==True:
			break
		else:
			#take a backup of the weight vector...
			weightVectorBackUp = [weightVector[i] for i in range(numFeatures)]

	print "Final weight Vector is"
	print weightVector
	print "Number of Iterations it took for converging "+str(iterations) 
	
	#evaluating the test data...
	print "Evaluating the Test data..."
	handleTestData(testSetFileName,weightVector,"LR-results/ouput.csv")
	
#Execution begins here
if __name__ == "__main__" : main()	
