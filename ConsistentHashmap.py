# Consistant Hash Map Implementation.
# It is possible client and server map to same hash value. Then store in same cell.
class ConsistentHashmapImpl:
    def __init__(self, servers, virtualServers, slotsInHashMap):
        self.servers = servers
        self.virtualServers = virtualServers
        self.slotsInHashMap = slotsInHashMap
        self.hashmap = {}
        self.sorted_keys = []
    
    def calculateVirtualServerHashValue(self, serverId, virtualServerNumber):
        hashingValueOfVirtualServer = (pow(serverId, 2) + pow(virtualServerNumber, 2) + (2 * virtualServerNumber) + 25) % self.slotsInHashMap
        return hashingValueOfVirtualServer
    
    def calculateRequestHashValue(self, requestId):
        hashingValueOfRequest = (pow(requestId, 2) + (2*requestId) + 17) % self.slotsInHashMap
        return hashingValueOfRequest
    
    # adding virtual server to hashmap. If there is colosion, then resolve using linear probing.
    def addServer(self, serverId):
        for virtualServerNumber in range(1, self.virtualServers+1):
            virtualServerHashValue = self.calculateVirtualServerHashValue(serverId, virtualServerNumber)
            if virtualServerHashValue in self.hashmap:
                # Checking if the hashed cell is already having a server. If yes, then resolve using linear probing.
                while virtualServerHashValue in self.hashmap and 'server' in self.hashmap[virtualServerHashValue]:
                    virtualServerHashValue += 1
                    virtualServerHashValue %= self.slotsInHashMap
            
            if virtualServerHashValue not in self.hashmap:
                self.hashmap[virtualServerHashValue] = {'server': serverId}
            else:
                self.hashmap[virtualServerHashValue]['server'] = serverId
            self.sorted_keys.append(virtualServerHashValue)
        self.sorted_keys.sort()

    # removing virtual server from hashmap. 
    def removeServer(self, serverId):
        for virtualServerNumber in range(1, self.virtualServers+1):
            virtualServerHashValue = self.calculateVirtualServerHashValue(serverId, virtualServerNumber)
            if virtualServerHashValue in self.hashmap and 'server' in self.hashmap[virtualServerHashValue] and self.hashmap[virtualServerHashValue]['server'] == serverId:
                if 'requests' in self.hashmap[virtualServerHashValue]:
                    del self.hashmap[virtualServerHashValue]['server']
                else:
                    del self.hashmap[virtualServerHashValue]
                    self.sorted_keys.remove(virtualServerHashValue)
            else:
                # Checking if the hashed cell is already having a server. If yes, then resolve using linear probing.
                while virtualServerHashValue in self.hashmap and 'server' in self.hashmap[virtualServerHashValue]:
                    virtualServerHashValue += 1
                    virtualServerHashValue %= self.slotsInHashMap
                    if 'server' in self.hashmap[virtualServerHashValue] and self.hashmap[virtualServerHashValue]['server'] == serverId:
                        if 'requests' in self.hashmap[virtualServerHashValue]:
                            del self.hashmap[virtualServerHashValue]['server']
                        else:
                            del self.hashmap[virtualServerHashValue]
                            self.sorted_keys.remove(virtualServerHashValue)
                        break

    # adding request to hashmap. If there is colosion, then resolve using linear probing.
    


# Testing the Consistent Hash Map Implementation.
servers = [1, 2, 3]
virtualServers = 9
slotsInHashMap = 512
consistentHashmapImpl = ConsistentHashmapImpl(servers, virtualServers, slotsInHashMap)
for serverId in servers:
    consistentHashmapImpl.addServer(serverId)

print(consistentHashmapImpl.hashmap)
print(consistentHashmapImpl.sorted_keys)

consistentHashmapImpl.removeServer(2)
print(consistentHashmapImpl.hashmap)
print(consistentHashmapImpl.sorted_keys)