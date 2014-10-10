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

#row is a sample
#lProbabilities - Prior Probabilities for each label.
#fProbabilities - Conditional Feature Probabilities for each label.
def predictLabel(row,lProbabilities,fProbabilities):
	#init vars
	maxProb =0
	maxLabel=""
	#loop over all possible labels and compute prob for each label.
	for label in lProbabilities:
		currentProb = lProbabilities[label]
		for index in range(numFeatures):
			key = (index, row[index], label)
			currentProb*=fProbabilities[key]
		if currentProb>maxProb:
			maxProb=currentProb
			maxLabel=label
	return maxLabel


#inputFileName - file name of the test set
# w is the weight vector.
#outputFileName - file name for the output.
#consider 1 as + 
# ans o as -ve
def handleTestData(inputFileName,lProbabilities,fProbabilities,outputFileName):
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
		pLabel = predictLabel(row,lProbabilities,fProbabilities)
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
	
	labelCounts={}
	#init class label counts...
	labelCounts["0"]=0
	labelCounts["1"]=0
	
	#the dictionary will contain counts of the feature occurrences, for each output label
	#the key will be a tuple (featureIndex, featureValue,outputLabel)
	featureCounts={}
	
	#the dictionary will contain probabilities of the feature occurrences, given output label
	#the key will be a tuple (featureIndex, featureValue,outputLabel)
	featureProbabilities={}

	#count the label occurrences...
	for row in trainingSet:
		labelCounts[row[classIndex]]+=1
		for index in range(numFeatures):
			key = (str(index), row[index],row[classIndex])
			if key in featureCounts:
				featureCounts[key]+=1
			else:
				featureCounts[key]=1

	#compute feature probabilities given class label.
	for key in featureCounts:
		featureProbabilities[key] = float(featureCounts[key])/labelCounts[key[2]]

	handleTestData(testSetFileName,labelProbabilities,featureProbabilities,"NB-results/output.csv")

			
#Execution begins here
if __name__ == "__main__" : main()	
