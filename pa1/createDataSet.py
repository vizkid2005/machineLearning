#!/usr/bin/python
import sys
import csv
import random
import decTree

'''
This file is used to create a workable datasets for training and testing(each of 1000 samples) 
from the food inspection dataset that contains more than 8700 samples.

'''
def main():
	entireDataSet = []
	trainData = []
	testData = []

	#Getting the dataset from CSV file to memory
	#Reusing the method readData from decTree.py
	entireDataSet = decTree.readData("foodInspectionsCleaned.csv")
	numberOfLines=len(entireDataSet)
	for x in range(0,1000):
		randNum = random.randrange(0,numberOfLines)
		trainData.append(entireDataSet[randNum])

	for x in range(0,1000):
		randNum = random.randrange(0,numberOfLines)
		testData.append(entireDataSet[randNum])

	#Reusing the method from decTree.py to write to csv file 	
	decTree.writeResult(predictionsPlusExpectedValues=trainData,fileName="foodInspectionTrain")
	decTree.writeResult(predictionsPlusExpectedValues=testData,fileName="foodInspectionTest")
	
if __name__ == "__main__": main()	

