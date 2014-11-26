#!/usr/bin/python
import sys
import os
import random
import shutil

def partitionForDataSet1():
	posPath = "datasets/set1/pos/"
	negPath = "datasets/set1/neg/"
	
	posTrainingPath = "training/set1/pos/"
	negTrainingPath = "training/set1/neg/"

	posTestPath = "test/set1/pos/"
	negTestPath = "test/set1/neg/"
	
	posFiles = os.listdir(posPath)
	negFiles = os.listdir(negPath)
	
	random.shuffle(posFiles) #shuffle all the files,...
	random.shuffle(negFiles)
	totalPosFiles = len(posFiles)

	#we will use 4 parts for training and 1 part for testing...
	for i in range(totalPosFiles):
		if i < (4*totalPosFiles)/5:
			#copy it to training.
			shutil.copy(posPath+posFiles[i], posTrainingPath+posFiles[i])
			shutil.copy(negPath+negFiles[i], negTrainingPath+negFiles[i])
		else:
			#copy it to test.
			shutil.copy(posPath+posFiles[i], posTestPath+posFiles[i])
			shutil.copy(negPath+negFiles[i], negTestPath+negFiles[i])



def partitionForDataSet2():
	posReviews =[ a for a in  open("datasets/set2/rt-polarity.pos","r").readlines()]
	negReviews =[ a for a in  open("datasets/set2/rt-polarity.neg","r").readlines()]
	
	posTrainingFile = open("training/set2/rt-polarity.pos","w")
	negTrainingFile = open("training/set2/rt-polarity.neg","w")

	posTestFile = open("test/set2/rt-polarity.pos","w")
	negTestFile = open("test/set2/rt-polarity.neg","w")
	
	count = len(posReviews)
	
	#we will use 4 parts for training and 1 part for testing...
	for i in range(count):
		if i < (4*count)/5:
			posTrainingFile.write(posReviews[i])
			negTrainingFile.write(negReviews[i])
		else:
			posTestFile.write(posReviews[i])
			negTestFile.write(negReviews[i])			

	negTrainingFile.close()
	posTrainingFile.close()
	posTestFile.close()
	negTestFile.close()
	 
#partitionForDataSet2()
#partitionForDataSet1()
			
			
