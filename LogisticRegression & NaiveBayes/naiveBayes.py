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
	global numFeatures
	global classIndex
	
	#init vars
	maxProb =0
	maxLabel=""
	#loop over all possible labels and compute prob for each label.
	s=""
	for label in lProbabilities:
		currentProb = lProbabilities[label]
		for index in range(numFeatures):
			key = (str(index), row[index], label)
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
	#define global variables...
	global numFeatures
	global trainingSetFileName
	global testSetFileName
	global numFeatures
	global classIndex
	
	
	trainingSet=readData(trainingSetFileName)
	if len(trainingSet) <=0:
		print "No data in training set"
		exit()

	numFeatures=len(trainingSet[0])-1
	classIndex=numFeatures

	#the below dictionary will contain probabilities of the label occurrences
	#the key will be the label value	
	labelCounts={}

	#the below dictionary will contain counts of the feature occurrences, for each output label
	#the key will be a tuple (featureIndex, featureValue,outputLabel)
	featureCounts={}
	
	#the below dictionary will contain probabilities of the feature occurrences, given output label
	#the key will be a tuple (featureIndex, featureValue,outputLabel)
	featureProbabilities={}
	
	#the below dictionary will contain probabilities of the label occurrences
	#the key will be the label value
	labelProbabilities={}

	
	for row in trainingSet:
		#count the label occurrences...
		if row[classIndex] in labelCounts:			
			labelCounts[row[classIndex]]+=1
		else:
			labelCounts[row[classIndex]]=1
		
		#computing conditional counts.	
		for index in range(numFeatures):
			key = (str(index), row[index],row[classIndex])
			if key in featureCounts:
				featureCounts[key]+=1
			else:
				featureCounts[key]=1

	totalCount=len(trainingSet)
	#compute label Probabilities
	for key in labelCounts:
		labelProbabilities[key]=float(labelCounts[key])/totalCount

	#compute feature probabilities given class label.
	for key in featureCounts:
		featureProbabilities[key] = float(featureCounts[key])/labelCounts[key[2]]
	handleTestData(testSetFileName,labelProbabilities,featureProbabilities,"NB-results/output.csv")

			
#Execution begins here
if __name__ == "__main__" : main()	
