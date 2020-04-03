class BusStopRoute:
    #bus stop traveling from
    busStopList = []
    #bus service used
    serviceList = []
    #bus stop to alight and change bus service
    changingBusStop = []
    #total distance covered by route
    distance = 0.0
    
    def __init__(self, busStopList, serviceList, changingBusStop, distance):
        self.busStopList = busStopList
        self.serviceList = serviceList
        self.changingBusStop = changingBusStop
        self.distance = distance
    def printRouteInfo(self):
        print(self.busStopList)
        print(self.serviceList)
        print(self.changingBusStop)
        print(self.distance)