#!/usr/bin/python
import sys
import csv
import math


#row is a sample
#lProbabilities - Prior Probabilities for each label.
#fProbabilities - Conditional Feature Probabilities for each label.
def predictLabel(row,lProbabilities,fProbabilities, liFeatures):
	#init vars
	maxProb =0
	maxLabel=""
	#loop over all possible labels and compute prob for each label.	
	for label in lProbabilities:
		currentProb = lProbabilities[label]		
		currFeatures = row[:-1] # exclude the last element which is the class label..
		notPresentFeatures = [ a for a in liFeatures if a not in currFeatures]
		for f in currFeatures:
			key = (f, label)			
			currentProb*=fProbabilities[key]
		
		for f in notPresentFeatures:
			key = (f, label)
			currentProb*=(1-fProbabilities[key])
			
		if currentProb>maxProb:
			maxProb=currentProb
			maxLabel=label		

	return maxLabel


#inputFileName - file name of the test set
# w is the weight vector.
#consider 1 as + 
# ans o as -ve
def handleTestData(testVectors,lProbabilities,fProbabilities, liFeatures):
	tp=0
	fp=0
	tn=0
	fn=0
	totalCount=len(testVectors)
	if totalCount <=0:
		print "Test data set is empty"
		exit()
			
	for row in testVectors:
		pLabel = predictLabel(row, lProbabilities, fProbabilities, liFeatures)
		aLabel = row[len(row)-1] 
		if(aLabel=="POSITIVE"):
			if(pLabel=="POSITIVE"):
				tp+=1
			else:
				fn+=1			
		else:
			if (pLabel=="POSITIVE"):
				fp+=1
			else:
				tn+=1
				
	#print "Total True positives is ",tp
	#print "Total True Negatives is ",tn
	#print "Total False Positives is ",fp
	#print "Total False Negatives is ",fn
	#print "Total Accuracy is ", (float(tp+tn)*100)/(tp + tn + fp + fn), " %"
	return (float(tp+tn)*100)/(tp + tn + fp + fn)
	
	
def runNaiveBayes(liFeatures, trainVectors, testVectors):
	
	if len(trainVectors) <=0:
		print "No data in training set"
		exit()


	#the below dictionary will contain probabilities of the label occurrences
	#the key will be the label value	
	labelCounts={}

	#the below dictionary will contain counts of the feature occurrences, for each output label
	#the key will be a tuple (feature, outputLabel)
	featureCounts={}
	
	#the below dictionary will contain probabilities of the feature occurrences, given output label
	#the key will be a tuple (feature, outputLabel)
	featureProbabilities={}
	
	#the below dictionary will contain probabilities of the label occurrences
	#the key will be the label value
	labelProbabilities={}		

	for word in liFeatures:
		keyPos = (word, "POSITIVE")
		keyNeg = (word, "NEGATIVE")
		featureCounts[keyPos] =1 #laplace smoothing.
		featureCounts[keyNeg] =1 #laplace smoothing.
	
	#laplace smoothing..
	labelCounts["NEGATIVE"] = 1
	labelCounts["POSITIVE"] = 1
	
	for row in trainVectors:
		#count the label occurrences...
		aLabel = row[len(row)-1]	
		labelCounts[aLabel]+=1
		
		#computing conditional counts.	
		temp = row[:-1] #ignore the last word of the temp..
		for word in temp:			
			key = (word, aLabel)
			featureCounts[key]+=1
	
	totalCount=len(trainVectors)
	
	shldPrint = False #use this we have to print out final probabilities...
	
	if shldPrint == True:
		#compute label Probabilities with laplace smoothing
		print "Printing P(Y)"	

	for key in labelCounts:
		labelProbabilities[key]=float(labelCounts[key])/(totalCount+2)
		if shldPrint == True:
			print "P(y=",key,") = ",labelProbabilities[key]

	if shldPrint == True:
		print
		print "-"*40
	
	if shldPrint == True:
		#compute feature probabilities given class label.
		print "Printing P(X|Y)"
		
	
	for key in featureCounts:
		
		featureProbabilities[key] = float(featureCounts[key])/(labelCounts[key[1]]+2)
		if shldPrint == True:
			print "P(x"+key[0]+"="+key[1]+"|y="+key[2]+")"+" = ",featureProbabilities[key]
	
	if shldPrint == True:	
		print
		print "-"*40	

	return handleTestData(testVectors, labelProbabilities, featureProbabilities, liFeatures)

			
#Execution begins here
if __name__ == "__main__" : main()	

