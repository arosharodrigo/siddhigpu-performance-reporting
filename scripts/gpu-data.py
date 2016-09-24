import os

# basedir = "/home/arosha/projects/Siddhi/projects/graphs/logs-2016-09-13/Filter-All/"
# basedir = "/home/arosha/projects/Siddhi/projects/graphs/logs-2016-09-13/Mix-All/"
basedir = "/home/arosha/projects/Siddhi/projects/graphs/logs-2016-09-13/Filter-All/"

sourceFileIdentification = "gpu_performance.log"

outputFileName = "gpuDataFile"

files = os.listdir(basedir)
allData = {}
for filename in files:
    if filename.__contains__(sourceFileIdentification):
        f = open(basedir + filename)
        lines = f.readlines()

        separator = "|"

        serializationTimeTotal = 0
        gpuTimeTotal = 0
        deserializationTimeTotal = 0

        filenameSplit = filename.split("_")
        xpc = int(filenameSplit.__getitem__(5).replace("x", ""))
        uc = int(filenameSplit.__getitem__(6).replace("c", ""))

        for line in lines:
            if line.find("EventProcessSerializationTime") != -1:
                items = line.split("|")
                temp = items.__getitem__(2)
                serializationTime = temp.replace("Avg=", "")
                # print serializationTime
                serializationTimeTotal += float(serializationTime)
            if line.find("EventProcessGpuTime") != -1:
                items = line.split("|")
                temp = items.__getitem__(2)
                gpuTime = temp.replace("Avg=", "")
                # print gpuTime
                gpuTimeTotal += float(gpuTime)
            if line.find("EventProcessSelectTime") != -1:
                items = line.split("|")
                temp = items.__getitem__(2)
                deserializationTime = temp.replace("Avg=", "")
                # print deserializationTime
                deserializationTimeTotal += float(deserializationTime)

        extractedData = str(xpc * uc) + separator + str(serializationTimeTotal) + separator + str(gpuTimeTotal) + separator \
                        + str(deserializationTimeTotal)
        allData[xpc * uc] = extractedData

outputFile = open(basedir + outputFileName, 'w+')
for k, v in sorted(allData.items()):
    outputFile.write(v)
    outputFile.write('\n')
    print v
