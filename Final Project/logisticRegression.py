#!/usr/bin/python
import sys
import csv
import math

learningRate=1
threshold   =0.01

#w is the weight dictionary
#row is a sample
def predictLabel(row,w):
	global numFeatures	
	#computing dot product here
	dotProduct=0
	for word in row:
		if word != "POSITIVE" and word != "NEGATIVE":
			dotProduct+=w[word]
		
	if dotProduct >= 0:
		   return "POSITIVE"
	
	return "NEGATIVE"

# samples - test vectors.
# w is the weight dictionary.
def handleTestData(samples, w):	
	tp=0
	fp=0
	tn=0
	fn=0	
	totalCount=len(samples)
	if totalCount <=0:
		print "Test data set is empty"
		exit()
		
	for row in samples:
		pLabel = predictLabel(row,w)
		aLabel = row[len(row)-1]
		if(aLabel == "POSITIVE"):
			if(pLabel=="POSITIVE"):
				tp+=1
			else:
				fn+=1			
		else:
			if (pLabel=="POSITIVE"):
				fp+=1
			else:
				tn+=1
				
	print "Total True positives is ",tp
	print "Total True Negatives is ",tn
	print "Total False Positives is ",fp
	print "Total False Negatives is ",fn
	print "Total Accuracy is ", (float(tp+tn)*100)/(tp + tn + fp + fn), " %"

#w is the weight vector
#x is the feature vecotor
#returns 1/(1+exp(w.x))
def maxLikelyHood(w,sample):
	dotProduct=0
	for i in sample:
		if i != "POSITIVE" and i != "NEGATIVE":
			dotProduct -= w[i]	#note the minus sign here...
			#print i, "--",w[i]
	
	
	if dotProduct > 100:
		dotProduct =100
	elif dotProduct < -100:
		dotProduct = -100
		
	#print dotProduct	
	return long(1)/long((1+math.exp(dotProduct)))
	#return 0
	
def runLogisticRegression(liFeatures, trainVectors, testVectors):
	#define global variables...
	global learningRate
	global threshold
	
	#initialize the weight vector to be 0's
	#weightVector = [0 for i in range(0,numFeatures)]	
	weightVector = {}	
	weightVectorBackUp = {}
	
	for w in liFeatures:
		weightVector[w] = 0
		weightVectorBackUp[w] = 0

	iterations=0
	
	while True: 
		iterations+=1		
		#init gradient vector...
		gradientVector = {}
		for key in weightVector:
			gradientVector[key] = 0		 
			
		for sample in trainVectors:
			y = -1
			if sample[len(sample)-1] == "POSITIVE":
				y = 1
			else:
				y = 0
			
			error = y - maxLikelyHood(weightVectorBackUp,sample)			
			for j in sample:
				if j != "POSITIVE" and j != "NEGATIVE":
					gradientVector[j]+=error
		
		#update weight vector..
		for key in weightVector:		
			weightVector[key]+=learningRate*gradientVector[key]				
		
		#print weightVector
		#check whether the increment in weight vector is greater than the "threshold" for every feature...		
		shouldBreak=True
		for i in weightVector:
			if math.fabs(weightVector[i] - weightVectorBackUp[i]) > threshold:
				shouldBreak=False		
			
		if shouldBreak==True:
			break
		else:
			#take a backup of the weight vector...				
			for key in weightVector:
				weightVectorBackUp[key] = weightVector[key]

	#print weightVector
	print "Number of Iterations it took for converging "+str(iterations) 
	
	#evaluating the test data...
	print "Evaluating the Test data..."
	handleTestData(testVectors,weightVector)
	
#Execution begins here
if __name__ == "__main__" : main()	
