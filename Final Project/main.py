#!/usr/bin/python
import os
import sys
import re
import logisticRegression
import naiveBayes
from math import log
import time

class Type():
	complete = 1
	training = 2
	test = 3

class DataSet():
	One = 1
	Two = 2
	Three = 3
	Yelp = 4
#this dataset has 1000 +ves and 1000-ves.
#this dataset has verbose reviews..
def parseDataSetOne(type1):
	dirPositive = ""
	dirNegative = ""
	if type1 == Type.complete:
		dirPositive = "datasets/set1/pos"
		dirNegative = "datasets/set1/neg"
	elif type1 == Type.training:
		dirPositive = "training/set1/pos"
		dirNegative = "training/set1/neg"		
	else:
		dirPositive = "test/set1/pos"
		dirNegative = "test/set1/neg"				

	liPositiveFiles = os.listdir(dirPositive)
	liNegativeFiles = os.listdir(dirNegative)
	
	liPosReviews = []
	liNegReviews = []
	
	for f in liPositiveFiles:
		fil = open(dirPositive+"/"+f, "r")
		liPosReviews.append(fil.read().lower()) #features are case insensitive.. (another draw back ?)
		
	for f in liNegativeFiles:
		fil = open(dirNegative+"/"+f, "r")
		liNegReviews.append(fil.read().lower())	
	
	return (liPosReviews, liNegReviews)

#contains 5331 positive reviews and same number of negative reviews.
#contains reviews which are short and more informal than dataset-1.
def parseDataSetTwo(type1):
	negativeFile = ""
	positiveFile = ""	
	
	if type1 == Type.complete:
		negativeFile = "datasets/set2/rt-polarity.neg"
		positiveFile = "datasets/set2/rt-polarity.pos"	
	elif type1 == Type.training:
		negativeFile = "training/set2/rt-polarity.neg"
		positiveFile = "training/set2/rt-polarity.pos"	
	else:
		negativeFile = "test/set2/rt-polarity.neg"
		positiveFile = "test/set2/rt-polarity.pos"		
	
	fil = open(positiveFile, "r")
	liPosReviews = [ a.lower() for a in fil.readlines()]#features are case-insensitive	
		
	fil = open(negativeFile, "r")
	liNegReviews = [a.lower() for a in fil.readlines()] #features are case-insensitive
	
	return (liPosReviews, liNegReviews)

#this data set is only for testing purposes..
def parseDataSetThree(type1):
	negativeFile = ""
	positiveFile = ""	
	
	if type1 == Type.complete:
		negativeFile = "datasets/set3/rt-polarity.neg"
		positiveFile = "datasets/set3/rt-polarity.pos"	
	elif type1 == Type.training:
		negativeFile = "training/set3/rt-polarity.neg"
		positiveFile = "training/set3/rt-polarity.pos"	
	else:
		negativeFile = "test/set3/rt-polarity.neg"
		positiveFile = "test/set3/rt-polarity.pos"		
	
	fil = open(positiveFile, "r")
	liPosReviews = [ a.lower() for a in fil.readlines()]#features are case-insensitive	
		
	fil = open(negativeFile, "r")
	liNegReviews = [a.lower() for a in fil.readlines()] #features are case-insensitive
	
	return (liPosReviews, liNegReviews)


#ignores punctuations in words..(it is a drawback...)
def getDocFrequencies(liPosReviews, liNegReviews):	
	#our features are unigram features...
	posWords = []
	for r in liPosReviews: #get word lists from positive reviews.
		wordList = re.sub("[^\w]", " ",  r).split() #replace all non-word characters with space, and then split on spaces..		
		posWords.extend(list(set(wordList))) #eliminate duplicates in each review.
	
	negWords = []
	for r in liNegReviews: #get word lists from negative reviews..
		wordList = re.sub("[^\w]", " ",  r).split() #replace all non-word characters with space, and then split on spaces..		
		negWords.extend(list(set(wordList)))#eliminate duplicates in each review.
	
	docFrequencyPos = {}
	docFrequencyNeg = {}
	for w in posWords:
		if len(w) > 2 and w != "NOT":
			if w in docFrequencyPos:
				docFrequencyPos[w]+=1
			else:
				docFrequencyPos[w]=1
	
	for w in negWords:
		if len(w) > 2 and w != "NOT":
			if w in docFrequencyNeg:
				docFrequencyNeg[w]+=1
			else:
				docFrequencyNeg[w]=1			
	
	return docFrequencyPos,docFrequencyNeg

class FeatureSelection():
	DocFrequency = 1
	InformationGain = 2

def getStopWordsUsingDocFrequency(dfp, dfn):
	thresholdForStopWords = 0.05 #means 5 %..
	#convert the frequencies into percentages...
	for key in dfp:
		dfp[key] = dfp[key]/len(liPosReviews)
		
	for key in dfn:
		dfp[key] = dfn[key]/len(liNegReviews)
	#remove all those words which occur more than threshold% in both the reviews..
	#if a term only occurs in one kind of set, then it is fine for us.
	stopWords = []
	for w in dfp:
		if w not in stopWords:	
			if dfp[w] >= thresholdForStopWords:
					if w in dfn and dfn[w] > thresholdForStopWords:
						stopWords.append(w)
							
	return stopWords

def removeStopWords(liPosReviews, liNegReviews, algo):	
	stopWords = []
	dfp, dfn = getDocFrequencies(liPosReviews, liNegReviews) 	
	
	if algo == 	FeatureSelection.DocFrequency:
		stopWords = getStopWordsUsingDocFrequency(dfp, dfn)
	elif algo == FeatureSelection.InformationGain:
		stopWords = getStopWordsUsingIG(dfp, dfn, liPosReviews, liNegReviews)
				
	'''
	print "-"*40
	print "Stop Words removed are:"
	print "-"*40	
	tempList = []
	for s in stopWords:
		if "NOT" != s[0:3]:
			tempList.append(s)
	print tempList				
	'''
				
	finalFeatures = [ a for a in dfp if a not in stopWords]
	finalFeatures.extend([ a for a in dfn if a not in stopWords])
			
	return list(set(finalFeatures))#remove duplicate features.	


thresholdIG = 0.1

def getStopWordsUsingIG(dfp, dfn, liPosReviews, liNegReviews):
	global thresholdIG
	stopWords = []
	totalWords = [a for a in dfp]
	totalWords.extend([a for a in dfn])
	totalWords = list(set(totalWords)) #remove duplicates..
	
	totalPos = len(liPosReviews)
	totalNeg = len(liNegReviews)
		
	liIg = {}
	for word in totalWords:
		currentEntropy = 0.5 # we have equal separation of +ve and -ves..
		wordCount = 0
		posDocuments = 0
		negDocuments = 0

		if word in dfp:
			wordCount += dfp[word]
			posDocuments = dfp[word]
			
		if word in dfn:
			wordCount += dfn[word]				
			negDocuments = dfn[word]
	
		positiveEntropy	 = 0
		if posDocuments != 0:
			positiveEntropy = (posDocuments/float(wordCount))*log((posDocuments/float(wordCount)),2)
	
		negativeEntropy	 = 0
		if negDocuments!=0:
			negativeEntopy = (negDocuments/float(wordCount))*log((negDocuments/float(wordCount)),2)

		ig  = currentEntropy - (float(wordCount)/(totalPos+totalNeg))*(-1*positiveEntropy-1*negativeEntopy)


		posDocuments = totalPos - posDocuments
		positiveEntropy	 = 0
		if posDocuments != 0:
			positiveEntropy = (posDocuments/float(totalPos+totalNeg-wordCount))*log((posDocuments/float(totalPos+totalNeg-wordCount)),2)
	
		negDocuments = totalNeg - negDocuments
		negativeEntropy	 = 0
		if negDocuments!=0:
			negativeEntopy = (negDocuments/float(wordCount))*log((negDocuments/float(wordCount)),2)

		ig  -=  (float(posDocuments+negDocuments)/(totalPos+totalNeg))*(-1*positiveEntropy-1*negativeEntopy)

		if ig in liIg:
			liIg[ig].append(word)
		else:
			liIg[ig] = [word]
				
	igs = [a for a in liIg]
	igs.sort()
	count =0
	for ig in igs:
		if count > thresholdIG*len(totalWords):
			break
		else:
			stopWords.extend(liIg[ig])
		count = count+len(liIg[ig])
					
	return stopWords

def doPreProcessing(reviews):
	#we prepend "not" to add the negation information to all words followed by a "not" and before a punctuation.
	liPuncts  = [',', ';', '!'] # can we use any other punctuation mark TODO
		
	for i in range(len(reviews)):
		finalReview = ""
		sentences = reviews[i].split('.') # this is doomed to fail, like in the cases "Mr." and "W.W.E."		
		for s in sentences:
			modSen = ""
			words = s.split()
			shldPrepend = False
			for j in range(len(words)):
				if words[j] == "not": #can we use any other negation word ???? TODO
					shldPrepend = True

				elif (words[j] in liPuncts) and shldPrepend==True:
					shldPrepend=False
										
				elif shldPrepend == True:
					modSen += "NOT"		
					
				modSen += words[j]					
				modSen += " "
					
			finalReview += modSen
		reviews[i] = finalReview
	
	return reviews

					
def buildDataVectors(ds, algo):
	liPosReviews = []
	liNegReviews = []
		
	trainPosReviews = []
	trainNegReviews = []
	testPosReviews = []
	testNegReviews = []
		
	if ds == DataSet.One:
		trainPosReviews, trainNegReviews = parseDataSetOne(Type.training)
		testPosReviews, testNegReviews = parseDataSetOne(Type.test)
	elif ds == DataSet.Two:
		trainPosReviews, trainNegReviews = parseDataSetTwo(Type.training)
		testPosReviews, testNegReviews = parseDataSetTwo(Type.test)
	elif ds == DataSet.Three:	
		trainPosReviews, trainNegReviews = parseDataSetThree(Type.training)
		testPosReviews, testNegReviews = parseDataSetThree(Type.test)	
	elif ds == DataSet.Yelp:	
		trainPosReviews, trainNegReviews = parseYelpDataSet(Type.training)
		testPosReviews, testNegReviews = parseYelpDataSet(Type.test)	

	#remove empty lines..
	trainPosReviews = [a for a in trainPosReviews if a.isspace() == False]
	trainNegReviews = [a for a in trainNegReviews if a.isspace() == False]
	testPosReviews = [a for a in testPosReviews if a.isspace() == False]
	testNegReviews = [a for a in testNegReviews if a.isspace() == False]
		
	#pre process the data...
	trainPosReviews = doPreProcessing(trainPosReviews)
	trainNegReviews = doPreProcessing(trainNegReviews)
	testPosReviews = doPreProcessing(testPosReviews)
	testNegReviews = doPreProcessing(testNegReviews)

	liPosReviews = []
	liPosReviews.extend(trainPosReviews)
	liPosReviews.extend(testPosReviews)

	liNegReviews = []
	liNegReviews.extend(trainNegReviews)
	liNegReviews.extend(testNegReviews)
	
	liFeatures = removeStopWords(liPosReviews, liNegReviews, algo)

	#build data vectors...
	trainVectors = []
	testVectors = []
	fDict = {}
	for f in liFeatures:
		fDict[f] = 1
		
	for r in trainPosReviews:
		words = list(set(r.split()))
		temp = [a for a in words if a in fDict] # we are checking only feature presence here.. can also try advanced stuff TODO
		if len(temp)!=0:
			temp.append("POSITIVE") #this is the assumed class label for a +ve review.
			trainVectors.append(temp)
		
	for r in trainNegReviews:
		words = list(set(r.split()))
		temp = [a for a in words if a in fDict] # we are checking only feature presence here.. can also try advanced stuff TODO
		if len(temp)!=0:
			temp.append("NEGATIVE") #this is the assumed class label for a -ve review.
			trainVectors.append(temp)
	
	for r in testPosReviews:
		words = list(set(r.split()))
		temp = [a for a in words if a in fDict] # we are checking only feature presence here.. can also try advanced stuff TODO
		temp.append("POSITIVE") #this is the assumed class label for a +ve review.
		testVectors.append(temp)
		
	for r in testNegReviews:
		words = list(set(r.split()))
		temp = [a for a in words if a in fDict] # we are checking only feature presence here.. can also try advanced stuff TODO

		temp.append("NEGATIVE") #this is the assumed class label for a -ve review.
		testVectors.append(temp)
	
	return liFeatures,trainVectors, testVectors						
	

def	parseYelpDataSet(type1):
	negativeFile = ""
	positiveFile = ""	
	
	if type1 == Type.training:
		negativeFile = "training/yelp/posFile.txt"
		positiveFile = "training/yelp/negFile.txt"	
	else:
		negativeFile = "test/yelp/posFile.txt"
		positiveFile = "test/yelp/negFile.txt"		
	
	fil = open(positiveFile, "r")
	liPosReviews = [ a.lower() for a in fil.readlines()]#features are case-insensitive	
		
	fil = open(negativeFile, "r")
	liNegReviews = [a.lower() for a in fil.readlines()] #features are case-insensitive
	
	return (liPosReviews, liNegReviews)
	
def handleYelpDataset():
	liFeatures,trainVectors, testVectors = buildDataVectors(DataSet.Yelp, FeatureSelection.InformationGain)
	print "running log reg now.."
	logisticRegression.runLogisticRegression(liFeatures, trainVectors, testVectors)
	
def main():
	global thresholdIG
	#builds the data vectors for both datasets..
	#liFeatures,trainVectors, testVectors = buildDataVectors(DataSet.Three, FeatureSelection.DocFrequency)
	#liFeatures,trainVectors, testVectors = buildDataVectors(DataSet.Two, FeatureSelection.InformationGain)	
	#print testVectors[0], len(testVectors)
	#logisticRegression.runLogisticRegression(liFeatures, trainVectors, testVectors)
	handleYelpDataset()
	exit()
	
	numTries = 10
	logResults = {} #dictionary to a tuple of (runtime in seconds, accuracy)
	naiveResults = {} 
	randomResults = {}				
	liThresholds=[]
	sum1 = 0
	for i in range(numTries):
		liThresholds.append(sum1)
		sum1 += 0.05 #remove 5% extra terms each time..
		#print sum1
		
	#lids = [DataSet.One, DataSet.Two]
	lids = [DataSet.Two]
	liLenFeatures = []
	for ds in lids:
		if ds ==  DataSet.One:
			print "="*40
			print "Using data set one."
			print "="*40
		else:
			print "="*40
			print "Using data set two."			
			print "="*40						

		for k in range(numTries): #total 10 different number of features..			
			thresholdIG = liThresholds[k]		
			liFeatures,trainVectors, testVectors = buildDataVectors(ds, FeatureSelection.InformationGain)		
			liLenFeatures.append(len(liFeatures))
			lAccuracy = 0
			#perform logistic regression..
			start_time = time.time()
			lAccuracy  = logisticRegression.runLogisticRegression(liFeatures, trainVectors, testVectors)
			logResults[len(liFeatures)] = (time.time() - start_time, lAccuracy)
		
		
			#perform naive Bayes...
			start_time = time.time()
			lAccuracy  = naiveBayes.runNaiveBayes(liFeatures, trainVectors, testVectors)			
			naiveResults[len(liFeatures)] = (time.time() - start_time, lAccuracy)
		
			#perform random forest...
			#TODO
	
		liLenFeatures.sort()
			
		print "-"*40
		print "Printing results with Logistic Regression"
		print "-"*40
		print "(numFeatures)\t(accuracy)\t(runTime)"
		for k in liLenFeatures:
			print k, "\t", logResults[k][1], "\t", logResults[k][0]

		print "-"*40
		print "Printing results with Naive Bayes"
		print "-"*40
		print "(numFeatures)\t(accuracy)\t(runTime)"
		for k in liLenFeatures:
			print k, "\t", naiveResults[k][1], "\t", naiveResults[k][0]

		''' 
		#commented this as random forests is not yet implemented..
		print "-"*40
		print "Printing results with Random Forests."
		print "-"*40
		print "(numFeatures)\t(accuracy)\t(runTime)"
		for k in liLenFeatures:
			print k, "\t", randomResults[k][1], "\t", randomResults[k][0]
		'''
		
if __name__ == "__main__" : main()	
