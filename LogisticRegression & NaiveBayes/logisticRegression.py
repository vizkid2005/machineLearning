#!/usr/bin/python
import sys
import csv
import math

trainingSetFileName="zoo-trainSimplified.csv"
testSetFileName="zoo-testSimplified.csv"
numFeatures=-1
classIndex=-1
learningRate=math.exp(5)
threshold = math.exp(50)

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
	weightVectorBackUp = [0 for i in range(0,numFeatures)]		
	iterations=0

	while True: 
		iterations+=1
		gradientVector = [0 for i in range(0,numFeatures)]
		for sample in trainingSet:
			error = float(sample[classIndex]) - maxLikelyHood(weightVector,sample)
			for j in range(0,numFeatures):
				gradientVector[j]+=gradientVector[j]+error*float(sample[j])
				weightVector[j]+=learningRate*gradientVector[j]				
						
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

	print weightVector
	print "Number of Iterations "+str(iterations) 

#Execution begins here
if __name__ == "__main__" : main()	
