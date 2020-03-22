import copy

from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap
import csv
import math
app = Flask(__name__)
Bootstrap(app)
from collections import deque
from collections import defaultdict
#
# class Queue:
#   arr = []
#   def enqueue(self,n):
#     self.arr.append(n)
#
#   def dequeue(self):
#     if len(self.arr)!=0:
#       n = self.arr[0]
#       del self.arr[0]
#       return n
#     else:
#       return None
#
#   #get the front node
#   def front(self):
#     if len(self.arr)!=0:
#       return self.arr[0]
#     else: #if arr empty
#       return None


class Station:
    def __init__(self, station, adj = []):
        self.name = station #name
        self.adj = adj

    def __repr__(self):
        return self.name

    def add_adj(self, adj):
        if adj not in self.adj:
            self.adj.append(adj)


##dummy data
dest_x = 1.39392
dest_y = 103.912632
start_station = 'Punggol'
# nearest_mrt_todst = start_station

mrt_lrt_needed = ['Punggol', 'Cove', 'Meridian', 'Coral Edge', 'Riviera', 'Kadaloor', 'Oasis', 'Damai', 'Punggol', 'Sam Kee',
                  'Teck Lee', 'Punggol Point', 'Samudera', 'Nibong', 'Sumang', 'Soo Teck', 'Punggol']
mrt_lrt_needed_capital = mrt_lrt_needed.copy()
for i in range(len(mrt_lrt_needed_capital)):  # convert all to uppercase
    mrt_lrt_needed_capital[i] = mrt_lrt_needed_capital[i].upper()

# print(mrt_lrt_needed)
# print(mrt_lrt_needed_capital)
with open('mrt_lrt_data.csv', 'r') as holdcsv:
    mrtcsv_data = next(csv.reader(holdcsv), None)  # skip first row
    data_coordinates = [(float(line[2]), float(line[3])) for line in csv.reader(holdcsv) if
                        line[0].upper() in mrt_lrt_needed_capital]  # store coordinates (x,y) of mrt_lrt_needed in data list
    # print("data coordinates: ", data_coordinates)

# check if mrt/lrt is needed
def MRT_needed(mrt_entered, dest_x, dest_y):
    # get nearest mrt from destination
    base = 9999  # random high number
    for i in range(len(mrt_entered)):
        distance_squared = (data_coordinates[i][0] - dest_x) ** 2 + (
                    data_coordinates[i][1] - dest_y) ** 2  # calculate distance
        if distance_squared < base:
            base = distance_squared
            nearest_mrt_todst = mrt_lrt_needed[i]

    mrt_entered = mrt_entered.upper()

    print("Nearest mrt to dest:", nearest_mrt_todst)

    if nearest_mrt_todst.upper() == mrt_entered:
        return 0 # MRT not necessary.
    else:
        return nearest_mrt_todst # mrt needed

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
print(f"Neighbours of {start_station} are: {getNeighbour(mrt_lrt_needed,start_station)}")

#creating graph dictionary for neighbours of stns
def createGraph():
    graph = {}
    for i in mrt_lrt_needed:
        graph[i] = getNeighbour(mrt_lrt_needed,i)
        # graph[i]=0
    # print(graph)
    return graph

graph = createGraph()

print("Graph:",graph)
dest_station = MRT_needed(start_station, dest_x, dest_y)

@app.route('/')
def MRT_route():
    mrt_lrt_needed = ['Punggol', 'Cove', 'Meridian', 'Coral Edge', 'Riviera', 'Kadaloor', 'Oasis', 'Damai', 'Punggol',
                      'Sam Kee',
                      'Teck Lee', 'Punggol Point', 'Samudera', 'Nibong', 'Sumang', 'Soo Teck', 'Punggol']

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

    def createGraph():
        graph = {}
        for i in mrt_lrt_needed:
            graph[i] = getNeighbour(mrt_lrt_needed,i)
        return graph

    # initialising stations ( this is without the repeats of punggol )
    stations = {}
    station_names = ['Punggol', 'Cove', 'Meridian', 'Coral Edge', 'Riviera', 'Kadaloor', 'Oasis', 'Damai',
                     'Sam Kee', 'Teck Lee', 'Punggol Point', 'Samudera', 'Nibong', 'Sumang', 'Soo Teck']
    station_graph = createGraph()
    for station_name in station_names:
        stations[station_name] = Station(station_name, station_graph[station_name])

    if start_station not in station_names or dest_station not in station_names:
        print(f"Invalid start or destination station!")
        return render_template('login.html')

    _start_station = stations[start_station]
    _dest_station = stations[dest_station]

    for k, v in stations.items():
        v_namelist = v.adj
        temp = []
        for item in v_namelist:
            temp.append(stations[item])
        v.adj = temp

    all_slns = []

    def rec_stn(station, start=False, cur_list=[]):

        temp = copy.deepcopy(cur_list)
        temp.append(station)

        if station == _dest_station:
            all_slns.append(temp)
            return

        if station == _start_station and not start:
            return

        for adj_station in station.adj:
            if not adj_station.name in [cur.name for cur in temp]:
                rec_stn(adj_station, cur_list=temp)

    print(f"Start: {_start_station.name}, Dest: {_dest_station.name}")
    rec_stn(_start_station, start=True)

    if not all_slns:
        print(f"No available path from {_start_station.name} to {_dest_station.name}")
    else:
        print("Available Paths:")
        cur_shortest_path = all_slns[0]
        for item in all_slns:
            print(item)
            if len(item) < len(cur_shortest_path):
                cur_shortest_path = item

        print("Shortest Path (No. of stops):")
        path_str = f"{len(cur_shortest_path)-1} Stops: {_start_station}"
        for item in cur_shortest_path[1:]:
            path_str += f" --> {item.name}"
        print(path_str)


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


if __name__ == '__main__':
    app.run(debug=True)
