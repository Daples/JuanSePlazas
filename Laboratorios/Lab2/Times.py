import random
import sys
import time

sys.setrecursionlimit(1000000)
myFile = open('Tables.csv','w')
#Title: Mergesort Python
#Author:anumi and Jingjie Yang
#Date: September 13, 2013
#Code version: 1.0
#Availability: https://stackoverflow.com/questions/18761766/mergesort-python
def insertionsort(x):
	"""
	It orders the array x
	:param x: array with numbers
	:returns: nothing
	"""
	for i in range(len(x)):
		j = i
		while j > 0 and x[j-1]>x[j]:
			temp = x[j]
			x[j] = x[j-1]
			x[j-1] = temp
			j -= 1

def arraysum(nums, i):
	"""
	:param nums: arrary with numbers
	:param i: index in the array
	:return: the sum of all the numbers of the array
	"""
	if (i == 0):
		return nums[0]
	return nums[i] + arraysum(nums,i-1)

def arraymax(nums,n):
	"""
	:param nums: arrary with numbers
	:param n: index in the array
	:return: the biggest number of the array
	"""
	max = nums[n]
	if (n != 0):
		temp = arraymax(nums, n-1)
		if (temp > max):
			max = temp
	return max

def mergesort(x):
	"""
	:param x: array with numbers
	:return: the ordered array
	"""
	result = []
	if len(x) < 2:
		return x
	mid = int(len(x) / 2)
	y = mergesort(x[:mid])
	z = mergesort(x[mid:])
	i = 0
	j = 0
	while i < len(y) and j < len(z):
		if y[i] > z[j]:
			result.append(z[j])
			j += 1
		else:
			result.append(y[i])
			i += 1
	result += y[i:]
	result += z[j:]
	return result


def randomarray(n):
	"""
	:param n: the size of the array
	:return: a random array with size n
	"""
	return [(int)(-100*random.random()+100) for e in range(n)]

def printinfile(methodToRun, *args):
	"""
	Prints the time to run in a file
	:param methodToRun: the method that you're going to test
	:param args: the arguments that the method needs
	:return: nothing
	"""
	now = time.clock()*1000000000
	methodToRun(*args)
	after = time.clock()*1000000000
	myFile.write('\n'+str(after - now))
		
def timesinmethods():
	"""
	Calculates the time of each method
	:return: nothing
	"""
	myFile.write('ArrayMax: ')
	for i in range(1,5):
		printinfile(arraysum, randomarray(10**i), 10**i-1)

	myFile.write('\nArraySum: ')
	for i in range(1,5):
		printinfile(arraymax, randomarray(10**i), 10**i-1)

	myFile.write('\nMergeSort: ')
	for i in range(1,5):
		printinfile(mergesort, randomarray(10**i))
	
	myFile.write('\nInsertionSort: ')
	for i in range(1,5):
		printinfile(insertionsort, randomarray(10**i))
	myFile.close()

timesinmethods()
