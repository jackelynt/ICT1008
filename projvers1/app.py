import copy
import json
from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap
import csv
import math
app = Flask(__name__)
Bootstrap(app)
from collections import deque
from collections import defaultdict
from BusStop import BusStop
from BusStopTable import BusStopTable
from BusService import BusService
from BusServiceTable import BusServiceTable
from BusStopRoute import BusStopRoute
import pandas
from BusRouteAlgo import BusRouteAlg
import HDB
import folium
import backend


class Station:
    def __init__(self, station, adj, latitude, longitude, MRT_type):
        self.name = station #name
        self.adj = adj
        self.latitude = latitude
        self.longitude = longitude
        self.type = MRT_type

    def __repr__(self):
        return self.name

    def add_adj(self, adj):
        if adj not in self.adj:
            self.adj.append(adj)


# check if mrt/lrt is needed
def MRT_needed(graph ,mrt_entered, dest_x, dest_y):
    # get nearest mrt from destination
    base = 9999  # random high number
    for i in graph.keys():
        distance_squared = (float(graph[i].latitude) - dest_x) ** 2 + (
                    float(graph[i].longitude) - dest_y) ** 2  # calculate distance
        if distance_squared < base:
            base = distance_squared
            nearest_mrt_todst = graph[i].name

    mrt_entered = mrt_entered.upper()

    print("Nearest mrt to dest:", nearest_mrt_todst)

    if nearest_mrt_todst.upper() == mrt_entered:
        return 0 # MRT not necessary.
    else:
        return nearest_mrt_todst # mrt needed
#creating graph dictionary for neighbours of stns
def createGraph(punggolMRTdf, mrt_lrt_needed):
    graph = {}
    for index, row in punggolMRTdf.iterrows():
        if str(row["station_name"]) in mrt_lrt_needed:
            graph[str(row["station_name"])] = Station(str(row["station_name"]), getNeighbour(mrt_lrt_needed, str(row["station_name"])), row["lat"], row["lng"], row["type"])
        # graph[i]=0
    # print(graph)
    return graph
def getNeighbour(array,stn):
        neighbours=[]
        stnindex = []
        for i in range(len(array)):
            if stn == array[i]:
                stnindex.append(i)
        for j in range(len(stnindex)):
            if stnindex[j] != 0:
                neighbours.append(array[stnindex[j]-1])
            if stnindex[j] != len(array)-1:
                neighbours.append(array[stnindex[j]+1])
        return neighbours

all_slns = []
def rec_stn(station,_dest_station, _start_station, graph, start=False, cur_list=[]):
    temp = copy.deepcopy(cur_list)
    temp.append(station)
    print(temp)
    if station == _dest_station:
        all_slns.append(temp)
        return

    if station == _start_station and not start:
        return

    for adj_station in graph[station].adj:
        if not adj_station in [cur for cur in temp]:  ##if adjacent name in temp
            rec_stn(adj_station,_dest_station, _start_station, graph, start=True, cur_list=temp)
            print(cur_list)

    # all_slns = []

def MRT_LRT_Algo(start_station, dest_x, dest_y):
    mrt_lrt_needed = [line.rstrip('\n') for line in open('MRT_LRT_Stations.txt')]
    mrt_lrt_needed_capital = mrt_lrt_needed.copy()
    for i in range(len(mrt_lrt_needed_capital)):  # convert all to uppercase
        mrt_lrt_needed_capital[i] = mrt_lrt_needed_capital[i].upper()
    punggolMRTdf = pandas.read_csv('mrt_lrt_data.csv')
    graph = {}
    print(f"Neighbours of {start_station} are: {getNeighbour(mrt_lrt_needed,start_station)}")
    graph = createGraph(punggolMRTdf,mrt_lrt_needed)
    for MRT in graph.keys():
        print("MRT : ", MRT)
        print("Adjacent List : ", graph[MRT].adj)

    dest_station = MRT_needed(graph, start_station, dest_x, dest_y)
    if(dest_station == 0 or dest_station == start_station):
        return [[graph[dest_station].name, graph[dest_station].latitude, graph[dest_station].longitude], ["HDB", "too close",dest_x, dest_y]]
    path_coords = []

    if start_station not in graph.keys() or dest_station not in graph.keys():
        print(f"Invalid start or destination station!")
        exit()

    coordinate_list = []
    coordinate_list = rec_stn(start_station, dest_station, start_station, graph,start=True)
    distance_list = []
    for list in all_slns:
        if len(distance_list) != 0:
            if len(list) < len(distance_list):
                distance_list = list
        else:
            distance_list = list
    tmp_list = []
    tmp_list_station = []
    for station_name in distance_list:
        tmp_list = []
        tmp_list.append(graph[station_name].type)
        tmp_list.append(graph[station_name].name)
        tmp_list.append(graph[station_name].longitude)
        tmp_list.append(graph[station_name].latitude)
        tmp_list_station.append(tmp_list)
    return tmp_list_station

def AlgoCompile(Postal, dest_x, dest_y, start_station):
    coordinate_list = MRT_LRT_Algo(start_station, dest_x, dest_y)#jack
    busstopTable = BusStopTable()#tofind closest bustop
    print(coordinate_list)
    closestbusstop = busstopTable.getClosestBusStop(float(coordinate_list[-1][3]), float(coordinate_list[-1][2]))
    print(Postal, dest_x, dest_y, start_station)
    HDB_List = HDB.HDBrun(Postal, dest_x, dest_y)
    HDB_List = list(reversed(HDB_List))
    destination_bus = HDB_List[0][1]
    busrouteList = BusRouteAlg(int(closestbusstop), int(destination_bus))
    coordinate_list.extend(list(reversed(busrouteList)))
    coordinate_list.extend(list(reversed(HDB_List[1:])))
    print(coordinate_list)
    #print(coordinate_list)
    #print(busrouteList)
    #print(coordinate_list)
    return coordinate_list







# MAP
@app.route("/")
def index():
    # For ddl
    ddval = []
    with open("HDBBlocks.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        counter = 0
        for row in csv_reader:
            if (counter == 0):
                counter += 1
            else:
                PCode = (row[6])
                toAppend = [row[0], PCode, row[4], row[5]]
                ddval.append(toAppend)
    return render_template('login.html', ddlist=ddval)


@app.route('/')
def MRT_route():
    mrt_lrt_needed = ['Punggol', 'Cove', 'Meridian', 'Coral Edge', 'Riviera', 'Kadaloor', 'Oasis', 'Damai', 'Punggol',
                      'Sam Kee',
                      'Teck Lee', 'Punggol Point', 'Samudera', 'Nibong', 'Sumang', 'Soo Teck', 'Punggol']
    return render_template('login.html')

@app.route('/success/<startloc> <endloc>')
def success(startloc, endloc):
    return (f'Start search for {startloc} to {endloc}')

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        start_loc = request.form['start']
        end_loc = request.form['end']
        return redirect(url_for('success', startloc = start_loc, endloc = end_loc))
    else:
        start_loc = request.args.get('start')
        end_loc = request.args.get('end')
        return redirect(url_for('success', startloc = start_loc, endloc = end_loc))
    

#loading starting map
@app.route('/reload')
def reload():
    return render_template("basemap.html")

#loading map with coordinates
@app.route('/reloadnext')
def reloadnext():
    ##if not first load
    if (request.args.get('startMrtLoc') != None):
        ##print(request.args.get('startMrtLoc'))
        ##temp test array
        #RouteArrayList = [[1.40454805557377, 103.897163888002], [1.40444046572287, 103.896924799455], [1.396805705, 103.9050542], [1.396941332, 103.9057295]]
        PosCode = request.args.get('postalCode')
        MrtStation = request.args.get('startMrtLoc')
        longtit = request.args.get('Longt')
        latit = request.args.get('Lat')
        PosCode = int(PosCode)
        longtit = float(longtit)
        latit = float(latit)
        RouteArrayList = AlgoCompile(PosCode, longtit, latit, MrtStation)
        #update map with coordinates
        #print(RouteArrayList)
        print(RouteArrayList)
        backend.UpdateMap(RouteArrayList)
    return render_template("map.html")

if __name__ == '__main__':
    app.run(debug=True)
