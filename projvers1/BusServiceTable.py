import csv
import pandas
from BusService import BusService

class BusServiceTable:
    busServiceDic = {}

    def __init__(self):
        busRouteDF = pandas.read_csv("BusRoute.csv")
        
        print(busRouteDF)
        busStop_List_1 = []
        busStop_List_2 = []
        distance_1 = []
        distance_2 = []
        tmpBusServiceNo = ""
        for index, row in busRouteDF.iterrows():
            if tmpBusServiceNo != row["ServiceNo"]:
                if len(busStop_List_1) != 0 or len(busStop_List_2) != 0:
                    busStop_List_1.reverse()
                    busStop_List_2.reverse()
                    bs = BusService(tmpBusServiceNo, busStop_List_1, busStop_List_2, distance_1, distance_2)
                    self.busServiceDic[tmpBusServiceNo] = bs

                tmpBusServiceNo = row["ServiceNo"]
                busStop_List_1 = []
                busStop_List_2 = []
                distance_1 = []
                distance_2 = []
            else:
                if row["Direction"] == 1:
                    busStop_List_1.append(row["BusStopCode"])
                    distance_1.append(row["Distance"])

                if row["Direction"] == 2:
                    busStop_List_2.append(row["BusStopCode"])
                    distance_2.append(row["Distance"])
        bs = BusService(tmpBusServiceNo, busStop_List_1, busStop_List_2, distance_1, distance_2)
        self.busServiceDic[tmpBusServiceNo] = bs

    def serviceNoBusStop(self, serviceNo, SourceBusStop):
        #print("Searching for ", serviceNo)
        if serviceNo not in self.busServiceDic.keys():
            #print("ServiceNo not available.", serviceNo)
            return None 
        tmpBusService = self.busServiceDic[serviceNo]
        tmpBusStopList = []
        if SourceBusStop in self.busServiceDic[serviceNo].busStopService1:
            tmpBusStopList = self.busServiceDic[serviceNo].busStopService1
        if SourceBusStop in self.busServiceDic[serviceNo].busStopService2:
            tmpBusStopList = self.busServiceDic[serviceNo].busStopService2
        return tmpBusStopList

    def searchServiceNoStartStop(self, serviceNo, SourceBusStop, DestinationBusStop):
        #print("Searching for ", serviceNo)
        #print("Start: ", SourceBusStop)
        #print("Destination: ", DestinationBusStop)
        return self.busServiceDic[serviceNo].StartStop(SourceBusStop, DestinationBusStop)
        

    def searchServiceNoDistanceBetweenBusStop(self, serviceNo, busStopSource, busStopDestination):
        #print("Searching for ", serviceNo)
        #print("Start: ", busStopSource)
        #print("Destination: ", busStopDestination)
        return self.busServiceDic[serviceNo].distanceFrom(busStopSource, busStopDestination)


#busservicetable = BusServiceTable()
#busservicetable.searchServiceNoDistanceBetweenBusStop("198",  "11361", "11059")
#busservicetable.searchServiceNoDistanceBetweenBusStop("198",  "11059", "11361")
#busservicetable.searchServiceNoDistanceBetweenBusStop("198",  "11029", "11059")
#busservicetable.searchServiceNoDistanceBetweenBusStop("198",  "11059", "11029")
