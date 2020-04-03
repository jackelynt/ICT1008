import sys
class BusService:
    serviceNo = ""
    busStopService1 = []
    busStopService2 = []
    distance_1 = []
    distance_2 = []
    
    def __init__(self, serviceNo, busStopService1,busStopService2, distance_1, distance_2):
        self.serviceNo = serviceNo
        self.busStopService1 = busStopService1
        self.busStopService2 = busStopService2
        self.distance_1 = distance_1
        self.distance_2 = distance_2
    
        #print(self.serviceNo)
        #print(self.busStopService1)
        #print(self.busStopService2)

    def distanceFrom(self, busStopSource, busStopDestination):
        distance1 = 0
        distance2 = 0
        #print(self.busStopService1)
        #print(self.distance_1)
        #print(self.busStopService2)
        #print(self.distance_2)
        if busStopSource in self.busStopService1 and busStopDestination in self.busStopService1:
            source_index = self.busStopService1.index(busStopSource)
            dest_index = self.busStopService1.index(busStopDestination)
            #print(busStopSource)
            #print(self.distance_1[source_index])
            #print(busStopDestination)
            #print(self.distance_1[dest_index])
            distance1 = abs(self.distance_1[source_index] - self.distance_1[dest_index])
            print(distance1)
            return distance1
        if busStopSource in self.busStopService2 and busStopDestination in self.busStopService2:
            source_index = self.busStopService2.index(busStopSource)
            dest_index = self.busStopService2.index(busStopDestination)
            #print(busStopSource)
            #print(self.distance_2[source_index])
            #print(busStopDestination)
            #print(self.distance_2[dest_index])
            distance2 = abs(self.distance_2[source_index] - self.distance_2[dest_index])
            print(distance2)
            return distance2

    def StartStop(self, SourceBusStop, DestinationBusStop):
        if SourceBusStop in self.busStopService1 and DestinationBusStop in self.busStopService1:
            if len(self.busStopService1[self.busStopService1.index(SourceBusStop):self.busStopService1.index(DestinationBusStop)]) == 0:
                return self.busStopService1[self.busStopService1.index(DestinationBusStop):self.busStopService1.index(SourceBusStop)+1]
            return self.busStopService1[self.busStopService1.index(SourceBusStop):self.busStopService1.index(DestinationBusStop)+1]
            

        if SourceBusStop in self.busStopService2 and DestinationBusStop in self.busStopService2:
            if len(self.busStopService2[self.busStopService2.index(SourceBusStop):self.busStopService2.index(DestinationBusStop)]) == 0:
                return self.busStopService2[self.busStopService2.index(DestinationBusStop):self.busStopService2.index(SourceBusStop)+1]
            return self.busStopService2[self.busStopService2.index(SourceBusStop):self.busStopService2.index(DestinationBusStop)+1]

