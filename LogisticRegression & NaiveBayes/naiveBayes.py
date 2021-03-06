#!/usr/bin/python
import sys
import csv
import math

trainingSetFileName="zoo-train.csv"
testSetFileName="zoo-test.csv"
numFeatures=-1
classIndex=-1
classLabelToCompare = "3"

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
#consider 1 as + 
# ans o as -ve
def handleTestData(inputFileName,lProbabilities,fProbabilities):
	global numFeatures
	global classIndex
	global classLabelToCompare
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

def main():
	#define global variables...
	global numFeatures
	global trainingSetFileName
	global testSetFileName
	global classIndex
	global classLabelToCompare
	
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

	#the below list is a list of list, each individual list is a list of distict features for that index
	distinctFeatures=[[] for i in range(numFeatures)]
	
	#the below dictionary will contain probabilities of the feature occurrences, given output label
	#the key will be a tuple (featureIndex, featureValue,outputLabel)
	featureProbabilities={}
	
	#the below dictionary will contain probabilities of the label occurrences
	#the key will be the label value
	labelProbabilities={}

	#prune datasets...
	for i in range(len(trainingSet)):
		if trainingSet[i][classIndex]!=classLabelToCompare:
			trainingSet[i][classIndex]="0" #replace all other class labels with 0
		
	
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
				featureCounts[key]=2 # start with 1 to accommodate smooting.			

			if row[index] not in distinctFeatures[index]:
					distinctFeatures[index].append(row[index])

	#do extra work for feature 13 ( index 12), as the value '5' is not in training set.
	distinctFeatures[12].append('5')
	
	#laplace smoothing...
	for index in range(numFeatures):
		for value in distinctFeatures[index]:
			for label in labelCounts:
				key = (str(index), value, label)
				if key not in featureCounts:
					featureCounts[key]=1
	
	totalCount=len(trainingSet)
	
	#compute label Probabilities with laplace smoothing
	print "Printing P(Y)"
	for key in labelCounts:
		labelProbabilities[key]=(float(labelCounts[key])+1)/(totalCount+2)
		print "P(y=",key,") = ",labelProbabilities[key]

	print
	print "-"*40
	
	#compute feature probabilities given class label.
	print "Printing P(X|Y)"
	for key in featureCounts:
		#print featureCounts[key]
		#print labelCounts[key[2]]	
		featureProbabilities[key] = float(featureCounts[key])/(labelCounts[key[2]]+len(distinctFeatures[int(key[0])]))
		print "P(x"+key[0]+"="+key[1]+"|y="+key[2]+")"+" = ",featureProbabilities[key]
	
	print
	print "-"*40	
	handleTestData(testSetFileName,labelProbabilities,featureProbabilities)

			
#Execution begins here
if __name__ == "__main__" : main()	

