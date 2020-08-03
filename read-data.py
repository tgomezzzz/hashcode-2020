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
            cacheServerData.append({"id": cacheServerId, "latency": latencyFromCacheServer})
        endpoints.append({"latencyFromDataCenter": latencyFromDataCenter, "cacheServerData": cacheServerData})
    data["endpointData"] = endpoints

    requests = []
    for i in range(0, data["numDescriptions"]):
        request = file.readline().split(" ")
        videoId = int(request[0])
        endpointId = int(request[1])
        count = int(request[2])
        requests.append({"videoId": videoId, "endpointId": endpointId, "count": count})
    data["requests"] = requests

    print(data)
    return data


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: python3 read-data.py [file name]")
        sys.exit()

    data = readData(sys.argv[1])