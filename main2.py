#Dimitrios Bakalis 
#A.M. 3033

import sys
import math
import timeit
from heapq import heapify, heappush, heappop

K_value = int(sys.argv[1])

file1 = open('males_sorted', 'r')
file2 = open('females_sorted', 'r')
males_file = file1.readlines()
females_file = file2.readlines()

L1 = {}

Q = []
heapify(Q)


def dummy(given_file):
	for line in given_file:
		yield line

f_file = dummy(females_file)

def main():
	global Q,L1
	start = timeit.default_timer()

	for line in males_file:
		m_line = line.split(', ')
		male_id = int(m_line[0]) 		# id
		male_weight = float(m_line[25]) # weight
		male_age = int(m_line[1]) 		# age
		male_status = m_line[8] 		# marriage
		if(male_age<18 or male_status[0] == 'M'): # ignoring the non-valid tuples from males
			continue

		temp_male_tuple = []
		temp_male_tuple.append(male_id), temp_male_tuple.append(male_weight), temp_male_tuple.append(male_age) 
		
		if male_age in L1:	# updating the value of the same key
			ext_list = L1[male_age]
			ext_list.append(temp_male_tuple)
			L1[male_age] = ext_list
		else:				# creating a new key-value
			L1[male_age] = [(temp_male_tuple)]

	result_counter = 0
	for female in f_file:
		f_line = female.split(', ')
		female_id = int(f_line[0]) 		# id
		female_weight = float(f_line[25]) # weight
		female_age = int(f_line[1]) 		# age
		female_status = f_line[8] 		# marriage
		if(female_age<18 or female_status[0] == 'M'): # ignoring the non-valid tuples from males
			continue

		if female_age in L1:		# we want a couple with the same age
			check = L1[female_age]
			for male in check:		# checking the current female with the tuples of L1
				result_counter+=1
				result = female_weight + male[1]
				cur_list = [result,str(male[0]),str(female_id)]
				if(result_counter <= K_value):
					heappush(Q,cur_list)
				else:
					if (result > Q[0][0]):
						heappop(Q)
						heappush(Q,cur_list)

	final_counter = 0
	final_list = []
	while(final_counter < K_value):
		final_list.append(heappop(Q))
		final_counter+=1
	final_list.reverse()
 
	for final in final_list:
		print("pair: " + final[1] +"," + final[2] + " score: " + str(final[0]))

	stop = timeit.default_timer()
	print("\nTime passed: " , stop-start)
	
main()
