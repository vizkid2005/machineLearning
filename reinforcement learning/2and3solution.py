#!/usr/bin/python
import sys
import csv
from math import *
import random

rowSize = 5
colSize = 4
wallBlocks = [(3,1), (3,3)]
epsilon = 0.5 #exploration vs exploitation...
gamma = 0.9 #discount factor..
alphaConstant = 0.1 # learning rate...

def isWallBlock(i,j):
	if (i,j) in wallBlocks:
		return True
	return False

def move(a,i,j):
	global rowSize
	global colSize
	inew=i
	jnew=j

	#ensure that it doesnt cross borders..
	if a == "up":
		if i-1 >=0:
			inew = i-1
						
	elif a == "down":
		if(i+1) < rowSize:
			inew = i+1
						
	elif a == "left":
		if j-1 >=0:
			jnew = j-1
	elif a == "right":
		if j+1 < colSize:
			jnew = j+1

	#ensure that it doesnt cross walls..
	if isWallBlock(inew,jnew):
		return (i, j)
		
	return (inew, jnew)


def placeStringInMiddle(s, width):
	s1=""	
	s = float("{0:.2f}".format(s))
	spacesToAdd = width - len(str(s))
	for i in range(spacesToAdd/2):
		s1+=" "
	s1+= str(s)
	for i in range(spacesToAdd-spacesToAdd/2):
		s1+=" "

	return s1
	
	
def printGrid(q):
	global rowSize
	global colSize
	width = 8
	print "-"*(width*3+1)*colSize
	for i in range(rowSize):
		s1 = ""
		s2 = ""
		s3 = ""
		widthSpace = " "*width
		for j in range(colSize):
			#contatenate top..
			s1+= widthSpace
			s1+= placeStringInMiddle(q[i][j]["up"], width)
			s1+= widthSpace
			s1+= "|"
			
			#print left and right
			s2+= placeStringInMiddle(q[i][j]["left"], width)
			s2+= widthSpace
			s2+= placeStringInMiddle(q[i][j]["right"], width)
			s2+= "|"
			
			#print bottom
			s3+= widthSpace
			s3+= placeStringInMiddle(q[i][j]["down"], width)
			s3+= widthSpace
			s3+= "|"
						
		print s1
		print s2
		print s3
		print "-"*(width*3+1)*colSize
	
isThirdQuestion = False
def rewardFunction(i, j):  # i, j are the row and column indices respectively...
	global isThirdQuestion
	if (i,j)  == (1,1):
		return -50 #for falling in pit
	elif (i,j) == (0,3):
		return 10 # reaching the destination..
	if isThirdQuestion:
		return 0 #no negative reward for 3rd question...
	return -1

def environment(i, j, a): # i, j are the row and column indices respectively...
	effect = a  #effect is same as action in cases of "down" and "left"
	
	if a=="up":
		val=random.choice(range(10))
		if val<=2:
			effect = "left"
		else:
			effect = "up"	
	elif a=="right":
		val=random.choice(range(10))
		if val<=2:
			effect = "down"
		else:
			effect = "right"		
	
	inew, jnew = move(effect, i, j)
	return (inew, jnew, rewardFunction(inew, jnew))	
	
#The 2nd question
def secondQuestion():	
	global rowSize
	global colSize
	global epsilon
	global gamma
	global alphaConstant
	acts = ["up", "down", "left", "right"]
	q = [[{"right":0, "left":0, "up":0, "down":0} for a in range(colSize)] for b in range(rowSize)]  #init the all q(s,a) to 0..
	
	s = (rowSize-1, 0) #start at the bottom left 
	numEpisodes=0
	
	while True:
		shldEpisodeRestart = False
		while shldEpisodeRestart==False:
				
			if s==(0, colSize-1): #if the final state is reached, then we can end this episode.
				shldEpisodeRestart = True
				
			#find out the best action...
			action=""
			maxAction = ""
			maxValue = -1000
			for key in acts:
				if q[s[0]][s[1]][key] > maxValue:
					maxValue = q[s[0]][s[1]][key]
					maxAction = key		
			
			#assume that only the 4 digits after the decimal notation are important for epsilon.
			# epsilonRound is always less than 10000
			epsilonRound = round(epsilon*1000)			
			val = random.choice(range(1000))
			if val > epsilonRound: # choose the action with maximum Q value
				action = maxAction
			else:
				#explore with uniform distribution.
				val = random.choice(range(3)) # pick any other action with equal chance.
				i = 0
				for a in acts:
					if a == maxAction:									
						continue
					elif i==val: 
						action = a
						break
					i+=1
				
			inew, jnew, rnew = environment(s[0], s[1], action)
			maxValNext = -1000
			for a in acts:
				if q[inew][jnew][a] > maxValNext:
					maxValNext = q[inew][jnew][a]
		
			q[s[0]][s[1]][action] = (1-alphaConstant)*(q[s[0]][s[1]][action]) + alphaConstant*(rnew + gamma*maxValNext)
			s = (inew, jnew)
		
		s = (rowSize-1, 0) #reset the state to start position of the episode.
		numEpisodes+=1	#update iteration count..
		if numEpisodes%10 ==0:
			#decrement the exploration on every ten episodes.
			epsilon = epsilon/(1+epsilon)
			
		if numEpisodes>100000:
			break

	print "*"*30
	print "Grid for 2nd Question is "				
	print "*"*30				
	printGrid(q)
	
	
def thirdQuestion():
	global rowSize
	global colSize
	global epsilon
	global gamma
	global alphaConstant
	
	epsilon = 0.5 #exploration vs exploitation... #reinit epsilon as it is changed by 2nd question.
	acts = ["up", "down", "left", "right"]
	q = [[{"right":0, "left":0, "up":0, "down":0} for a in range(colSize)] for b in range(rowSize)]  #init the all q(s,a) to 0..
	
	s = (rowSize-1, 0) #start at the bottom left 
	numEpisodes=0
	
	while True:
		shldEpisodeRestart = False
		while shldEpisodeRestart==False:
				
			if s==(0, colSize-1): #if the final state is reached, then we can end this episode.
				shldEpisodeRestart = True
				
			#find out the best action...
			action=""
			maxAction = ""
			maxValue = -1000
			for key in acts:
				if q[s[0]][s[1]][key] > maxValue:
					maxValue = q[s[0]][s[1]][key]
					maxAction = key		
			
			#assume that only the 4 digits after the decimal notation are important for epsilon.
			# epsilonRound is always less than 10000
			epsilonRound = round(epsilon*1000)			
			val = random.choice(range(1000))
			if val > epsilonRound: # choose the action with maximum Q value
				action = maxAction
			else:
				#explore with uniform distribution.
				val = random.choice(range(3)) # pick any other action with equal chance.
				i = 0
				for a in acts:
					if a == maxAction:									
						continue
					elif i==val: 
						action = a
						break
					i+=1
				
			inew, jnew, rnew = environment(s[0], s[1], action)
			maxValNext = -1000
			for a in acts:
				if q[inew][jnew][a] > maxValNext:
					maxValNext = q[inew][jnew][a]
		
			q[s[0]][s[1]][action] = (1-alphaConstant)*(q[s[0]][s[1]][action]) + alphaConstant*(rnew + gamma*maxValNext)
			s = (inew, jnew)
		
		s = (rowSize-1, 0) #reset the state to start position of the episode.
		numEpisodes+=1	#update iteration count..
		if numEpisodes%10 ==0:
			#decrement the exploration on every ten episodes.
			epsilon = epsilon/(1+epsilon)
			
		if numEpisodes>100000:
			break
	
	print "*"*30
	print "Grid for 3rd Question is "				
	print "*"*30
	printGrid(q)

def main():
	global isThirdQuestion
	random.seed()
	secondQuestion()
	isThirdQuestion = True
	thirdQuestion()

#Execution begins here
if __name__ == "__main__" : main()	
