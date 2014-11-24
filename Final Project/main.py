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
def getFeatures(liPosReviews, liNegReviews):	
	#our features are unigram features...
	liFeatures = []
	for r in liPosReviews: #get word lists from positive reviews.
		wordList = re.sub("[^\w]", " ",  r).split() #replace all non-word characters with space, and then split on spaces..		
		liFeatures.extend(wordList)
	
	for r in liNegReviews: #get word lists from negative reviews..
		wordList = re.sub("[^\w]", " ",  r).split() #replace all non-word characters with space, and then split on spaces..		
		liFeatures.extend(wordList)
	
	#do unique on features..
	liFeatures = list(set(liFeatures))
	return liFeatures

tempReviews=[]

def doPreProcessing(reviews):
	global tempReviews
	#we prepend "not" to add the negation information to all words followed by a "not" and before a punctuation.
	liPuncts  = [',', ';', '!'] # can we use any other punctuation mark TODO
		
	for i in range(len(reviews)):
		finalReview = ""
		sentences = reviews[i].split('.') # this is doomed to fail, like in the cases "Mr." and "W.W.E."		
		for s in sentences:
			modSen = ""
			words = s.split(" ")
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
	global tempReviews
	#liPosReviews, liNegReviews = parseDataSetOne()
	liPosReviews, liNegReviews = parseDataSetTwo() #parse the data set..
	
	liPosReviews = doPreProcessing(liPosReviews)
	liNegReviews = doPreProcessing(liNegReviews)
	
	liFeatures = getFeatures(liPosReviews, liNegReviews) 
	print liFeatures
	
	
	
	
if __name__ == "__main__" : main()	
