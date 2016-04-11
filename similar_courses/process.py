import numpy

matrix = numpy.loadtxt("similarity.txt")
key_file = open("pair.txt", "r")
keys = {}
line = key_file.readline()
while (line!=""):
	words = line.split(':', 1)
	keys[int(words[0])] = words[1].replace("\n", "")
	line = key_file.readline()


def my_cmp(x,y):
	if x[1] < y[1]:
		return -1
	elif x[1] > y[1]:
		return 1
	else:
		return 0

output = open("output","w")

for i in range(0,341):
	
	list = []
	for j in range(0,341):
		pair = []
		pair.append(j)
		pair.append(matrix[i][j])
		list.append(pair)
	list.sort(my_cmp, reverse=True)
	
	for k in range(1,7):	
		output.write(keys[i] + " " + keys[list[k][0]] + " " + "\n")
