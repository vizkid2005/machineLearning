#!/usr/bin/python
import sys
import csv
from math import *
liActions = []
rowSize = 5
colSize = 4
wallBlocks = [(3,1), (3,3)]
gamma = 0.9
threshold = 0.001

class actions:
	def __init__(self, action, listOfEffects):
		self.action = action
		self.listOfEffects = listOfEffects #this is a dictionary of effect to probabilities.

def printMatrix(v):
	print
	print "-"*25
	print "Printing Value Matrix"
	print "-"*25
	print
	for row in v:
		print row


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

def copyMatrix(a,b): # copies a to b
	global rowSize
	global colSize
	for i in range(rowSize):
		for j in range(colSize):
			b[i][j] = a[i][j]

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

	#init the value matrix
	value=[ [-100 for b in range(colSize)] for a in range(rowSize)]
	
	#init the goal and pit values.
	value[1][1] = -50
	value[0][3] = 10
	iterations = 0
	while True:
		iterations+=1
		valueBackup =[ [-100 for b in range(colSize)] for a in range(rowSize)]
		copyMatrix(value, valueBackup)
		for i in range(rowSize):
			for j in range(colSize):
				#check that the current block is a wall or not..
				if (i,j) in wallBlocks:
					continue
				#this has four possible actions..
				maxVal = -10000 
				for a in liActions:
					currVal=-1				
					for effect in a.listOfEffects.keys():
						inew, jnew = move(effect, i, j)	
						if isWallBlock(i,j):
							continue					
						if (isStateValid(inew, jnew)):
							currVal += (gamma*a.listOfEffects[effect]*valueBackup[inew][jnew])
						else: # we remain in the same state.
							currVal += (gamma*a.listOfEffects[effect]*valueBackup[i][j])
							
					#print currVal
					if currVal > maxVal:
						maxVal = currVal
				value[i][j] = maxVal
		shldBreak = True
		for i in range(rowSize):
			for j in range(colSize):
				if fabs(valueBackup[i][j]-value[i][j]) > threshold:
					shldBreak = False
		if(shldBreak==True):
			break
		break
		
		
	print "Number of iterations it took to converge is ", iterations													
	printMatrix(value)			
	

	
#Execution begins here
if __name__ == "__main__" : main()	
		
