import csv
import pandas
import copy
from BusStop import BusStop
from BusStopTable import BusStopTable
from BusService import BusService
from BusServiceTable import BusServiceTable
from BusStopRoute import BusStopRoute

def BusRouteAlg(startBusStopID, destinationBusStopID):
    busstoptable = BusStopTable()
    busservicetable = BusServiceTable()
    
    busStopRoutes = {}
    tobesearchedBusStop = []
    searchedServiceNo = []
    #bus stop routes prepared
    for stops in busstoptable.busStopDic.keys():
        #print(stops)
        busStopRoutes[stops] = None
    #find the bus services available from starting bus stop....
    start_service = busstoptable.searchBusStop(startBusStopID)
    for services in start_service:
        #find bus stops available for to travel to on this bus services
        service_bus_stop_1 = busservicetable.serviceNoBusStop(services, startBusStopID)
        for busStop in service_bus_stop_1:
            #route not available
            if busStopRoutes[busStop] is None:
                #create route object
                busStopList = busservicetable.searchServiceNoStartStop(services,startBusStopID, busStop)
                serviceList = [services]
                changingBusStop = [startBusStopID]
                distance = busservicetable.searchServiceNoDistanceBetweenBusStop(services, startBusStopID, busStop)
                #print(busStop)
                #print(busStopList)
                #print(serviceList)
                #print(changingBusStop)
                #print("Disance:",distance)
                
                busStopRoutes[busStop] = BusStopRoute(busStopList, serviceList, changingBusStop, distance)
                #if busStop == destinationBusStopID:
                #    print(busStopRoutes[busStop].serviceList)
                tobesearchedBusStop.append(busStop)
            else:
                pass
        #bus service used will not be used again in an route
        searchedServiceNo.append(services)
        #print("Service No: ", services, "completed")
    tobesearchedBusStop.remove(startBusStopID)
    #print(tobesearchedBusStop)

    while len(tobesearchedBusStop) > 0:
        #finding available route in next breadth
        for startingbusStop in tobesearchedBusStop:
            #check is the previous route information available
            if busStopRoutes[startingbusStop] is not None:
                #busStopRoutes[startingbusStop].printRouteInfo()
                #search bus service on bus stop
                bus_stop_services = []
                bus_stop_services = busstoptable.searchBusStop(startingbusStop)
                #remove any bus service used
                for searchedServices in searchedServiceNo:
                    if searchedServices in bus_stop_services:
                        bus_stop_services.remove(searchedServices)
                
                #print("Bus Stop: ", startingbusStop)
                #print("Bus Stop Service: ", bus_stop_services)
                #new service is found
                for services in bus_stop_services:
                    if services not in searchedServiceNo:
                        service_bus_stop_1 = busservicetable.serviceNoBusStop(services,startingbusStop)
                        for busStop in service_bus_stop_1:
                            if busStopRoutes[busStop] is None:
                                #busStopRoutes[startingbusStop].printRouteInfo()
                                busStopList = []
                                busStopList = copy.deepcopy(busStopRoutes[startingbusStop].busStopList)
                                busStopList.extend(busservicetable.searchServiceNoStartStop(services,startingbusStop, busStop))
                                busStopList = list(dict.fromkeys(busStopList))
                                serviceList = []
                                serviceList = copy.deepcopy(busStopRoutes[startingbusStop].serviceList)
                                serviceList.append(services)
                                changingBusStop = []
                                changingBusStop = copy.deepcopy(busStopRoutes[startingbusStop].changingBusStop)
                                changingBusStop.append(startingbusStop)
                                distance = busStopRoutes[startingbusStop].distance + busservicetable.searchServiceNoDistanceBetweenBusStop(services, startingbusStop, busStop)
                                busStopRoutes[busStop] = BusStopRoute(busStopList,serviceList,changingBusStop, distance)
                                #busStopRoutes[busStop].printRouteInfo()
                                if busStop not in tobesearchedBusStop:
                                    tobesearchedBusStop.append(busStop)
                            else:
                                pass

                        searchedServiceNo.append(services)
                tobesearchedBusStop.remove(startingbusStop)

    routeFile = open("BusStopRoute.txt", "w")
    for busStop in busStopRoutes.keys():
        busstopListxy = []
        if busStopRoutes[busStop] is not None:
            for busStopXY in busStopRoutes[busStop].busStopList:
                busstopListxy.append(busstoptable.searchBusStopXY(busStopXY))
            bussstopxy = list(reversed(busstopListxy))
            #print(bussstopxy)
            routeFile.writelines(str(busStop) + " : " + str(busstopListxy) + "\n")

    print(str(destinationBusStopID) + " : " + str(busStopRoutes[destinationBusStopID].busStopList))
    busstopListxy = []
    for busStopXY in busStopRoutes[destinationBusStopID].busStopList:
        tmp_xyList = ["Bus",busstoptable.busStopDic[busStopXY].busStopDesc]
        tmp_xyList.extend(busstoptable.searchBusStopXY(busStopXY))
        busstopListxy.append(tmp_xyList)
        bussstopxy = list(reversed(busstopListxy))
        
    print(busstopListxy)
    return busstopListxy






