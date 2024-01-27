import random
# Consistant Hash Map Implementation.
# It is possible client and server map to same hash value. Then store in same cell.
class ConsistentHashmapImpl:
    def __init__(self, servers, virtualServers, slotsInHashMap):
        self.servers = servers
        self.virtualServers = virtualServers
        self.slotsInHashMap = slotsInHashMap
        self.occupied_slots = [-1]*slotsInHashMap
    
    def calculateVirtualServerHashValue(self, serverId, virtualServerNumber):
        sid = int(serverId)
        vsn = int(virtualServerNumber)
        hashingValueOfVirtualServer = ((sid ** 2) + (vsn ** 2) + (2 * vsn) + 25) % self.slotsInHashMap
        return hashingValueOfVirtualServer
    
    def calculateRequestHashValue(self, requestId):
        hashingValueOfRequest = (pow(requestId, 2) + (2*requestId) + 17) % self.slotsInHashMap
        return hashingValueOfRequest
    
    def getServers(self): 
        return self.servers

    # adding virtual server to hashmap. If there is colosion, then resolve using linear probing.
    def addServer(self, serverId, serverName):
        for virtualServerNumber in range(1, self.virtualServers + 1):
            virtualServerHashValue = self.calculateVirtualServerHashValue(serverId, virtualServerNumber)
            initial_hash_value = virtualServerHashValue
            i = 0
            while self.occupied_slots[virtualServerHashValue] != -1 and i<self.slotsInHashMap:
                i+= 1
                virtualServerHashValue = (initial_hash_value + i**2) % self.slotsInHashMap

            # If all the slots are checked and still not found an empty slot, then return.
            if self.occupied_slots[virtualServerHashValue] != -1:
                return False

            self.occupied_slots[virtualServerHashValue] = serverId

        self.servers.append(serverName)
        return True

    # removing virtual server from hashmap. 
    def removeServer(self, serverId, serverName):
        count  = 0
        for i in range(0, self.slotsInHashMap): 
            if int(self.occupied_slots[i]) == int(serverId) : 
                count+=1
                self.occupied_slots[i] = -1
        # Checking if serverName in servers list, then remove it.
        if serverName in self.servers:
            self.servers.remove(serverName)


    def getContainerID(self, requestId): 
        requestHashValue = self.calculateRequestHashValue(requestId)

        while self.occupied_slots[requestHashValue] == -1:
            requestHashValue = (requestHashValue+1)%self.slotsInHashMap

        # print(self.occupied_slots)
        return self.occupied_slots[requestHashValue]
    
    def getRandomServerId(self): 
        return random.choice(self.servers)

