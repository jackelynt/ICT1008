import csv
import pandas
import math
from BusStop import BusStop
class BusStopTable:
    busStopDic = {}

    def __init__(self):
        busRouteDF = pandas.read_csv("BusRoute.csv")
        print(busRouteDF)
        busStopDF = pandas.read_csv("BusStop.csv")
        for index, row in busRouteDF.iterrows():
            if row["BusStopCode"] in self.busStopDic.keys():
                self.busStopDic[row["BusStopCode"]].addBusService(row["BusStopCode"] ,row["ServiceNo"])
            else:
                self.busStopDic[row["BusStopCode"]] = BusStop(row["BusStopCode"] ,[row["ServiceNo"]])
        busStopDF = pandas.read_csv("BusStop.csv")

        for index, row in busStopDF.iterrows():
            if row["BusStopCode"] in self.busStopDic.keys():
                self.busStopDic[row["BusStopCode"]].addXY(row["Latitude"], row["Longitude"])
                self.busStopDic[row["BusStopCode"]].addDesc(row["Description"])
            

    def searchBusStop(self, BusStopNum):
        #print(self.busStopDic[BusStopNum].busServiceList)
        return self.busStopDic[BusStopNum].busServiceList
    
    def searchBusStopXY(self, BusStopNum):
        return self.busStopDic[BusStopNum].getXY()

    def getClosestBusStop(self, Latitude, Longitude):
        busStopCloseBusStop = -1
        shortDistance = 99999999
        #print(Latitude)
        #print(Longitude)
        for busstop in self.busStopDic.keys():
            
            distance =  (Latitude - self.busStopDic[busstop].Latitude)**2 + (Longitude-self.busStopDic[busstop].Longitude)**2
            print(distance)
            distance = math.sqrt(distance) 
            if distance < shortDistance: 
                shortDistance = distance
                busStopCloseBusStop = busstop

        return busStopCloseBusStop 

#busstoptable = BusStopTable()