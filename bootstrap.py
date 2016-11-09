#!/usr/local/bin/python
# coding: latin-1
import re
import os
import time
import sys
import random


class Bootstrap: 

	template = { 'N' : [
		'.','.','.','.','▒','▒','.','.','.',',', 
		'.','.','.','▒','▒','▒','▒','.','.',',',
		'.','.','▒','▒','▒','▒','▒','▒','.',',',
		'.','.','.','▒','▒','▒','▒','.','.',',',
		',',',',',','▒','▒','▒','▒',',',',',','
	], 

	'S' : [
		'.','.','.','▒','▒','▒','▒','.','.',',', 
		'.','.','.','▒','▒','▒','▒','.','.',',',
		'.','.','▒','▒','▒','▒','▒','▒','.',',',
		'.','.','.','▒','▒','▒','▒','.','.',',',
		',',',',',',',','▒','▒',',',',',',',','
	], 

	'W' : [
		'.','.','.','▒','.','.','.','.','.',',', 
		'.','.','▒','▒','▒','▒','▒','▒','.',',',
		'.','▒','▒','▒','▒','▒','▒','▒','.',',',
		'.','.','▒','▒','▒','▒','▒','▒','.',',',
		'.','.',',','▒',',',',',',',',',',',','
	], 

	'E' : [
		'.','.','.','.','.','.','▒','.','.',',', 
		'.','.','▒','▒','▒','▒','▒','▒','.',',',
		'.','.','▒','▒','▒','▒','▒','▒','▒',',',
		'.','.','▒','▒','▒','▒','▒','▒','.',',',
		',',',',',',',',',',',','▒',',',',',','
	]
	}

	interatorTemplate = [] 
	def __init__(self):
		self.map = []	
		self.rovers = []
		self.sizex = 1
		self.sizey = 1
		self.xLimit = 1
		self.yLimit = 1 


	def buildMap(self) : 
		
		for rover in self.rovers:
		 	self.interatorTemplate.append(0)

		for valueL in range(0, self.yLimit):
			currentLine = []
			for valueC in reversed(range(0, self.xLimit)):	
				hasRover = self.hasARover(valueC, valueL)

				if not hasRover is False:
					
					currentLine.append(self.template[self.rovers[hasRover]['orientation']][self.interatorTemplate[hasRover]])
					self.interatorTemplate[hasRover]+= 1
		
				else:
					if(valueC % self.sizex ==  0 ):
						currentLine.append(',')	
					else:	
						if (valueL % self.sizey == self.sizey - 1):
							currentLine.append(',')	
						else:
							currentLine.append('.')

			self.map.append(currentLine)
		
		return self.map	
		
	def setSizePointMap(self,x,y):
		self.sizex = x
		self.sizey = y	

	def setLimitMap(self,x,y):
		self.xLimit = x * self.sizex
		self.yLimit = y * self.sizey
		

	def setData(self, data):
		data = re.sub('\t+', '', data)
		data = data.splitlines()
		self.inputData = data
	
	def readData(self):	
		for index, value in enumerate(self.inputData):

			if index == 0:
				mapLimit = value.split(' ')	
				self.setLimitMap(int(mapLimit[0]) + 1, int(mapLimit[1]) + 1)
			elif index % 2 == 0:
				initialPosition = initialPosition.split(' ')
				self.addRoverPosition(int(initialPosition[0]), int(initialPosition[1]), initialPosition[2], value)
				initialPosition = None 
			else: 
				initialPosition = value

		return True	
			
	def getRelativePosition(self, d, c):
		if d == 'x':
			return (self.xLimit / self.sizex - (c + 1)) * self.sizex  #50 / 10 = 5 - 2 =  3
		elif d == 'y':	
			return (self.yLimit / self.sizey - (c + 1)) * self.sizey  #25 / 5 = 5 - 2 = 3 

	def addRoverPosition(self, x, y, orientation, coordinates = None, steps = 0):
		relativeX = self.getRelativePosition('x', x) 
		relativeY = self.getRelativePosition('y', y) 

		self.rovers.append({"x" : x, "y": y, "orientation" : orientation, "pX" : relativeX, "pY": relativeY, "coordinates" : coordinates, 'steps' : steps}) 
		

	def hasARover(self, x, y):
		index = 0
		for value in enumerate(self.rovers):
			if(
				(x >= value[1]['pX'] and x < value[1]['pX'] + self.sizex)
				and (y >= value[1]['pY'] and y < value[1]['pY'] + self.sizey) 

			):
				return index 
			index+=1

		return False 

	
	def clear(self):

		self.interatorTemplate = []
		self.map = []

	
	def refreshPositions(self):
		index = 0
		for value in enumerate(self.rovers):
			

			for letterIndex, letter in enumerate(value[1]['coordinates']):
				
				if letterIndex == self.rovers[index]['steps']:
					
					self.setMovement(index, letter) 

					self.rovers[index]['steps']+= 1
					break
				
			index+=1


		return True

	
	def setMovement(self, indexRover, typeMovement):
		
		
		orientation = self.rovers[indexRover]['orientation']
		if typeMovement == 'M':
			
			if orientation == 'N':
				self.rovers[indexRover]['y']+= 1					
				self.rovers[indexRover]['pY'] = self.getRelativePosition('y', self.rovers[indexRover]['y'])
			if orientation == 'S':
				self.rovers[indexRover]['y']-= 1					
				self.rovers[indexRover]['pY'] = self.getRelativePosition('y', self.rovers[indexRover]['y'])

			if orientation == 'W':
				self.rovers[indexRover]['x']-= 1					
				self.rovers[indexRover]['pX'] = self.getRelativePosition('x', self.rovers[indexRover]['x'])	

			if orientation == 'E':
				self.rovers[indexRover]['x']+= 1					
				self.rovers[indexRover]['pX'] = self.getRelativePosition('x', self.rovers[indexRover]['x'])	

		elif typeMovement == 'L':

			if orientation == 'N':
				self.rovers[indexRover]['orientation'] = 'W'
			if orientation == 'S':
				self.rovers[indexRover]['orientation'] = 'E'
			if orientation == 'W':
				self.rovers[indexRover]['orientation'] = 'S'
			if orientation == 'E':
				self.rovers[indexRover]['orientation'] = 'N'

		elif typeMovement == 'R':
			
			if orientation == 'N':
				self.rovers[indexRover]['orientation'] = 'E'
			if orientation == 'S':
				self.rovers[indexRover]['orientation'] = 'W'
			if orientation == 'W':
				self.rovers[indexRover]['orientation'] = 'N'
			if orientation == 'E':
				self.rovers[indexRover]['orientation'] = 'S'

		return True

		
	
	def start(self):

		self.readData()


		cont = 0
		
		while(cont < 11):

			os.system("clear")
			
			self.buildMap()

			for i in range(0,len(self.map)):
				print "".join(self.map[i])
			
			
			time.sleep(1)


			self.refreshPositions()

			cont+=1


			self.clear()

		print "\nOutput Data: "	
		for rover in self.rovers:
			print rover['x'], rover['y'], rover['orientation'] 



boot = Bootstrap()
boot.setSizePointMap(10, 5)


boot.setData("".join(line for line in open('inputdata')))
boot.start()
