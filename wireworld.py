import json
import sys
import copy

import numpy as np

initial_state = [
[0, 0, 0, 3, 0, 0, 0], 
[0, 3, 0, 3, 0, 3, 0], 
[3, 0, 3, 0, 3, 0, 3], 
[1, 0, 0, 3, 0, 0, 1], 
[2, 0, 3, 3, 3, 0, 2], 
[0, 3, 0, 3, 0, 3, 0], 
[0, 0, 0, 3, 0, 0, 0]
]


def config(initial_state):
	print("To load a file, type in the filename. To use the default state, press enter")
	filename = input()
	if filename[-5:] != ".json":
		if filename != "":
			print(filename)
			raise Exception("Config file is not a .json file")
	if filename != "":
		print("yes")
		with open(filename, "r") as j:
			initial_state = json.load(j)
			
	rowsno = (len(initial_state))     # y coord
	colsno = (len(initial_state[0]))  # x coord
	return initial_state, rowsno, colsno
	
def arrayprint(arr):
	for row in arr:
		for col in row:
		    print(str(col) + " ", end='')
		print()		

#  This is temporary, and just used to make it easier to visualise right now
def visualarr(printarr, initial_state):

	for y in range(len(printarr)):
		for x in range(len(printarr[0])):
		    if initial_state[y][x] == 0:
		    	printarr[y][x] = (" ")
		    elif initial_state[y][x] == 1:
		    	printarr[y][x] = ("■")
		    elif initial_state[y][x] == 2:
		    	printarr[y][x] = ("▥")
		    elif initial_state[y][x] == 3:
		    	printarr[y][x] = ("□")
	return printarr

def adjcheck(x, y, initial_state, rowsno, colsno):
	total = 0
	if y > 0:  		# y-1 wont be out of bounds
		if x > 0:  		# x-1 wont be out of bounds
			if initial_state[y-1][x-1] == 1:  # top left
				total += 1
		if initial_state[y-1][x] == 1:        # top middle
			total += 1
		if x < (colsno - 1):  # x+1 wont be out of bounds
			if initial_state[y-1][x+1] == 1:  #top right
				total += 1
				
	if x > 0:  			# x-1 wont be out of bounds
		if initial_state[y][x-1] == 1:        # middle left
			total += 1

	if x < (colsno - 1):  	# x+1 wont be out of bounds
		if initial_state[y][x+1] == 1:        # middle right
			total += 1

	if y < (rowsno - 1):  # y+1 wont be out of bounds
		if x > 0:		# x-1 wont be out of bounds
			if initial_state[y+1][x-1] == 1:  # bottom left
				total += 1
		if initial_state[y+1][x] == 1:        #bottom middle
			total += 1
		if x < (colsno - 1):  # x+1 wont be out of bounds
			if initial_state[y+1][x+1] == 1:  # bottom right
				total += 1

	if 0 < total < 3:
		return True
	else:
		return False
		
def main(initial_state, printfirst):
	if printfirst == 1:
		initial_state, rowsno, colsno = config(initial_state)  # only needs to load file on first run
	else:
		rowsno = (len(initial_state))     # y coord
		colsno = (len(initial_state[0]))  # x coord
		
	if printfirst == 1:
		print("///"*12)
		print("Initial state")
		arrayprint(initial_state)

		printarr = copy.deepcopy(initial_state)
		printarr = visualarr(printarr, initial_state)	
					
		arrayprint(printarr)

	changed = copy.deepcopy(initial_state)

	for y in range(rowsno):
		for x in range(colsno):
			if (initial_state[y][x] == 1) or (initial_state[y][x] == 2):
				changed[y][x] += 1
			if (initial_state[y][x] == 3):
				if (adjcheck(x,y,initial_state,rowsno,colsno)) == True:
					changed[y][x] = 1
				else:
					changed[y][x] = 3
					
	initial_state = copy.deepcopy(changed)
	print("///"*12)
	print("Next Cycle")
		
	arrayprint(initial_state)
	
	printarr = copy.deepcopy(initial_state)
	printarr = visualarr(printarr, initial_state)

	arrayprint(printarr)	
			
	print("///"*12)	
	return initial_state	

last = main(initial_state, 1)

quitting = ""
while quitting != "exit":
	print("Type exit to quit, save if you want to save the current state, or press enter to continue")
	quitting = input()
	quitting = quitting.lower()
	
	if quitting == "save":
		print("What file would you like to save to?")
		savename = input()
		if savename[-5:] != ".json":
			savename = (savename + ".json")
		with open(savename, "w") as s:
			json.dump(last,s)
		print("Type exit to quit, or press enter to continue")
		quitting = input()
		quitting = quitting.lower()
			
	if quitting != ("exit"):
		last = main(last, 0)
		
