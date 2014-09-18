#!/usr/bin/python
import sys
import csv
from math import log
from Node import Node
'''
IMPORTANT : DO NOT make any changes .. This is still a work in progress 
You can see but you can not touch !!! 

'''

'''
This program knows no difference between a number or a string, It considers everything as a string. (Either a string matches the criteria or it doesn't) 
This makes it more robust. Ultimately entropy and informatin gain depends on the probability of a certain value.
It does not matter what the value is .. 
I think this will work in most cases .. Lets see ... 
'''

'''
The method readData, given a CSV file name, reads the data and returns the data set as a list of lists.
Each element in the list is a list.
'''
def readData(fileName):
	data = []
	myFile = open(fileName, 'rt')
	try:
		reader = csv.reader(myFile)
		for row in reader:
			#data.append(map(int, row))
			'''
			Could have converted all values to int but not doing so because the food inspection dataset has values as strings.
			Will convert to int() on the fly. (if Needed) I dont think it will be needed.
			'''
			data.append(row)
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
#Add a better version of the description.
'''
def createTree(subDataSet, depth=10):
	
	#Counting the number of rows in the Dataset
	numOfRows = len(subDataSet)
	print ""
	print ""
	print "Inside createTree with depth = "+str(depth)
	print "With Dataset : "

	for row in subDataSet:
		print row

	#if the required depth is > 0 and the dataset has some rows 
	if depth > 0 and len(subDataSet) > 0:
		
		#We first calculate the entropy for the entire data set
		entropy = calcEntropy(subDataSet)
		print "With Entropy : "+str(entropy) 
		
		#We initially set the best parameters to 0 and None
		bestGain = 0.0
		bestSet = None
		bestCriteria = None
		bestColumn = None
		print "Best values : "
		print "Gain "+str(bestGain)
		print "Set "+str(bestSet)
		print "Criteria "+str(bestCriteria)
		print "Column "+str(bestColumn)
		print ""
		#Lets first count the number of columns, excluding the last column (Ofcourse :p )
		numberOfColumns = len(subDataSet[0])-1
		#print "Number of Columns "+str(numberOfColumns)
		#print ""
		#Now we iterate through each column to see which is the best column to split on
		for col in range(0,numberOfColumns):
			#print "Value of col : "+str(col)
			#We then see which values are present in the column, we will choose one vlalue as criteria to split into 2 datasets
			valuesInColumn = {}
			for row in subDataSet:
				valuesInColumn[row[col]]=1

			#print "Values in col :  "+str(col)+ " are : "+str(valuesInColumn)	
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
		print "Gain "+str(bestGain)
		print "Set "+str(bestSet)
		print "Criteria "+str(bestCriteria)
		print "Column "+str(bestColumn)
		print ""

		if bestGain > 0.0:
			rBranch = createTree(bestSet[0],depth-1)
			lBranch =  createTree(bestSet[1],depth-1)

			# Possible loss of context in rightBranch and LeftBranch,
			return Node(col = bestColumn, leftBranch = lBranch,rightBranch= rBranch, criteria = bestCriteria)

		#No further branching possible, create a node with all the possible leaf values	
		'''
		!!!! IMPORTANT !!!!
		Note to self : 
		The leaves should be class labels 
		change code when back next time 
		Signing of at 3:05 AM  9/18/2014
		'''
		else :
			print ""
			print "No further branching possible "
			print "Adding leaf values : "+str(valuesInColumn)
			return Node(leafValues= valuesInColumn)							


'''
Small note to self : Was wondering whether the algorithm will split the data set 2wice on the same column
I am not keeping track of which column has been used for split, so it is possible that the same column may be used again for splitting.
However the algorithm would have already chosen the best column based on Info gain since it is greedy. Lets see how it plays out. 
'''
'''
The method calcInfoGain return the Information Gain when passed with the current value of entropy, and dataset split on a particular.
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
		if row[len(row)-1] in countsOfLabels : 
			countsOfLabels[row[len(row)-1]] += 1
		else :
			countsOfLabels[row[len(row)-1]] = 1

	return countsOfLabels			
	
def printTree(tree, indent=''):
	if tree.leafValues != None:
		print tree.leafValues
	else:
		print indent+"Column : "+str(tree.col)+" with criteria : "+str(tree.criteria)
		print indent+"Left Branch -> "
		printTree(tree.leftBranch,indent="     ")
		print indent+"Right Branch -> "
		printTree(tree.rightBranch,indent="     ")

def writeResult():
	print ""
def classifyNewSample():	
	print ""

'''
The method splitData takes a dataset as input and splits it into 2 based on the criteria on the specified column and returns the resulting 2 datasets.
Provide Column value as if counting from ZERO.
'''	
def splitData(subDataSet, column, criteria):
	
	subDataSet1=[]
	subDataSet2=[]
	for row in subDataSet:
		if(row[column]==criteria):
			subDataSet1.append(row)
		else:
			subDataSet2.append(row)

	return (subDataSet1,subDataSet2)

#The main function that calls all other functions, execution begins here
def main():
	
	trainData = readData("zoo-train.csv")
	testData = readData("zoo-test.csv")

	#Taking depth of tree as input
	#treeDepth = input("Enter the depth of tree : ")

	#The variable tree will be an instance of the type Node
	tree = createTree(trainData)
	print "  "
	print ""
	print ""
	printTree(tree)
if __name__ == "__main__" : main()	
		