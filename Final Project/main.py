#!/usr/bin/python
import os
import sys

#this dataset has 1000 +ves and 1000-ves.
#this dataset has verbose reviews..
def parseDataSetOne():
	dirPositive = "datasets/set1/pos"
	liPositiveFiles = os.listdir(dirPositive)
	
	dirNegative = "datasets/set1/neg"
	liNegativeFiles = os.listdir(dirNegative)
	
	liPosReviews = []
	liNegReviews = []
	
	for f in liPositiveFiles:
		fil = open(dirPositive+"/"+f, "r")
		liPosReviews.append(fil.read())
	
	for f in liNegativeFiles:
		fil = open(dirNegative+"/"+f, "r")
		liNegReviews.append(fil.read())	
	
	return (liPosReviews, liNegReviews)

#contains 5331 positive reviews and same number of negative reviews.
#contains reviews which are short and more informal than dataset-1.
def parseDataSetTwo():
	negativeFile = "datasets/set2/rt-polarity.neg"
	positiveFile = "datasets/set2/rt-polarity.pos"	
	
	fil = open(positiveFile, "r")
	liPosReviews = fil.readlines()
		
	fil = open(negativeFile, "r")
	liNegReviews = fil.readlines()
	
	print len(liPosReviews)
	print len(liNegReviews)
	return (liPosReviews, liNegReviews)


def main():
	#parseDataSetOne()
	parseDataSetTwo()
if __name__ == "__main__" : main()	
