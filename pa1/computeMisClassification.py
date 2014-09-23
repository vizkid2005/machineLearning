filename="PredictionOfzoo-test"
ext=".csv"
for i in range(1,17):
	filename="results/PredictionOfzoo-test"
	filename=filename+str(i)+ext
	f = open(filename,"r")
	lines=f.readlines()

	totalCount=len(lines)
	misClassificationCount=0
	for l in lines:
		t = l.split()[0].split(',')
		if(t[0]!=t[1]):
			misClassificationCount+=1
	rate = float(misClassificationCount)/totalCount		
	print str(rate)
	
