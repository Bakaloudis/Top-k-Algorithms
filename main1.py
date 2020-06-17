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
L2 = {}
p1_max = p1_cur = 0
p2_max = p2_cur = 0

m_counter = f_counter = T = 0

Q = []
heapify(Q)

itterated_list = [] 	# stores the couples that have been popped from the Q max heap queue

def f(value_1,value_2):
	result = value_1 + value_2
	return result

def dummy(given_file):
	for line in given_file:
		line = line.split(', ')
		yield line

m_file = dummy(males_file)
f_file = dummy(females_file)

def Top_K():
	global m_counter,f_counter,T
	global p1_max,p1_cur,p2_max,p2_cur
	global m_file,f_file
	global Q,itterated_list
	global L1,L2

	while True:

		for m_line in m_file:
			male_id = int(m_line[0]) 		# id
			male_weight = float(m_line[25]) # weight
			male_age = int(m_line[1]) 		# age
			male_status = m_line[8] 		# marriage
			temp_male_tuple = []
			temp_male_tuple.append(male_id), temp_male_tuple.append(male_weight), temp_male_tuple.append(male_age)

			if(male_age<18 or male_status[0] == 'M'): # ignoring the non-valid tuples from males
				continue

			m_counter+=1
			if(m_counter == 1): # first valid tuple from males
				p1_max = p1_cur = male_weight
				L1[male_age] = [(temp_male_tuple)]
				break
			else:
				p1_cur = male_weight
				if male_age in L1:			# updating the value of the same key
					ext_list = L1[male_age]
					ext_list.append(temp_male_tuple)
					L1[male_age] = ext_list
				else:						# creating a new key-value
					L1[male_age] = [(temp_male_tuple)]

				T = max(f(p1_max,p2_cur),f(p1_cur,p2_max))
				
				if male_age in L2:			# we want a couple with the same age
					check = L2[male_age]
					for female in check: 	# checking the current male with the tuples of L2  
						result = male_weight + female[1]
						check = 0
						for x in itterated_list:
							if(x[0] == male_id and x[1] == female[0]):
								check = 1
								break
						if(check == 0):
							cur_list = [result*-1,str(male_id),str(female[0])]
							heappush(Q,cur_list)

					if (len(Q)>=1):
						while (Q[0][0]*-1 >= T):
							final = heappop(Q)	
							couple = [final[1],final[2]]
							itterated_list.append(couple)	# updating the list with the current couple
							yield(final)
				break

		for f_line in f_file: 
			female_id = int(f_line[0]) 			# id
			female_weight = float(f_line[25]) 	# weight
			female_age = int(f_line[1]) 		# age
			female_status = f_line[8] 			# marriage
			temp_female_tuple = []
			temp_female_tuple.append(female_id), temp_female_tuple.append(female_weight), temp_female_tuple.append(female_age)

			if(female_age<18 or female_status[0] == 'M'): # ignoring the non-valid tuples from females
				continue

			f_counter+=1
			if(f_counter == 1): # first valid tuple from females
				p2_max = female_weight
			p2_cur = female_weight
			
			if female_age in L2: 			# updating the value of the same key
				ext_list = L2[female_age]
				ext_list.append(temp_female_tuple)
				L2[female_age] = ext_list
			else: 							# creating a new key-value
				L2[female_age] = [(temp_female_tuple)]

			T = max(f(p1_max,p2_cur),f(p1_cur,p2_max))
			
			if female_age in L1:	# we want a couple with the same age
				check = L1[female_age]
				for male in check: 	# checking the current female with the tuples of L1
					result = male[1] + female_weight
					check = 0
					for x in itterated_list:
						if(x[0] == male[0] and x[1] == female_id):
							check = 1
							break
					if(check == 0):
						cur_list = [result*-1,str(male[0]),str(female_id)]
						heappush(Q,cur_list)

				if (len(Q)>=1):
					while (Q[0][0]*-1 >= T):
						final = heappop(Q) 
						couple = [final[1],final[2]]
						itterated_list.append(couple)	# updating the list with the current couple
						yield(final)
			break
			
				
def main():
	start = timeit.default_timer()
	counter = 0
	for value in Top_K(): 	# running through the Top_K algorithm generator 
		counter+=1
		if (counter < K_value):
			print("pair: " + value[1] +"," + value[2] + " score: " + str(value[0]*-1))
		if (counter == K_value):
			print("pair: " + value[1] +"," + value[2] + " score: " + str(value[0]*-1))
			print('\n')
			break
	stop = timeit.default_timer()
	print("Time passed: " , stop-start)

	print("\nValid tuples that have been read from the males_sorted file:",m_counter)
	print("Valid tuples that have been read from the females_sorted file:",f_counter)

main()
