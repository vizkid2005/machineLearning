import main as main2
import time
import sys
import os
import cPickle as pickle
import decTree 
import random

def main():
	baseDir = ""
	listOfTrees = []
	baggedDir = baseDir+"baggedTrees/"
	treeFileList = os.listdir(baggedDir)

	#Load all the bagged trees into main memory
	for f in treeFileList:
		if "Tree20" in f:
			pickleFile = open(baggedDir+f,"rb")
			tree = pickle.load(pickleFile)
			listOfTrees.append(tree)

	#no use for liFeatures and trainVectors	
	liFeatures, trainVectors, testVectors = main2.buildDataVectors(1, main2.FeatureSelection.InformationGain)	

	biglist = []
	tree = listOfTrees[6]
	for vec in testVectors:
		result = decTree.classifyNewSample(tree, [vec], depth=20)
		biglist.append(result[0])

	accuracy = decTree.resultsToAccuracy(biglist)
	tptnRates = decTree.TPTNRates(biglist)
	
	print "Results for a single tree "	
	print "Accuracy\t TP\t TN\t FP\t FN"
	print str(accuracy)+"\t"+str(tptnRates[0])+"\t"+str(tptnRates[1])+"\t"+str(tptnRates[2])+"\t"+str(tptnRates[3])

	allPredictions =[]

	for i in range(0,len(testVectors)):
		vecPrediction = []	

		for j in range(0,9):
			result = decTree.classifyNewSample(listOfTrees[j], [testVectors[i]], depth=20)
			vecPrediction.append(result[0])	
		
		countPos = 0
		countNeg = 0
		expectedValue = None
		for result in vecPrediction:
			if result[0] == "POSITIVE":
				countPos = countPos+1
			elif result[0] == "NEGATIVE":
				countNeg = countNeg+1
			expectedValue = result[1]

		prediction = None

		if countPos == countNeg:
			prediction = coinToss()				
		elif countPos > countNeg:
			prediction = "POSITIVE"
		else :
			prediction = "NEGATIVE"

		baggedPredictionPlusExpected = [prediction, expectedValue]
		allPredictions.append(baggedPredictionPlusExpected)
	
	accuracy = decTree.resultsToAccuracy(allPredictions)
	tptnRates = decTree.TPTNRates(allPredictions)
	print "Results for bagged Tree "
	print "Accuracy\t TP\t TN\t FP\t FN"
	print str(accuracy)+"\t"+str(tptnRates[0])+"\t"+str(tptnRates[1])+"\t"+str(tptnRates[2])+"\t"+str(tptnRates[3])
	
def coinToss():
	x = random.randrange(0,10,1)
	prediction = None
	if x > 5:
		prediction = "POSITIVE"
	else:
		prediction = "NEGATIVE"
	return prediction		

if __name__=="__main__": main()