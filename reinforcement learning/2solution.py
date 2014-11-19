#!/usr/bin/python
import sys
import csv
from math import *

liActions = []
rowSize = 5
colSize = 4
wallBlocks = [(3,1), (3,3)]
epsilon = 0.5 #exploration vs exploitation.
alpha = 0.9 # learning rate.

class actions:
	def __init__(self, action, listOfEffects):
		self.action = action
		self.listOfEffects = listOfEffects #this is a dictionary of effect to probabilities.

def isWallBlock(i,j):
	if (i,j) in wallBlocks:
		return True
	return False

def isStateValid(i,j):
	if i < 0 or i >=rowSize:
		return False
	elif j<0 or j>=colSize:
		return False
		
	return True

def move(a,i,j):
	if a == "up":
		return (i-1, j)
	if a == "down":
		return (i+1, j)
	if a == "left":
		return (i, j-1)
	if a == "right":
		return (i, j+1)


def printGrid(q):
	global rowSize
	global colSize

	for i in range(rowSize):
		for j in range(colSize):
			

#The main function that calls all other functions, execution begins here
def main():	
	global liActions
	global rowSize
	global colSize
	
	#load the input data...
	liActions.append(actions("up", {"up":0.6, "left":0.4}))
	liActions.append(actions("down", {"down":1.0}))
	liActions.append(actions("left", {"left":1.0}))
	liActions.append(actions("right", {"right":0.6, "down":0.4}))
	
	q = [[[0, 0, 0, 0] for a in range(colSize)] for b in range(rowSize)]
	 
#Execution begins here
if __name__ == "__main__" : main()	
