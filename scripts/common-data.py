import re
import os

# basedir = "/home/arosha/projects/Siddhi/projects/performance-test/siddhigpu-performance-test/logs/"

# basedir = "/home/arosha/projects/Siddhi/projects/graphs/logs-2016-09-13/Filter-All/"
# basedir = "/home/arosha/projects/Siddhi/projects/graphs/logs-2016-09-13/Mix-All/"
basedir = "/home/arosha/projects/Siddhi/projects/graphs/logs-2016-09-13/Filter-All/"
# sourceFileIdentification = "cpu_st.log"
# outputFileName = "3graphDataFile-cpu-st"
# basedir = "/home/arosha/projects/Siddhi/projects/performance-test/siddhigpu-performance-test/logs-2016-08-29-Filter-All/CPU_MT/"
# sourceFileIdentification = "cpu_mt.log"
# outputFileName = "3graphDataFile-cpu-mt"
# basedir = "/home/arosha/projects/Siddhi/projects/performance-test/siddhigpu-performance-test/logs-2016-08-29-Filter-All/GPU_SD/"
sourceFileIdentification = "gpu.log"
outputFileName = "3graphDataFile-gpu-sd"

# outputFileName = "3graphDataFile"

files = os.listdir(basedir)
allData = {}
for filename in files:
	if filename.__contains__(sourceFileIdentification):
		f = open(basedir + filename)
		lines = f.readlines()

		separator = "|"
		speedUp = 0
		eventProcessTroughputEPS = 0

		queuePublishLatencyCount = 0
		queuePublishLatencyTotal = 0

		xpc = 1
		uc = 1

		for line in lines:
			if line.find("Performance Logs") != -1:
				temp = line.replace("Performance Logs|", "")
				configs = temp.replace("\n", "")
			if line.find("EventConsume") != -1:
				temp = re.compile("Speedup=(.*)]")
				speedUp = temp.findall(line).__getitem__(0)
			if line.find("EventProcessTroughputEPS") != -1:
				items = line.split("|")
				temp = items.__getitem__(10)
				eventProcessTroughputEPS = temp.replace("Avg=", "")
				xpc = int(items.__getitem__(1).replace("xpc=", ""))
				uc = int(items.__getitem__(2).replace("uc=", ""))
			if line.find("QueuePublishLatency") != -1:
				queuePublishLatencyCount += 1
				temp = line.split("|").__getitem__(8)
				queuePublishLatency = temp.replace("Avg=", "")
				queuePublishLatencyTotal += float(queuePublishLatency)

		# print configs+speedUp+separator+eventProcessTroughputEPS+separator+str(queuePublishLatencyTotal)
		extractedData = configs + separator + str(speedUp) + separator + str(eventProcessTroughputEPS) + separator + \
						str(queuePublishLatencyTotal/queuePublishLatencyCount)
		# extractedData = str(xpc*uc) + separator + str(speedUp) + separator + str(eventProcessTroughputEPS) + separator + \
		# 				str(queuePublishLatencyTotal/queuePublishLatencyCount)
		allData[xpc * uc] = extractedData

outputFile = open(basedir + outputFileName, 'w+')
for k, v in sorted(allData.items()):
	outputFile.write(v)
	outputFile.write('\n')
	print v
