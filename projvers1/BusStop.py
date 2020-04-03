class BusStop:
    busStopID = ""
    busStopDesc = ""
    busServiceList = []
    Latitude = -1
    Longitude = -1
    
    def __init__(self, busStopID, busServiceList):
        self.busStopID = busStopID
        self.busServiceList = busServiceList
        #print(self.busStopID)
        #print(self.busServiceList)

    def addBusService(self, busStopID, busServiceNo):
        if self.busStopID == busStopID:
            self.busServiceList.append(busServiceNo)
        else:
            print("Add bus service fail")
    
    def addXY(self, Latitude, Longitude):
        self.Latitude = Latitude
        self.Longitude = Longitude

    def printBusDetails(self):
        print(BusStop.busStopID)
        print(BusStop.busServiceList)
    
    def getXY(self):
        return [self.Longitude, self.Latitude]
    
    def addDesc(self, desc):
        self.busStopDesc = desc
