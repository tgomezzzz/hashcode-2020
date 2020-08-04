import sys

def readData(fileName):
    file = None
    try:
        file = open(fileName)
    except: 
        print("Error: file " + fileName + " could not be opened")
    
    data = {}
    header = file.readline().split(" ")
    data["numVideos"] = int(header[0])
    data["numEndpoints"] = int(header[1])
    data["numDescriptions"] = int(header[2])
    data["numCacheServers"] = int(header[3])
    data["cacheServerCapacity"] = int(header[4])

    videoSizes = file.readline().split(" ")
    for i in range(0, data["numVideos"]):
        videoSizes[i] = int(videoSizes[i])
    data["videoSizes"] = videoSizes

    endpoints = []
    for i in range(0, data["numEndpoints"]):
        endpoint = file.readline().split(" ")
        latencyFromDataCenter = int(endpoint[0])
        numCacheServers = int(endpoint[1])
        cacheServerData = []
        for j in range(0, numCacheServers):
            cacheServer = file.readline().split(" ")
            cacheServerId = int(cacheServer[0])
            latencyFromCacheServer = int(cacheServer[1])
            cacheServerData.append((cacheServerId, latencyFromCacheServer))
        endpoints.append({"latencyFromDataCenter": latencyFromDataCenter, "cacheServerData": cacheServerData})
    data["endpoints"] = endpoints

    requests = []
    for i in range(0, data["numDescriptions"]):
        request = file.readline().split(" ")
        videoId = int(request[0])
        endpointId = int(request[1])
        count = int(request[2])
        requests.append({"videoId": videoId, "endpointId": endpointId, "count": count})
    data["requests"] = requests

    data["cacheCapacity"] = [data["cacheServerCapacity"]] * data["numCacheServers"]
    file.close()
    return data

def getCostliestRequests(data):
    requests = data["requests"]
    endpoints = data["endpoints"]

    costs = []
    for i in range(0, len(requests)):
        endpointId = requests[i]["endpointId"]
        latencyFromDataCenter = endpoints[endpointId]["latencyFromDataCenter"]
        cost = latencyFromDataCenter * requests[i]["count"]
        videoId = requests[i]["videoId"]
        # Maps the requestId to the total cost
        costs.append((i, cost, videoId))
    costs.sort(key=lambda x:x[1])
    return costs;

def getBestCache(request):
    # track available space in cache
    requestId = request[0]
    videoId = data["requests"][requestId]["videoId"]
    videoSize = data["videoSizes"][videoId]
    #print("Video size: " + str(videoSize))
    endpointId = data["requests"][requestId]["endpointId"]
    endpointCaches = data["endpoints"][endpointId]["cacheServerData"]
    endpointCaches.sort(key=lambda x:x[1])
    #print("Available caches: " + str(endpointCaches))

    # Loop over all available caches to determine which has space to cache in.
    # By sorting first, we loop over the fastest caches first.
    for i in range(0, len(endpointCaches)):
        currentCache = endpointCaches[i]
        cacheCapacity = data["cacheCapacity"]
        if cacheCapacity[currentCache[0]] >= videoSize:
            #print("Space available!!! in cache " + str(currentCache[0]))
            cacheCapacity[currentCache[0]] -= videoSize
            #print("Current size in cache " + str(currentCache[0]) + ": " + str(cacheCapacity[currentCache[0]]))
            return currentCache[0]
    # no cache can accept, so take a hit and return 
    return -1
            

if __name__ == "__main__":
    solution = {}

    if (len(sys.argv) != 2):
        print("Usage: python3 read-data.py [file name]")
        sys.exit()

    data = readData(sys.argv[1])
    costliestRequests = getCostliestRequests(data)
    
    for i in reversed(costliestRequests):
        #print("Request index: " + str(i[0]) + ", request size: " + str(i[1]), ", Video ID: " + str(i[2]))
        bestCacheId = getBestCache(i)
        #print("best cache: " + str(bestCacheId))
        if (bestCacheId != -1):
            videoSet = solution.get(bestCacheId, set())
            #print("Current video list: " + str(videoList))
            videoSet.add(i[2])
            solution[bestCacheId] = videoSet
            #print("New video list: " + str(solution[bestCacheId]))
        #print("No cache for video " + str(i[2]))

    #print()
    print("SOLUTION: " + str(solution))

    filename = "solutions" + sys.argv[1][4:][:-3] + ".out"
    solutionFile = open(filename, "w")
    solutionFile.write(str(len(solution)) + "\n")
    for i in solution:
        solutionFile.write(str(i) + " ")
        for j in solution[i]:
            solutionFile.write(str(j) + " ")
        solutionFile.write("\n")
    solutionFile.close()
