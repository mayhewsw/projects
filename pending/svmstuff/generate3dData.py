from random import random

f = open('threeclasstraindata.dat', 'w')
flab = open('threeclasstrainlabs.dat', 'w')
fact = 30

numpoints  = 300
for i in range(numpoints):
	if i < numpoints/3:
		# +x, +-y, +z
		s = str(fact*random()) + ' ' + str(fact*random() - fact/2) + ' ' + str(fact*random()) + '\n'
		f.write(s)
		flab.write("0\n")
	elif i < 2*numpoints/3:
		# -x, +-y, +z
		s = str(fact - fact*random()) + ' ' + str(fact*random() - fact/2) + ' ' + str(fact*random()) + '\n'
		f.write(s)
		flab.write("1\n")

	else:
		# +-x, +-y, -z
		s = str(fact*random() - fact/2) + ' ' + str(fact*random() - fact/2) + ' ' + str(fact - fact*random()) + '\n'
		f.write(s)
		flab.write("2\n")
		
f.close()
flab.close()

f = open('threeclasstestdata.dat', 'w')
flab = open('threeclasstestlabs.dat', 'w')

# numpoints should be divisible by 3
numpoints = 30

for i in range(numpoints):
	if i < numpoints/3:
		# +x, +-y, +z
		s = str(fact*random()) + ' ' + str(fact*random() - fact/2) + ' ' + str(fact*random()) + '\n'
		f.write(s)
		flab.write("0\n")
	elif i < 2*numpoints/3:
		# -x, +-y, +z
		s = str(fact - fact*random()) + ' ' + str(fact*random() - fact/2) + ' ' + str(fact*random()) + '\n'
		f.write(s)
		flab.write("1\n")

	else:
		# +-x, +-y, -z
		s = str(fact*random() - fact/2) + ' ' + str(fact*random() - fact/2) + ' ' + str(fact - fact*random()) + '\n'
		f.write(s)
		flab.write("2\n")

f.close()
flab.close()
