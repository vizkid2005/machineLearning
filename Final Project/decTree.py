#!/usr/bin/python
import sys
import csv
from math import log
from Node import Node
import main as main2 
import cPickle as pickle

'''
Require intuition on how to compare the row, which is a list of columns, to dict. 
See methods, makeVector(row) and shrinkVector(row). 
'''
def readData(fileName):
	data = []
	myFile = open(fileName, 'rt')
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

'''
The method calcEntropy takes a dataset as input and returns its entropy calculated on the basis of 
the number of occurences of each class label.
Here is exactly where the use of the method countOccurenceOfClassLabel() comes into play.
'''

def calcEntropy(subDataSet):
	classLablelCounts = countOccurenceOfClassLabel(subDataSet)
	totalRows = len(subDataSet)
	entropy = 0.0

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
		
		print "Current Depth : "+str(depth)
		print ""
		#We first calculate the entropy for the entire data set
		entropy = calcEntropy(subDataSet)

		#We initially set the best parameters to 0 and None
		bestGain = 0.0
		bestSet = None
		bestCriteria = None
		bestColumn = None

		#Lets first count the number of columns, excluding the last column (Ofcourse :p )
		numberOfColumns = len(makeVector(subDataSet[0]))-1

		#Now we iterate through each column to see which is the best column to split on
		for col in range(0,numberOfColumns):

			#We then see which values are present in the column, we will choose one vlalue as criteria to split into 2 datasets
			valuesInColumn = {}
			for row in subDataSet:
				row = makeVector(row)
				valuesInColumn[row[col]]=1
			
			#We are now iterating through each value in the current iteration of column to see which value serves as the best split
			for value in valuesInColumn:

				#Split the dataset on the current value of column and value
				(set1,set2) = splitData(subDataSet,col, value)

				#Calculate infoGain for each col and each value in the column
				infoGain = calcInfoGain(entropy, set1,set2)
				
				#Choose the best col and value 
				if infoGain > bestGain and len(set1) > 0 and len(set2) > 0 :
					bestGain = infoGain
					bestSet = (set1, set2)
					bestCriteria = value
					bestColumn = col
		
		#Finally split the dataset and create the subtree based on the best values obtained above
		print "Splitting on Column : "+str(bestColumn)+" with criteria : "+str(bestCriteria)
		print "Best values : "
		print "Best Gain : "+str(bestGain)
		print "Best Criteria : "+str(bestCriteria)
		print "Best Column : "+str(bestColumn)
		print ""

		if bestGain > threshold:
			lBranch =  createTree(bestSet[0],depth-1,threshold)
			rBranch = createTree(bestSet[1],depth-1,threshold)
			return Node(col = bestColumn, leftBranch = lBranch,rightBranch= rBranch, criteria = bestCriteria)

		else:
			print ""
			print "No further branching possible "
			print "Adding leaf values : "+str(valuesInColumn)
			return Node(leafValues= countOccurenceOfClassLabel(subDataSet))	

	#No further branching possible since depth has become 0, create a node with all the possible leaf values	
	else : 
		return Node(leafValues = countOccurenceOfClassLabel(subDataSet))	

'''
The method calcInfoGain returns the Information Gain when passed with the current value of entropy, and dataset split on a particular value of a particular column.
This used to find which is the best column to split the dataset on and subsequently decide what should the criteria be. 
'''
def calcInfoGain(currentEntropy, subDataSet1,subDataSet2):
	p = float(len(subDataSet1))/(len(subDataSet1)+len(subDataSet2))
	infoGain = currentEntropy - p*calcEntropy(subDataSet1) - (1-p)*calcEntropy(subDataSet2)
	return infoGain

'''
The method countOccurenceOfClassLabel is called whenever we need to count how many times each class label occurs in a the subDataSet. 
This will be used to calculate Entropy and Infogain
It returns a dictionary that has keys as the class label and the values as the number of Occurences of that class label
'''	
def countOccurenceOfClassLabel(subDataSet):
	
	countsOfLabels = {}
	for row in subDataSet:
		row = makeVector(row)
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
def classifyNewSample(tree, testData,depth,fileName):	
	
	predictionsPlusExpectedValues = []

	for row in testData:
		row = makeVector(row)
		currentNode = tree
		leaf = None
		predictedLabel = None
		currentPredictionPlusExpectedValues = []

		#Handling the Special case of depth = 0 
		if(depth == 0):
			leaf = tree.leafValues
		else:	
			#Recursively searching for the leaf node that martches the criteria
			while(leaf == None):
				if row[currentNode.col] == currentNode.criteria: 
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

	writeResult(predictionsPlusExpectedValues=predictionsPlusExpectedValues,depth=depth,fileName=fileName)

'''
The method splitData takes a dataset as input and splits it into 2 based on the criteria on the specified column and returns the resulting 2 datasets.
Provide Column value as if counting from ZERO.
'''	
def splitData(subDataSet, column, criteria):
	
	subDataSet1=[] #All samples that match the criteria
	subDataSet2=[] #All samples that do not match the criteria
	for row in subDataSet:
		row = makeVector(row)
		#Doing a one vs rest split 
		if(row[column]==criteria):
			subDataSet1.append(shrinkVector(row)) 
		else:
			subDataSet2.append(shrinkVector(row))

	return (subDataSet2,subDataSet1)

def makeVector(trainVector):

	#Added +1 to accomodate class label, may be wrong
	lengthOfVector = len(liFeaturesDict)
	vector = zeroListMaker(lengthOfVector+1)
	
	for word in trainVector:
		index = liFeaturesDict.get(word, -1)
		if index != -1:
			vector[index] = 1

	if trainVector[len(trainVector)-1] == "POSITIVE":
		vector[lengthOfVector] = 1
	elif trainVector[len(trainVector)-1] == "NEGATIVE":
		vector[lengthOfVector] = 0

	return vector	 			

def shrinkVector(fullVector):
	originalVector = []
	for index, featureValue in enumerate(fullVector[:len(fullVector)-1]):
		if featureValue == 1:

			#I have to iterate over the dictionary
			for key, value in liFeaturesDict.items():
				if value == index:
					originalVector.append(key)

	if fullVector[len(fullVector)-1] == 1:
		originalVector.append("POSITIVE")
	elif fullVector[len(fullVector)-1] == 0:
		originalVector.append("NEGATIVE")

	return originalVector				

def zeroListMaker(lengthOfList):
	return [0]*lengthOfList

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
	
	#Making the liFeatures into a Dictionary.
	for index, word in enumerate(liFeatures):
		liFeaturesDict[word] = index

	depth =1
	threshold = 0.5

	sampleData = trainVectors[:2]
	sampleData.extend(trainVectors[1200:1202])

	tree = createTree(sampleData,depth, threshold)
	printTree(tree)

	pickleFile = open(baseDir+"Tree.pickle","wb")
	pickle.dump(tree, pickleFile)
	pickleFile.close()
	
	'''
	temp = trainVectors[0]
	fullVector = makeVector(temp,liFeaturesDict)
	shrunkVector = shrinkVector(fullVector, liFeaturesDict)

	print temp
	print shrunkVector

	if set(temp) == set(shrunkVector):
		print "Both are equal"
	lenLiFeatures = len(liFeatures)
	#tree = createTree(trainVectors,depth,threshold)

	#entropy = calcEntropy(trainVectors[:200])
	#print "Entropy is : "+str(entropy)
	'''

#The main function that calls all other functions, execution begins here
def main():	

	runDecTree(1,2)	
		
#Execution begins here
if __name__ == "__main__" : main()	
		
