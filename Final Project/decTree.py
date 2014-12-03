#!/usr/bin/python
import sys
import csv
from math import log
from Node import Node
import main as main2 
import cPickle as pickle

'''
The method calcEntropy takes a dataset as input and returns its entropy calculated on the basis of 
the number of occurences of each class label.
Here is exactly where the use of the method countOccurenceOfClassLabel() comes into play.
'''

#Works
def calcEntropy(subDataSet):
	classLablelCounts = countOccurenceOfClassLabel(subDataSet)
	totalRows = len(subDataSet)
	#print "For length of dataset : "+str(totalRows)
	#print classLablelCounts
	entropy = 0.0

	#I think, I need to handle the case where there is just one class Label,
	#For eg, just 1 NEGATIVE Sample out of 1600
	for key in classLablelCounts:
		p = float(classLablelCounts[key])/totalRows
		entropy -= p*log(p,2)

	return entropy	
	
'''
The createTree function is where all the magic happens, 
We call createTree recursively until we reach the required depth or a good decision tree
The method takes a sub part of the dataset as input and creates a tree based on the decision criteria.
'''
def createTree(subDataSet, depth=10,threshold=0.0):
	
	#Counting the number of rows in the Dataset
	#PROJECT : Now subdataset is a list of variable length vectors,
	#Each has to be converted to full size vector using the makeVector() method
	numOfRows = len(subDataSet)

	#if the required depth is > 0 and the dataset has some rows 
	if depth > 0 and len(subDataSet) > 0:
		
		#countDict = calcCountDict(subDataSet)
		print "Current Depth : "+str(depth)
		print ""
		#We first calculate the entropy for the entire data set
		entropy = calcEntropy(subDataSet)

		#We initially set the best parameters to 0 and None
		bestGain = 0.0
		bestSet = None
		bestCriteria = None
		bestColumn = None

		#Now we iterate through each column to see which is the best column to split on
		for col in liFeatures:
			#Split the dataset on the current value of column and value
			(set1,set2) = splitData(subDataSet,col)

			#Calculate infoGain for each col and each value in the column
			#MajorChange
			infoGain = calcInfoGain(entropy, set1, set2)
			
			#Choose the best col and value 
			if infoGain > bestGain and len(set1) > 0 and len(set2) > 0 :
				bestGain = infoGain
				bestSet = (set1, set2)
				bestCriteria = 1
				bestColumn = col
		
		#Finally split the dataset and create the subtree based on the best values obtained above
		print "Splitting on Column : "+str(bestColumn)
		print "Best values : "
		print "Best Gain : "+str(bestGain)
		print "Best Column : "+str(bestColumn)
		print ""

		if bestGain > threshold:
			lBranch =  createTree(bestSet[0],depth-1,threshold)
			rBranch = createTree(bestSet[1],depth-1,threshold)
			return Node(col = bestColumn, leftBranch = lBranch,rightBranch= rBranch, criteria = bestCriteria)

		else:
			print ""
			print "No further branching possible "
			print "Adding leaf values"
			return Node(leafValues= countOccurenceOfClassLabel(subDataSet))	

	#No further branching possible since depth has become 0, create a node with all the possible leaf values	
	else : 
		return Node(leafValues = countOccurenceOfClassLabel(subDataSet))	

'''
The method calcInfoGain returns the Information Gain when passed with the current value of entropy, and dataset split on a particular value of a particular column.
This used to find which is the best column to split the dataset on and subsequently decide what should the criteria be. 
'''
#Haven't checked
def calcInfoGain(currentEntropy, subDataSet1,subDataSet2):
	p = float(len(subDataSet1))/(len(subDataSet1)+len(subDataSet2))
	infoGain = currentEntropy - p*calcEntropy(subDataSet1) - (1-p)*calcEntropy(subDataSet2)
	return infoGain

'''
The method countOccurenceOfClassLabel is called whenever we need to count how many times each class label occurs in a the subDataSet. 
This will be used to calculate Entropy and Infogain
It returns a dictionary that has keys as the class label and the values as the number of Occurences of that class label
'''	

#Works
def countOccurenceOfClassLabel(subDataSet):	
	countsOfLabels = {}
	for row in subDataSet:
		if not row:
			continue		
		else:
			if row[len(row)-1] in countsOfLabels : 
				countsOfLabels[row[len(row)-1]] += 1
			else :
				countsOfLabels[row[len(row)-1]] = 1
	return countsOfLabels			

'''
The method printTree takes a tree of the type Node and an indent value. It outputs the tree in a human interpretable form 
by showing subsequent branches with indents. 
'''	

def printTree(tree, indent=''):
	if tree.leafValues != None:
		print "Leaf Node : "+str(tree.leafValues)
	else:
		print "Split on Column : "+str(tree.col)+" with criteria : "+str(tree.criteria)
		print indent+"Left Branch -> ",
		printTree(tree.leftBranch,indent="     "+indent)
		print indent+"Right Branch -> ",
		printTree(tree.rightBranch,indent="     "+indent)
'''
The method write result will write the result of the classifier and the expected result in a CSV format.
'''
def writeResult(predictionsPlusExpectedValues,depth="",fileName="predictionsWithDepth"):
	with open(fileName+str(depth+1)+".csv",'wb') as f:
		csvWriter = csv.writer(f)
		for row in predictionsPlusExpectedValues:
			csvWriter.writerow(row)
		f.close()

'''
Given a tree and a dataset, the method classifyNewSample will output the predicted classification of each row in the dataset.
'''
def classifyNewSample(tree, testData,depth):	
	
	predictionsPlusExpectedValues = []

	for row in testData:
		currentNode = tree
		leaf = None
		predictedLabel = None
		currentPredictionPlusExpectedValues = []

		#Handling the Special case of depth = 0 
		if(depth == 0):
			leaf = tree.leafValues
		else:	
			#Recursively searching for the leaf node that matches the criteria
			while(leaf == None):
				if currentNode.col in row: 
					currentNode = currentNode.rightBranch
				else:
					currentNode = currentNode.leftBranch				
				leaf = currentNode.leafValues

		# Counting the occurences of each possible class label in the leaf
		labelCount = len(leaf)

		#if there is only one label then classify as that label
		if(labelCount == 1):
			predictedLabel = leaf.keys()
		
		#Else we count the number of occurences of each label and assign the label which has a greater number of occurences
		else:
			probabilityOfClassLabels = {}
			#Counting the total number of occurences of each label
			totalNumberOfLabels = 0
			for key in leaf.keys():
				totalNumberOfLabels += leaf[key]

			#Calculating and assigning the probability of each key to the dictionary probabilityOfClassLabels
			for key in leaf.keys():
				probabilityOfClassLabels[key] = float(leaf[key])/totalNumberOfLabels

			maxProbability = 0.0
			bestKey = None
		
			'''
			Getting the label with Max Probability, if 2 labels are equally probable then the selection
			depends on the order in which the keys are stored, which is generally random, because the dict in Python stores the dict in an unordered manner 
			2 runs of the program will never have keys in the same order. 
			'''
			for key in leaf.keys():
				if probabilityOfClassLabels[key] > maxProbability:
					maxProbability = probabilityOfClassLabels[key]
					bestKey = key
			predictedLabel = bestKey

		#Handles the case where the label is of the type list, this happens when there are multiple labels in one Node
		if(type(predictedLabel) == list):	
			currentPredictionPlusExpectedValues.append(str(predictedLabel[0]))
		else: # No issue when there is just one label per node 
			currentPredictionPlusExpectedValues.append(str(predictedLabel))

		#appending the expected result from testData	
		currentPredictionPlusExpectedValues.append(row[len(row)-1])
		#List of lists containing the prediction vs expected values
		predictionsPlusExpectedValues.append(currentPredictionPlusExpectedValues)

	return predictionsPlusExpectedValues	
	#writeResult(predictionsPlusExpectedValues=predictionsPlusExpectedValues,depth=depth,fileName=fileName)

'''
The method splitData takes a dataset as input and splits it into 2 based on the criteria on the specified column and returns the resulting 2 datasets.
Provide Column value as if counting from ZERO.
'''	
#Works
def splitData(subDataSet, column):
	
	subDataSet1=[] #All samples that match the criteria
	subDataSet2=[] #All samples that do not match the criteria
	for row in subDataSet:
		#row = makeVector(row)
		#Doing a one vs rest split 
		if column in row:
			subDataSet1.append(row) 
		else:
			subDataSet2.append(row)

	return (subDataSet2,subDataSet1)

def TPTNRates(results):
	tp = tn =0
	fp = fn = 0
	for result in results:
		if result[0] == result[1] and result[0] == "POSITIVE":
			tp = tp +1
		elif result[0] == "POSITIVE" and result[1] == "NEGATIVE":
			fp = fp +1
		elif result[0] == "NEGATIVE" and result[1] == "POSITIVE":
			fn = fn +1
		elif result[0] == result[1] and result[0] == "NEGATIVE":
			tn = tn +1

	return (tp, tn, fp, fn)		

#Is Accuracy enough of an evaluation measure ?
def resultsToAccuracy(results):
	totalSamples = len(results)

	counter = 0
	for result in results:
		if result[0] == result[1]:
			counter = counter + 1
				
	return float(counter)/totalSamples		 
#I did not see the reason to use this	
def calcCountDict(subDataSet):
	countDict = {}
	for vec in subDataSet:
		for word in vec:
			if word !="POSITIVE" or word !="NEGATIVE":
				if countDict.get(word, -1) != -1:
					p, q = countDict.get(word)
					if vec[len(vec)-1] == "POSITIVE":
						p = p+1
					elif vec[len(vec)-1] == "NEGATIVE":
						q = q+1
					countDict[word] = (p, q)
				else:
					p = 0
					q = 0
					if vec[len(vec)-1] == "POSITIVE":
						p = p+1
					elif vec[len(vec)-1] == "NEGATIVE":
						q = q+1
 					countDict[word] = (p, q)
 	return countDict				

liFeatures = 0
trainVectors = []
testVectors = []
lenLiFeatures = 0
liFeaturesDict = {}

def runDecTree(dataSet, featureSelectionMethod):
	
	baseDir=""

	ds = dataSet
	fs = featureSelectionMethod

	global liFeatures
	global trainVectors
	global testVectors
	global lenLiFeatures
	global liFeaturesDict

	liFeatures, trainVectors, testVectors = main2.buildDataVectors(ds, main2.FeatureSelection.InformationGain)
	
	depthAccuracyTPTN = []

	for d in range(0,10):
		tree = createTree(trainVectors,depth = d)
		results = classifyNewSample(tree, testVectors[:20], depth = d)
		accuracy = resultsToAccuracy(results)
		tptnRates = TPTNRates(results)
		depthAccuracyTPTN.append((d, accuracy, tptnRates))
	print ""
	print ""
	print ""
	print "Depth\t Accuracy\t TP\t TN\t FP\t FN"
	for row in depthAccuracyTPTN:
		print str(row[0])+"\t "+str(row[1])+"\t "+str(row[2][0])+"\t "+str(row[2][1])+"\t "+str(row[2][2])+"\t "+str(row[2][3])

			 

	'''
	print countOccurenceOfClassLabel(trainVectors)
	print calcEntropy(trainVectors)
	temp = liFeatures[53]
	subDataSet1, subDataSet2 = splitData(trainVectors, temp)
	
	print "Len of subdataset1"
	print str(len(subDataSet1))
	print "Len of subDataSet2 "
	print str(len(subDataSet2))

	print "Entropy of subdataset 1 : "
	print calcEntropy(subDataSet1)
	print "Entropy of subDataSet1 2 : "
	print calcEntropy(subDataSet2)
	'''

	'''	
	#Making the liFeatures into a Dictionary.
	for index, word in enumerate(liFeatures):
		liFeaturesDict[word] = index

	depth =1
	threshold = 0.5

	calcCountDict()

	sampleData = trainVectors[:2]
	sampleData.extend(trainVectors[1200:1202])

	tree = createTree(sampleData,depth, threshold)
	printTree(tree)

	pickleFile = open(baseDir+"Tree.pickle","wb")
	pickle.dump(tree, pickleFile)
	pickleFile.close()
	
	'''
#The main function that calls all other functions, execution begins here
def main():	

	runDecTree(1,2)	
		
#Execution begins here
if __name__ == "__main__" : main()	
		
