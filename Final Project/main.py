#!/usr/bin/python
import os
import sys
import re
import logisticRegression

class Type():
	complete = 1
	training = 2
	test = 3

class DataSet():
	One = 1
	Two = 2
	Three = 3

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
		'''I don't think so, words are more useful than their case. 
		   However, excessive capitalization of words may indicate positive sentiment. Eg. WOW !! YAYY !!! 
		   We can try coutning the number of capitalized words per sentence normalized by the length of the review
		'''

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

thresholdForStopWords = 5

def removeStopWords(liPosReviews, liNegReviews):
	global thresholdForStopWords
	dfp, dfn = getDocFrequencies(liPosReviews, liNegReviews) 
	
	#convert the frequencies into percentages...
	for key in dfp:
		dfp[key] = (dfp[key]*100)/len(liPosReviews)
		
	for key in dfn:
		dfp[key] = (dfn[key]*100)/len(liNegReviews)
	stopWords = []	
	#remove all those words which occur more than threshold% in both the reviews..
	#if a term only occurs in one kind of set, then it is fine for us.
	for w in dfp:
		if w not in stopWords:	
			if dfp[w] >= thresholdForStopWords:
					if w in dfn and dfn[w] > thresholdForStopWords:
						stopWords.append(w)
	
	print "-"*40
	print "Stop Words removed are:"
	print "-"*40	
	tempList = []
	for s in stopWords:
		if "NOT" not in s:
			tempList.append(s)
			
	print tempList
	
	finalFeatures = [ a for a in dfp if a not in stopWords]
	finalFeatures.extend([ a for a in dfn if a not in stopWords])
	
	return list(set(finalFeatures)) #remove duplicate features.

#The NOT is getting appended to unnecessary places, CHECK
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

	
def removeStopWordsUsingIG(liPosReviews, liNegReviews):
	#TODO	
	return
					
def buildDataVectors(ds):
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
	else:	
		trainPosReviews, trainNegReviews = parseDataSetThree(Type.training)
		testPosReviews, testNegReviews = parseDataSetThree(Type.test)	

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
	
	liFeatures = removeStopWords(liPosReviews, liNegReviews)

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
	
def main():
	#builds the data vectors for both datasets..
	liFeatures,trainVectors, testVectors = buildDataVectors(DataSet.Three)	
	#print testVectors[0], len(testVectors)
	logisticRegression.runLogisticRegression(liFeatures, trainVectors, testVectors)
	
if __name__ == "__main__" : main()	
