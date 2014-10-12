#!/usr/bin/python
import sys
import csv

#this code is used to simplify the data set, i.e., reduce the 7-class problem to binary class problem.
def simplify(fileName):
	data = [row.replace("\r","").replace("\n","").split(',') for row in open(fileName,"r")]			
	if(len(data)<=0):
		return	
	classIndex=len(data[0])-1		
	count=0
	outputFileName=fileName.split(".")[0]+"Simplified.csv"
	outputFile=open(outputFileName,"w")
	for row in data:
		if row[classIndex]!="1":
			row[classIndex]="0"
		outputFile.write(",".join(row)+"\n")


def main():
	simplify("zoo-test.csv")
	simplify("zoo-train.csv")

#Execution begins here
if __name__ == "__main__" : main()	
