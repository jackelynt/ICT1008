import math

import pandas as pd

EARTH_RADIUS = 6373.0 # use for calculation of distance later


# Bus stop nodes
class BusStop:
    """A class for Bus Stop nodes.
       Contains: latitude, longitude, busStopNumber, next"""
    latitude = -1
    longitude = -1
    busStopNumber = -1
    next = None

    def __init__(self, latitude, longitude, busStopNumber):
        self.latitude = latitude
        self.longitude = longitude
        self.busStopNumber = busStopNumber


# HDB nodes
class HDB:
    """A class for HDB nodes.
    Contains: latitude, longitude, block_number, road_Name, postal_Code, accomplice (A list to store all adjacent HDB nodes),
    adjBusStop (A list to store all adjacent Bus Stop nodes), next"""
    latitude = -1
    longitude = -1
    block_number = -1
    road_Name = ""
    postal_Code = -1
    accomplice = []
    adjBusStop = []
    next = None

    def __init__(self, latitude, longitude, block_number, road_Name, postal_Code):
        self.latitude = latitude
        self.longitude = longitude
        self.block_number = block_number
        self.road_Name = road_Name
        self.postal_Code = postal_Code

# Coordinate nodes, used to contain latitude and longitude of each HDB node
class Coordinate:
    """A class for HDB Coordinate nodes.
        Contains: Value (Usually the opposite the type of list you store in. E.g. Longitude list, values will be latitude), postal_Code, next"""
    value = -1
    postal_Code = -1
    next = None

    def __init__(self, value, postal_Code):
        self.value = value
        self.postal_Code = postal_Code

# Coordinate nodes, similar to HDB, used to contain the latitude and longitude of each Bus stop node
class BusCoordinate:
    """A class for Bus Coordinate nodes.
    Contains: Value (Usually the opposite the type of list you store in. E.g. Longitude list, values will be latitude), coordinate_Bus_Stop_Number, next"""
    value = -1
    coordinate_Bus_Stop_Number = -1
    next = None

    def __init__(self, value, bus_Stop_Number):
        self.value = value
        self.coordinate_Bus_Stop_Number = bus_Stop_Number


# Edge node to store all edges between HDB to HDB nodes or HDB to Bus nodes
class edge:
    """A class for Edge nodes. NOTE: Only have default constructor. All values have to be self assigned.
    Contains: Destination(Destination postal code / Bus Stop Number), Distance, next"""
    destination = -1
    distance = -1
    next = None
    # No self-defined constructor

# This is the main class that stores and maps all HDB nodes and Bus nodes together
class HDBMap:
    """Class that contains the map of all HDB nodes and Bus Stop nodes. Purpose is to populate a map. Use with together with HDBEdge object
    to do routing on this map."""
    HDB_Data = {}
    Longitude_Data = {}
    Latitude_Data = {}
    Bus_Data = {}
    Bus_Longitude_Data = {}
    Bus_Latitude_Data = {}

    # Add a new HDB node into the HDB_Data dictionary by using hash chaining.
    def addHDB(self, HDB):
        """A function to add HDB node to the map and populate the map with it's data. Returns no value. Supply HDB node."""
        tmp_postalcode = str(HDB.postal_Code)
        postal_Code_1stPortion = tmp_postalcode[0:3]

        if postal_Code_1stPortion not in self.HDB_Data.keys():
            linkedList = SinglyLinkedList(HDB)
            self.HDB_Data[postal_Code_1stPortion] = linkedList

            LongitudeNode = Coordinate(round(float(HDB.latitude), 3), HDB.postal_Code)
            if round(float(HDB.longitude), 3) not in self.Longitude_Data.keys():
                LongitudeList = SinglyLinkedNode(LongitudeNode)
                self.Longitude_Data[round(float(HDB.longitude), 3)] = LongitudeList
            else:
                self.Longitude_Data[round(float(HDB.longitude), 3)].addNode(LongitudeNode)

            LatitudeNode = Coordinate(round(float(HDB.longitude), 3), HDB.postal_Code)
            if round(float(HDB.latitude), 3) not in self.Latitude_Data.keys():
                LatitudeList = SinglyLinkedNode(LatitudeNode)
                self.Latitude_Data[round(float(HDB.latitude), 3)] = LatitudeList
            else:
                self.Latitude_Data[round(float(HDB.latitude), 3)].addNode(LatitudeNode)

        else:
            self.HDB_Data[postal_Code_1stPortion].addNode(HDB)

            LongitudeNode = Coordinate(round(float(HDB.latitude), 3), HDB.postal_Code)
            if round(float(HDB.longitude), 3) not in self.Longitude_Data.keys():
                LongitudeList = SinglyLinkedNode(LongitudeNode)
                self.Longitude_Data[round(float(HDB.longitude), 3)] = LongitudeList
            else:
                self.Longitude_Data[round(float(HDB.longitude), 3)].addNode(LongitudeNode)

            LatitudeNode = Coordinate(round(float(HDB.longitude), 3), HDB.postal_Code)
            if round(float(HDB.latitude), 3) not in self.Latitude_Data.keys():
                LatitudeList = SinglyLinkedNode(LatitudeNode)
                self.Latitude_Data[round(float(HDB.latitude), 3)] = LatitudeList
            else:
                self.Latitude_Data[round(float(HDB.latitude), 3)].addNode(LatitudeNode)


    # Add a bus stop node into the map together with populating the map its coordinates
    def addBus(self, Bus):
        """Function to add bus stop node into the map and populate all its data into the map. Returns no value. Supply Bus stop node."""
        self.Bus_Data[Bus.busStopNumber] = Bus

        LongitudeNode = BusCoordinate(round(float(Bus.latitude), 3), Bus.busStopNumber)
        if round(float(Bus.longitude), 3) not in self.Bus_Longitude_Data.keys():
            LongitudeList = SinglyLinkedNode(LongitudeNode)
            self.Bus_Longitude_Data[round(float(Bus.longitude), 3)] = LongitudeList
        else:
            self.Bus_Longitude_Data[round(float(Bus.longitude), 3)].addNode(LongitudeNode)

        LatitudeNode = BusCoordinate(round(float(Bus.longitude), 3), Bus.busStopNumber)
        if round(float(Bus.latitude), 3) not in self.Bus_Latitude_Data.keys():
            LatitudeList = SinglyLinkedNode(LatitudeNode)
            self.Bus_Latitude_Data[round(float(Bus.latitude), 3)] = LatitudeList
        else:
            self.Bus_Latitude_Data[round(float(Bus.latitude), 3)].addNode(LatitudeNode)

    # Function to remove a wrongly added HDB node and to remove all its data from the map
    def removeHDB(self, HDB):
        """Function to remove wrongly added HDB node and remove all its data from the map. Return 0 is successful, -1 if failure.
        Supply a HDB node to be removed."""
        tmp_postalcode = str(HDB.postal_Code)
        postal_Code_1stPortion = tmp_postalcode[0:3]

        if postal_Code_1stPortion in self.HDB_Data.keys():
            head = self.HDB_Data[postal_Code_1stPortion].head
            temp = head
            prev = temp
            while temp.postal_code != HDB.postal_Code:
                prev = temp
                temp = temp.next

            prev.next = temp.next
            temp.postal_code = None

            head = self.Longitude_Data[round(float(HDB.longitude), 3)].head
            temp = head
            prev = temp
            while temp.postal_Code != HDB.postal_Code:
                prev = temp
                temp = temp.next

            prev.next = temp.next

            head = self.Latitude_Data[round(float(HDB.latitude), 3)].head
            temp = head
            prev = temp
            while temp.postal_Code != HDB.postal_Code:
                prev = temp
                temp = temp.next

            prev.next = temp.next
            return 0

        else:
            return -1

    def removeBus(self, Bus):
        """Function to remove a bus stop node from the map and all its data from the map. Return 0 if successful, -1 if failure. Supply bus stop node."""
        tmp_busStopNumber = str(Bus.busStopNumber)
        if tmp_busStopNumber in self.Bus_Data.keys():
            self.Bus_Data[tmp_busStopNumber] = None

            head = self.Bus_Latitude_Data[round(float(Bus.latitude), 3)].head
            temp = head
            prev = temp
            while temp.coordinate_Bus_Stop_Number != Bus.busStopNumber:
                prev = temp
                temp = temp.next

            prev.next = temp.next

            head = self.Bus_Longitude_Data[round(float(Bus.longitude), 3)].head
            temp = head
            prev = temp
            while temp.coordinate_Bus_Stop_Number != Bus.busStopNumber:
                prev = temp
                temp = temp.next

            prev.next = temp.next
            return 0
        else:
            return -1

    def updateHDB(self, HDB, updatedList, updatedBus):
        """Function to update HDB nodes's adjacency lists within the map and overwrite the old values for the node. Returns no value. Supply HDB node,
        new updated HDB adjacency list, new updated Bus stop adjacency list."""
        tmp_postalcode = str(HDB.postal_Code)
        postal_Code_1stPortion = tmp_postalcode[0:3]
        if postal_Code_1stPortion in self.HDB_Data.keys():
            head = self.HDB_Data[postal_Code_1stPortion].head
            temp = head

            # print(temp.postal_Code)

            while (temp.postal_Code != HDB.postal_Code and temp.next != None):
                temp = temp.next
        temp.accomplice = []
        temp.adjBusStop = []
        # print("Before", temp.accomplice)
        for item in updatedList:
            if item not in temp.accomplice and item != temp.postal_Code:
                temp.accomplice.append(item)
        if temp.postal_Code in temp.accomplice:
            temp.accomplice.remove(temp.postal_Code)

        for item in updatedBus:
            if item not in temp.adjBusStop:
                temp.adjBusStop.append(item)

        # print("Accomplice", temp.accomplice)
        # print("Adjacent bus stops", temp.adjBusStop)

    def findAdjacency(self, HDB):
        """Function to find adjacent HDB and Bus Stop nodes based on latitude and longitude for a specific HDB node.
        Supply HDB node that needs to find its adjacency"""
        longitude = round(float(HDB.longitude), 3)
        latitude = round(float(HDB.latitude), 3)

        AssosiatedHDB = []
        AssosiatedBus = []

        for i in range(1, 2):
            Start = [round(longitude + (i / 1000), 3), latitude]

            right = [Start[0], Start[1]]
            left = [round(Start[0] - (i / 1000) - (i / 1000), 3), Start[1]]
            top = [round(Start[0] - (i / 1000), 3), round(Start[1] + (i / 1000), 3)]
            bottom = [round(Start[0] - (i / 1000), 3), round(Start[1] - (i / 1000), 3)]

            endingPoint = [Start[0], Start[1]]

            # Check top corner
            # print("Top conner",top)
            while Start[1] < top[1]:
                Start[1] = round(Start[1] + round((1 / 1000), 3), 3)
                if Start[1] in self.Latitude_Data.keys():
                    temptc = self.Latitude_Data[Start[1]].head
                    while temptc is not None:
                        if Start[0] == temptc.value or Start[0] == (temptc.value + 0.001) or Start[0] == (
                                temptc.value - 0.001):
                            tempholder = temptc.postal_Code
                            if (tempholder not in AssosiatedHDB and tempholder != HDB.postal_Code):
                                AssosiatedHDB.append(tempholder)
                                # first3Num = str(tempholder)[0:3]
                                # linkedList = self.HDB_Data[first3Num]
                                # node = linkedList.head
                                # while node != None:
                                #     if node.postal_Code == tempholder:
                                #         if HDB.postal_Code not in node.accomplice:
                                #             node.accomplice.append(HDB.postal_Code)
                                #             node = None
                                #         break
                                #     else:
                                #         node = node.next
                            temptc = temptc.next
                        else:
                            temptc = temptc.next

                # Top corner for bus stop
                if Start[1] in self.Bus_Latitude_Data.keys():
                    bustc = self.Bus_Latitude_Data[Start[1]].head
                    while bustc is not None:
                        if Start[0] == bustc.value or Start[0] == (bustc.value + 0.001) or Start[0] == (
                                bustc.value - 0.001):
                            if bustc.coordinate_Bus_Stop_Number not in AssosiatedBus:
                                AssosiatedBus.append(bustc.coordinate_Bus_Stop_Number)
                            bustc = bustc.next
                        else:
                            bustc = bustc.next

            # Check top row
            # print("Top  row", left)
            while Start[0] > left[0]:
                Start[0] = round(Start[0] - round((1 / 1000), 3), 3)
                if Start[0] in self.Longitude_Data.keys():
                    temptr = self.Longitude_Data[Start[0]].head
                    while temptr is not None:
                        if Start[1] == temptr.value or Start[1] == (temptr.value + 0.001) or Start[1] == (
                                temptr.value - 0.001):
                            tempholder = temptr.postal_Code
                            if (tempholder not in AssosiatedHDB and tempholder != HDB.postal_Code):
                                AssosiatedHDB.append(tempholder)
                                # first3Num = str(tempholder)[0:3]
                                # linkedList = self.HDB_Data[first3Num]
                                # node = linkedList.head
                                # while node != None:
                                #     if node.postal_Code == tempholder:
                                #         if HDB.postal_Code not in node.accomplice:
                                #             node.accomplice.append(HDB.postal_Code)
                                #             node = None
                                #         break
                                #     else:
                                #         node = node.next
                            temptr = temptr.next
                        else:
                            temptr = temptr.next

                # Top row bus stop
                if Start[0] in self.Bus_Longitude_Data.keys():
                    bustr = self.Bus_Longitude_Data[Start[0]].head
                    while bustr is not None:
                        if Start[1] == bustr.value or Start[1] == (bustr.value + 0.001) or Start[1] == (
                                bustr.value - 0.001):
                            if (bustr.coordinate_Bus_Stop_Number not in AssosiatedBus):
                                AssosiatedBus.append(bustr.coordinate_Bus_Stop_Number)
                            bustr = bustr.next
                        else:
                            bustr = bustr.next

            # Check bottom left corner
            # print("Bottomw corner", bottom)
            while Start[1] > bottom[1]:
                Start[1] = round(Start[1] - round((1 / 1000), 3), 3)
                if Start[1] in self.Latitude_Data.keys():
                    tempbc = self.Latitude_Data[Start[1]].head
                    while tempbc is not None:
                        if (Start[0] == tempbc.value or Start[0] == (tempbc.value + 0.001) or Start[0] == (
                                tempbc.value - 0.001)):
                            tempholder = tempbc.postal_Code
                            if (tempholder not in AssosiatedHDB and tempholder != HDB.postal_Code):
                                AssosiatedHDB.append(tempholder)
                                # first3Num = str(tempholder)[0:3]
                                # linkedList = self.HDB_Data[first3Num]
                                # node = linkedList.head
                                # while node != None:
                                #     if node.postal_Code == tempholder:
                                #         if HDB.postal_Code not in node.accomplice:
                                #             node.accomplice.append(HDB.postal_Code)
                                #             node = None
                                #         break
                                #     else:
                                #         node = node.next
                            tempbc = tempbc.next
                        else:
                            tempbc = tempbc.next

                # Bottom corner bus stop
                if Start[1] in self.Bus_Latitude_Data.keys():
                    busbc = self.Bus_Latitude_Data[Start[1]].head
                    while busbc is not None:
                        if (Start[0] == busbc.value or Start[0] == (busbc.value + 0.001) or Start[0] == (
                                busbc.value - 0.001)):
                            if (busbc.coordinate_Bus_Stop_Number not in AssosiatedBus):
                                AssosiatedBus.append(busbc.coordinate_Bus_Stop_Number)
                            busbc = busbc.next
                        else:
                            busbc = busbc.next

            # Check bottom row
            # print("Bottom row", right)
            while Start[0] < right[0]:
                Start[0] = round(Start[0] + round((1 / 1000), 3), 3)
                if Start[0] in self.Longitude_Data.keys():
                    tempbr = self.Longitude_Data[Start[0]].head
                    while tempbr is not None:
                        if (Start[1] == tempbr.value or Start[1] == (tempbr.value + 0.001) or Start[1] == (
                                tempbr.value - 0.001)):
                            tempholder = tempbr.postal_Code
                            if (tempholder not in AssosiatedHDB and tempholder != HDB.postal_Code):
                                AssosiatedHDB.append(tempholder)
                                # first3Num = str(tempholder)[0:3]
                                # linkedList = self.HDB_Data[first3Num]
                                # node = linkedList.head
                                # while node != None:
                                #     if node.postal_Code == tempholder:
                                #         if HDB.postal_Code not in node.accomplice:
                                #             node.accomplice.append(HDB.postal_Code)
                                #             node = None
                                #         break
                                #     else:
                                #         node = node.next
                            tempbr = tempbr.next
                        else:
                            tempbr = tempbr.next

                # Check bottom row bus stop
                if Start[0] in self.Bus_Longitude_Data.keys():
                    busbr = self.Bus_Longitude_Data[Start[0]].head
                    while busbr is not None:
                        if (Start[1] == busbr.value or Start[1] == (busbr.value + 0.001) or Start[1] == (
                                busbr.value - 0.001)):
                            if (busbr.coordinate_Bus_Stop_Number not in AssosiatedBus):
                                AssosiatedBus.append(busbr.coordinate_Bus_Stop_Number)
                            busbr = busbr.next
                        else:
                            busbr = busbr.next

            # Check to back of starting point
            # print("Back  to  start", endingPoint)
            while Start[1] < endingPoint[1]:
                Start[1] = round(Start[1] + round((1 / 1000), 3), 3)
                if Start[1] in self.Latitude_Data.keys():
                    tempbts = self.Latitude_Data[Start[1]].head
                    while tempbts is not None:
                        if (Start[0] == tempbts.value or Start[0] == (tempbts.value + 0.001) or Start[0] == (
                                tempbts.value - 0.001)):
                            tempholder = tempbts.postal_Code
                            if (tempholder not in AssosiatedHDB and tempholder != HDB.postal_Code):
                                AssosiatedHDB.append(tempholder)
                                # first3Num = str(tempholder)[0:3]
                                # linkedList = self.HDB_Data[first3Num]
                                # node = linkedList.head
                                # while node != None:
                                #     if node.postal_Code == tempholder:
                                #         if HDB.postal_Code not in node.accomplice:
                                #             node.accomplice.append(HDB.postal_Code)
                                #             node = None
                                #         break
                                #     else:
                                #         node = node.next
                            tempbts = tempbts.next
                        else:
                            tempbts = tempbts.next

                # Check back to start bus stop
                if Start[1] in self.Bus_Latitude_Data.keys():
                    busbts = self.Bus_Latitude_Data[Start[1]].head
                    while busbts is not None:
                        if (Start[0] == busbts.value or Start[0] == (busbts.value + 0.001) or Start[0] == (
                                busbts.value - 0.001)):
                            if (busbts.coordinate_Bus_Stop_Number not in AssosiatedBus):
                                AssosiatedBus.append(busbts.coordinate_Bus_Stop_Number)
                            busbts = busbts.next
                        else:
                            busbts = busbts.next

        # a = []
        # for x in range(0, len(AssosiatedHDB)):
        #     element = AssosiatedHDB[x]
        #     a.append(element)
        # b = set()
        # unique = []
        # for x in a:
        #     if x not in b:
        #         unique.append(x)
        #         b.add(x)
        # print("AssociatedHDB: ", AssosiatedHDB)
        # print("AssociatedBus: ", AssosiatedBus)
        self.updateHDB(HDB, AssosiatedHDB, AssosiatedBus)

    # def HDBrouting(self, src, dest, outward):
    #     chosenRoute = []
    #     srcLatitude = src.latitude
    #     srcLongitude = src.longitude
    #
    #     while (srcLatitude != dest.latitude and srcLongitude != dest.longitude):
    #


class HDBEdges:
    """Class that contains all edges and their distances. This class contains all routing functions for a HDBMap objects
    Use together with a HDBMap object for routing."""
    edges = {}
    busStops = {}

    def addEdge(self, postal_Code):
        """Populate the edges connected to a HDB node from a HBDMap object. Returns no value. Supply postal code of the HDB node."""
        first3Num = str(postal_Code)[0:3]
        linkedList = HDBMap.HDB_Data[first3Num]
        node = linkedList.head
        while node != None:
            if (node.postal_Code == postal_Code):
                break
            else:
                node = node.next
        if node != None:
            for items in node.accomplice:
                if (items != None):
                    distance = self.calDistance(node.postal_Code, items)
                    newEdge = edge()
                    newEdge.distance = round(float(distance), 4)
                    newEdge.destination = items
                    if postal_Code not in self.edges.keys():
                        edgeList = SinglyLinkedNode(newEdge)
                        self.edges[postal_Code] = edgeList
                    else:
                        self.edges[postal_Code].addNode(newEdge)

            for items in node.adjBusStop:
                if (items != None):
                    distance = self.calBusStopDistance(node.postal_Code, items)
                    newBusEdge = edge()
                    newBusEdge.distance = round(float(distance), 4)
                    newBusEdge.destination = items
                    # print(postal_Code)
                    # print(self.busStops.keys())
                    if postal_Code not in self.busStops.keys():
                        busEdgeList = SinglyLinkedNode(newBusEdge)
                        self.busStops[postal_Code] = busEdgeList
                    else:
                        self.busStops[postal_Code].addNode(newBusEdge)

        # temp = self.edges[postal_Code].head
        # while (temp != None):
        #     print("edges destination: ", temp.destination, " edges distance: ", temp.distance)
        #     temp = temp.next

    def calDistance(self, postal_Code1, postal_Code2):
        """Makes use of haversine formula to determine the distance between two HDB nodes in the same HDBMap object. Returns the distance as a float.

        Supply both HDB node's postal code."""
        PC1 = str(postal_Code1)[0:3]
        PC2 = str(postal_Code2)[0:3]
        list1 = HDBMap.HDB_Data[PC1]
        node1 = list1.head
        list2 = HDBMap.HDB_Data[PC2]
        node2 = list2.head
        while node1 != None:
            if (node1.postal_Code == postal_Code1):
                break
            else:
                node1 = node1.next

        while node2 != None:
            if (node2.postal_Code == postal_Code2):
                break
            else:
                node2 = node2.next

        lat1 = math.radians(node1.latitude)
        lon1 = math.radians(node1.longitude)
        lat2 = math.radians(node2.latitude)
        lon2 = math.radians(node2.longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = EARTH_RADIUS * c

        # print(distance)
        return distance

    def calBusStopDistance(self, postal_Code, bus_Stop_Number):
        """Makes use of haversine formula to determine the distance between one HDB nodes and one Bus Stop node in the same HDBMap object.
        Returns the distance as a float.
        Supply the HDB node's postal code and the Bus Stop node's bus stop number."""
        PC = str(postal_Code)[0:3]
        HDBList = HDBMap.HDB_Data[PC]
        HDBNode = HDBList.head

        while HDBNode != None:
            if (HDBNode.postal_Code == postal_Code):
                break
            else:
                HDBNode = HDBNode.next

        HDBLatitude = HDBNode.latitude
        HDBLongitude = HDBNode.longitude

        BusNode = HDBMap.Bus_Data[bus_Stop_Number]
        BusLatitude = BusNode.latitude
        BusLongitude = BusNode.longitude

        lat1 = math.radians(HDBLatitude)
        lon1 = math.radians(HDBLongitude)
        lat2 = math.radians(BusLatitude)
        lon2 = math.radians(BusLongitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = EARTH_RADIUS * c

        return distance

    def AstarRouting(self, sourcePostalCode, dlat, dlong):  # backward searching. From  HDB to the best bus stop
        """Function to routing on a HDBMap object based on A* algorithm and provide a optimised route to transverse from a HDB node to a
        Destination MRT/LRT station.
        Returns a list containing latitude and longitude value of HDB and Bus Stop nodes in sequence to route you to a bus stop that
        can bring you to the MRT station.
        Supply Source HDB postal code and MRT station's latitude and longitude"""

        sequence = []
        seen = []
        OriginalDistance = -1

        destLatitude = round(float(dlat), 3)
        destLongitude = round(float(dlong), 3)

        # find the best bus stop to go to
        first3Num = str(sourcePostalCode)[0:3]
        linkedList = hdbMap.HDB_Data[first3Num]
        node = linkedList.head
        while node != None:
            # print(type(node.postal_Code))
            # print("Source: ", type(sourcePostalCode))
            if (node.postal_Code == str(sourcePostalCode)):
                break
            else:
                node = node.next
        # Found the HDB node
        print(node)


        # Find destination values
        lat1 = math.radians(destLatitude)
        lon1 = math.radians(destLongitude)

        # Find original distance between HDB and MRT
        lat2 = math.radians(node.latitude)
        lon2 = math.radians(node.longitude)
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        OriginalDistance = EARTH_RADIUS * c

        print("Original distance from dest to src: ", OriginalDistance)

        # Search for the bus stop to go to
        heuristicValue = -1
        edgeCost = -1
        selectedBusStop = None

        for items in node.adjBusStop:
            if (items != None):  # Some HDB do  not have any adj bus stop
                if (heuristicValue == -1):
                    temp = self.busStops[node.postal_Code].head
                    while temp != None:
                        if temp.destination == items:
                            edgeCost = temp.distance
                            BusNode = HDBMap.Bus_Data[items]
                            BusLatitude = BusNode.latitude
                            BusLongitude = BusNode.longitude

                            lat2 = math.radians(BusLatitude)
                            lon2 = math.radians(BusLongitude)

                            dlon = lon2 - lon1
                            dlat = lat2 - lat1

                            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
                            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                            distance = EARTH_RADIUS * c

                            thisValue = OriginalDistance - distance  # Technically is the distance able to be covered if take this route
                            heuristicValue = thisValue/edgeCost
                            selectedBusStop = BusNode
                            # print("bus stop choosing heuristic: ", heuristicValue)
                            # print("Selected bus stop  numb", BusNode.busStopNumber)
                            break
                        else:
                            temp = temp.next

                else:
                    temp = self.busStops[node.postal_Code].head
                    while temp != None:
                        if temp.destination == items:
                            edgeCost = temp.distance
                            BusNode = HDBMap.Bus_Data[items]
                            BusLatitude = BusNode.latitude
                            BusLongitude = BusNode.longitude

                            lat2 = math.radians(BusLatitude)
                            lon2 = math.radians(BusLongitude)

                            dlon = lon2 - lon1
                            dlat = lat2 - lat1

                            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
                            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                            distance = EARTH_RADIUS * c

                            thisValue = (OriginalDistance - distance)/edgeCost
                            if (thisValue > heuristicValue):
                                heuristicValue = thisValue
                                selectedBusStop = BusNode
                            # print("bus stop choosing heuristic: ", heuristicValue)
                            # print("Selected bus stop  numb", BusNode.busStopNumber)
                            break

                        else:
                            temp = temp.next

            else:
                print("No bus stop nearby")

        print("Final selected bus stop numb : ", selectedBusStop.busStopNumber)
        busStopData = []
        busStopData.append("Bus stop number")
        busStopData.append(selectedBusStop.busStopNumber)
        sequence.append(busStopData)


        first3digit = str(sourcePostalCode)[0:3]
        StartNode = HDBMap.HDB_Data[first3digit].head
        # print(type(sourcePostalCode))
        while StartNode != None:
            print("StartNode: ", StartNode.postal_Code)
            if (StartNode.postal_Code == str(sourcePostalCode)):
                break
            else:
                StartNode = StartNode.next

        startLongitude = StartNode.longitude
        startLatitude = StartNode.latitude
        startlist = []
        startlist.append("HDB")
        startlist.append(StartNode.block_number)
        startlist.append(startLongitude)
        startlist.append(startLatitude)

        sequence.append(startlist)
        seen.append("HDB")
        seen.append(sourcePostalCode)

        selectedHDB = node
        lastSeenNode = selectedHDB
        # starter = True
        while (True):
            # Search for route to go to selectedBusStop
            heuristicValue = -1
            edgeCost = -1
            node = selectedHDB


            lat1 = math.radians(selectedBusStop.latitude)
            lon1 = math.radians(selectedBusStop.longitude)
            lat2 = math.radians(selectedHDB.latitude)
            lon2 = math.radians(selectedHDB.longitude)
            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            HDBBUSDistance = EARTH_RADIUS * c

            if(HDBBUSDistance < 0.1):
                break


            for items in node.accomplice:
                if (items in seen):
                    continue
                # print("Looking at postal: ", items)
                if (items != None):
                    if (heuristicValue == -1):
                        temp = self.edges[node.postal_Code].head
                        while temp != None:
                            if temp.destination == items:
                                edgeCost = temp.distance
                                first3digit = str(items)[0:3]
                                HDBNode = HDBMap.HDB_Data[first3digit].head
                                while HDBNode != None:
                                    if (HDBNode.postal_Code == items):
                                        break
                                    else:
                                        HDBNode = HDBNode.next
                                HDBLatitude = HDBNode.latitude
                                HDBLongitude = HDBNode.longitude

                                lat2 = math.radians(HDBLatitude)
                                lon2 = math.radians(HDBLongitude)

                                dlon = lon2 - lon1
                                dlat = lat2 - lat1

                                a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
                                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                                distance = EARTH_RADIUS * c

                                thisValue = HDBBUSDistance - distance  # Technically is the distance able to be covered if take this route
                                heuristicValue = thisValue/(edgeCost*edgeCost)
                                selectedHDB = HDBNode
                                break
                            else:
                                temp = temp.next

                    else:
                        temp = self.edges[node.postal_Code].head
                        while temp != None:
                            if temp.destination == items:
                                edgeCost = temp.distance
                                first3digit = str(items)[0:3]
                                HDBNode = HDBMap.HDB_Data[first3digit].head
                                while HDBNode != None:
                                    if (HDBNode.postal_Code == items):
                                        break
                                    else:
                                        HDBNode = HDBNode.next
                                HDBLatitude = HDBNode.latitude
                                HDBLongitude = HDBNode.longitude

                                lat2 = math.radians(HDBLatitude)
                                lon2 = math.radians(HDBLongitude)

                                dlon = lon2 - lon1
                                dlat = lat2 - lat1

                                a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
                                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                                distance = EARTH_RADIUS * c

                                thisValue = (HDBBUSDistance - distance)/(edgeCost*edgeCost)

                                if (thisValue > heuristicValue):
                                    print("For postal: ", HDBNode.postal_Code, " has the heuristic value of :",
                                          thisValue)
                                    heuristicValue = thisValue
                                    selectedHDB = HDBNode
                                break

                            else:
                                temp = temp.next

            print("Selected: ", selectedHDB.postal_Code)
            if(lastSeenNode != selectedHDB):
                hdblist = []
                hdblist.append("HDB")
                hdblist.append(selectedHDB.block_number)
                hdblist.append(selectedHDB.longitude)
                hdblist.append(selectedHDB.latitude)
                sequence.append(hdblist)
                print("Appending: ", selectedHDB.postal_Code)
                seen.append("HDB")
                seen.append(selectedHDB.postal_Code)
                lastSeenNode = selectedHDB

            # elif(starter == True):
            #     sequence.append(selectedHDB.longitude)
            #     sequence.append(selectedHDB.latitude)
            #     sequence.append("HDB")
            #     print("Appending: ", selectedHDB.postal_Code)
            #     seen.append(selectedHDB.postal_Code)
            #     seen.append("HDB")
            #     lastSeenNode = selectedHDB
            #     starter = False
            else:
                break

        buslist = []
        buslist.append("Bus")
        buslist.append("Destination bus stop")
        buslist.append(selectedBusStop.longitude)  # add this bus stop node into our sequence of route
        buslist.append(selectedBusStop.latitude)
        sequence.append(buslist)
        seen.append("Bus")
        seen.append(selectedBusStop.busStopNumber)
        # seen.reverse()
        print(seen)
        sequence.reverse()
        return sequence


class SinglyLinkedList:
    """A linked list class to store HDB nodes / Bus nodes"""
    head = None

    def __init__(self, node):
        self.head = node

    def addNode(self, node):
        """A function to add a new node into the list. Returns no value. Supply the new node."""
        node.next = self.head
        self.head = node

    def removeCoordinates(self, value):
        """A function that search for a Coordinate node with the same value supplied and
        remove that node from the list. Use together with a  HDBEdge object.
        Returns no value.
        Supply the value to search for and remove (Usually postal code/bus stop number)"""
        temp = self.head
        prev = None

        while (temp.next != None):
            if (temp == temp.next):
                prev.next = temp.next

            prev = temp
            temp = temp.next

    def removeHDBNode(self, node):
        """A function that search for a HDB node and
        remove that node from the list. Use together with a  HDBMap object.
        Returns no value.
        Supply the HDB node to remove."""
        temp = self.head
        prev = None

        while (temp.next != None):
            if (temp.postal_code == (node.postal_code)):
                prev.next = temp.next

            prev = temp
            temp = temp.next


class SinglyLinkedNode:
    """A linked list class to store coordinate nodes"""
    head = None

    def __init__(self, node):
        self.head = node

    def addNode(self, node):
        """A function to add a new Coordinate node into the linked list. Returns no value. Supply new Coordinate node to add into the list."""
        node.next = self.head
        self.head = node

    def removeNode(self, value):
        """A function that search the list for a node containing the value provided. Returns no value.
        Supply the value to search from the list."""
        temp = self.head
        prev = None

        while (temp.next != None):
            if (temp == temp.next):
                prev.next = temp.next

            prev = temp
            temp = temp.next
df = pd.read_csv("streetname.csv")
tmp_list = list(df["Street_Name"])

HDBdf = pd.read_csv("sg_zipcode_mapper.csv")
# MRTdf = pd.read_csv("ICT1008/projvers1/mrt_lrt_data.csv")
BUSdf = pd.read_csv("BusStop.csv")
hdbMap = HDBMap()
edges = HDBEdges()

def HDBrun(postal, dlat, dlong):
    tmp_HDB = None
    for index, row in HDBdf.iterrows():
        tmp_HDB = HDB(row["latitude"], row["longtitude"], row["blk_no"], row["road_name"], row["postal"])
        hdbMap.addHDB(tmp_HDB)

    for index, row in BUSdf.iterrows():
        tmp_Bus = BusStop(row["Latitude"], row["Longitude"], row["BusStopCode"])
        hdbMap.addBus(tmp_Bus)

    for index, row in HDBdf.iterrows():
        tmp_HDB = HDB(row["latitude"], row["longtitude"], row["blk_no"], row["road_name"], row["postal"])
        hdbMap.findAdjacency(tmp_HDB)
        edges.addEdge(tmp_HDB.postal_Code)
        #print(tmp_HDB.postal_Code)

    seq = edges.AstarRouting(postal, dlat, dlong)
    return seq

