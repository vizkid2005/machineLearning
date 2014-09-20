#!/usr/bin/python
import sys
import csv
import random

'''
This file is used to create a workable datasets for training and testing(each of 1000 samples) 
from the food inspection dataset that contains more than 8700 samples.

'''
def main():
	data = []
	myFile = open("foodInspectionTest.csv", 'rt')
	try:
		reader = csv.reader(myFile)
		for row in reader:
			data.append(row)
	except:
		print "Error opening File: "+fileName
		exit()
	finally:
		myFile.close()
	numberOfLines=len(data)	
	numFeatures=len(data[0])

	distinctValues=[]
	for i in range(0,numFeatures):
		distinctValues.append([])
	
	for row in data:
		for i in range(0,numFeatures):
			row[i]=row[i].replace("\"","")
			row[i]="\""+row[i]+"\""	
						
	for i in range(0,numFeatures):
		for row in data:
			if row[i] not in distinctValues[i]:
				distinctValues[i].append(row[i])
	print "@relation foodInspection"				
	for i in range(0,numFeatures):
		print "@attribute feature"+str(i)+" {"+ ",".join(distinctValues[i]) +"}"
	print "@data"
	print 

	for row in data:
		print ",".join(row)
	
	
if __name__ == "__main__": main()	

