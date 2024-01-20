# Consistant Hash Map Implementation.
# It is possible client and server map to same hash value. Then store in same cell.
class ConsistentHashmapImpl:
    def __init__(self, servers, virtualServers, slotsInHashMap):
        self.servers = servers
        self.virtualServers = virtualServers
        self.slotsInHashMap = slotsInHashMap
        self.hashmap = {}
        self.sorted_keys = []
        occupied_slots = [-1]*slotsInHashMap
    
    def calculateVirtualServerHashValue(self, serverId, virtualServerNumber):
        hashingValueOfVirtualServer = (pow(serverId, 2) + pow(virtualServerNumber, 2) + (2 * virtualServerNumber) + 25) % self.slotsInHashMap
        return hashingValueOfVirtualServer
    
    def calculateRequestHashValue(self, requestId):
        hashingValueOfRequest = (pow(requestId, 2) + (2*requestId) + 17) % self.slotsInHashMap
        return hashingValueOfRequest
    
    # adding virtual server to hashmap. If there is colosion, then resolve using linear probing.
    def addServer(self, serverId):
        print("### Server : " + str(serverId))
        listOfOccupiedSlots = []
        for virtualServerNumber in range(1, self.virtualServers+1):
            virtualServerHashValue = self.calculateVirtualServerHashValue(serverId, virtualServerNumber)
            if virtualServerHashValue in self.hashmap:
                numberOfCellsChecked = 0

                # Checking if the hashed cell is already having a server. If yes, then resolve using linear probing. Also checking till all the slots are checked.
                while virtualServerHashValue in self.hashmap and 'server' in self.hashmap[virtualServerHashValue] and numberOfCellsChecked < self.slotsInHashMap:
                    virtualServerHashValue += 1
                    virtualServerHashValue %= self.slotsInHashMap
                    numberOfCellsChecked += 1
                
                # If all the slots are checked and still not found a empty slot, then return.
                if numberOfCellsChecked == self.slotsInHashMap:
                    return False
            
            if virtualServerHashValue not in self.hashmap:
                self.hashmap[virtualServerHashValue] = {'server': serverId}
            else:
                self.hashmap[virtualServerHashValue]['server'] = serverId

            self.occupied_slots[virtualServerHashValue] = serverId
            self.sorted_keys.append(virtualServerHashValue)
        self.sorted_keys.sort()
        return True

    # removing virtual server from hashmap. 
    def removeServer(self, serverId):
        for i in range(1, self.virtualServers+1): 
            if self.occupied_slots[i] == serverId : 
                self.occupied_slots[i] = -1
        for virtualServerNumber in range(1, self.virtualServers+1):
            virtualServerHashValue = self.calculateVirtualServerHashValue(serverId, virtualServerNumber)
            numberOfCellsChecked = 0

            # As linear probing was used to resolve colosion, we need to check all the slots to remove the server.
            while virtualServerHashValue in self.hashmap and numberOfCellsChecked < self.slotsInHashMap:
                if self.hashmap[virtualServerHashValue]['server'] == serverId:
                    self.hashmap[virtualServerHashValue].pop('server')
                    # If there is no other entry for the key, then remove the key from hashmap.
                    if len(self.hashmap[virtualServerHashValue]) == 0:
                        self.hashmap.pop(virtualServerHashValue)
                    self.sorted_keys.remove(virtualServerHashValue)
                    break
                virtualServerHashValue += 1
                virtualServerHashValue %= self.slotsInHashMap
                numberOfCellsChecked += 1

    # adding request to hashmap. If there is colosion, then resolve using linear probing.
    def addRequest(self, requestId):
        requestHashValue = self.calculateRequestHashValue(requestId)
        if requestHashValue in self.hashmap:
            numberOfCellsChecked = 0

            # Checking if the hashed cell is already having a request. If yes, then resolve using linear probing. Also checking till all the slots are checked.
            while requestHashValue in self.hashmap and 'request' in self.hashmap[requestHashValue] and numberOfCellsChecked < self.slotsInHashMap:
                requestHashValue += 1
                requestHashValue %= self.slotsInHashMap
                numberOfCellsChecked += 1
            
            # If all the slots are checked and still not found a empty slot, then return.
            if numberOfCellsChecked == self.slotsInHashMap:
                return False
        
        if requestHashValue not in self.hashmap:
            self.hashmap[requestHashValue] = {'request': requestId}
        else:
            self.hashmap[requestHashValue]['request'] = requestId
        self.sorted_keys.append(requestHashValue)
        self.sorted_keys.sort()
        return True
    
    # removing request from hashmap.
    def removeRequest(self, requestId):
        requestHashValue = self.calculateRequestHashValue(requestId)
        numberOfCellsChecked = 0

        # As linear probing was used to resolve colosion, we need to check all the slots to remove the request.
        while requestHashValue in self.hashmap and numberOfCellsChecked < self.slotsInHashMap:
            if self.hashmap[requestHashValue]['request'] == requestId:
                self.hashmap[requestHashValue].pop('request')
                # If there is no other entry for the key, then remove the key from hashmap.
                if len(self.hashmap[requestHashValue]) == 0:
                    self.hashmap.pop(requestHashValue)
                self.sorted_keys.remove(requestHashValue)
                break
            requestHashValue += 1
            requestHashValue %= self.slotsInHashMap
            numberOfCellsChecked += 1


# Testing the Consistent Hash Map Implementation.
# servers = [1, 2, 3]
# requestIds = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# virtualServers = 9
# slotsInHashMap = 512
# consistentHashmapImpl = ConsistentHashmapImpl(servers, virtualServers, slotsInHashMap)
# for serverId in servers:
#     consistentHashmapImpl.addServer(serverId)

# # print(consistentHashmapImpl.hashmap)
# # print(consistentHashmapImpl.sorted_keys)

# # consistentHashmapImpl.removeServer(2)
# # print(consistentHashmapImpl.hashmap)
# # print(consistentHashmapImpl.sorted_keys)

# for requestId in requestIds:
#     consistentHashmapImpl.addRequest(requestId)

# print(consistentHashmapImpl.hashmap)

# consistentHashmapImpl.removeRequest(2)
# print(consistentHashmapImpl.hashmap)