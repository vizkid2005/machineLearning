#!/usr/bin/python
import json
import sys
import os

def main():
	#path = "datasets/yelp/yelp_academic_dataset_review.json"
	path = "datasets/yelp/small.json"
	posFile = "yelp/posFile.txt"
	negFile = "yelp/negFile.txt"
	tr = "training/"
	ts = "test/"
	
	
	posTrainingFile = open(tr+posFile, "w")
	negTrainingFile = open(tr+negFile, "w")
	
	posTestFile = open(ts+posFile, "w")
	negTestFile = open(ts+negFile, "w")
	
	lines = [a for a in open(path, "rb").readlines()]
	count = len(lines)	
	thresholdForPositive = 2
	i = 0
	for l in lines:									
		obj = json.loads(l)
		if i < (4*count)/5:
			#add the review to the training list..
			if obj['stars'] > thresholdForPositive:
				posTrainingFile.write(obj['text']+"\n")
			else:
				negTrainingFile.write(obj['text']+"\n")							
		else:
			#add the review to the test list...
			if obj['stars'] > thresholdForPositive:
				posTestFile.write(obj['text']+"\n")
			else:
				negTestFile.write(obj['text']+"\n")										
		i+=1
			
	#close all the files..
	posTrainingFile.close()
	negTrainingFile.close()
	
	posTestFile.close()
	negTestFile.close()
	
#Execution begins here
if __name__ == "__main__" : main()	


