#!/usr/bin/python
import os
import sys
import re

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
		liPosReviews.append(fil.read().lower()) #features are case insensitive.. (another draw back ?)
		
	for f in liNegativeFiles:
		fil = open(dirNegative+"/"+f, "r")
		liNegReviews.append(fil.read().lower())	
	
	return (liPosReviews, liNegReviews)

#contains 5331 positive reviews and same number of negative reviews.
#contains reviews which are short and more informal than dataset-1.
def parseDataSetTwo():
	negativeFile = "datasets/set2/rt-polarity.neg"
	positiveFile = "datasets/set2/rt-polarity.pos"	
	
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
		if w == "NOT":
			pass
		if w in docFrequencyPos:
			docFrequencyPos[w]+=1
		else:
			docFrequencyPos[w]=1
	
	for w in negWords:
		if w == "NOT":
			pass
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
		fPos = dfp[w]		
		modW = "NOT"+w		
		if modW in dfp:
			fPos += dfp[modW]

		if fPos >= thresholdForStopWords:
			if w in dfn:
				fNeg = dfn[w]
				if modW in dfn:
					fNeg +=dfn[modW]
					
				if fNeg > thresholdForStopWords:
					stopWords.append(w)
					stopWords.append(modW)	
	
	print "-"*40
	print "Stop Words removed are:"
	print "-"*40	
	print stopWords
	
	finalFeatures = [ a for a in dfp if a not in stopWords]
	finalFeatures.extend([ a for a in dfn if a not in stopWords])
	
	print finalFeatures

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
					
def main():
	#liPosReviews, liNegReviews = parseDataSetOne()
	liPosReviews, liNegReviews = parseDataSetTwo() #parse the data set..
	
	liPosReviews = doPreProcessing(liPosReviews)
	liNegReviews = doPreProcessing(liNegReviews)
	
	removeStopWords(liPosReviews, liNegReviews)
	#print liFeatures
	
	
	
	
if __name__ == "__main__" : main()	
