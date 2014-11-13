#!/usr/bin/python
import sys
import csv

liActions = []
class actions:
	def __init__(self, action, listOfEffects):
		self.action = action
		self.listOfEffects = listOfEffects #this is a dictionary of effect to probabilities.

#The main function that calls all other functions, execution begins here
def main():	
	#load the input data...
	liActions.append("up", {"up":0.6, "left":0.4} )
	liActions.append("down", {"down":1.0})
	liActions.append("left", {"left":1.0})
	liActions.append("right", {"right":0.6, "down":0.4})

	
#Execution begins here
if __name__ == "__main__" : main()	
		
