import json
import urllib
import pandas
from urllib.parse import urlparse
import csv

import httplib2 as http #External library

with open("BusRoute.csv","w",newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["ServiceNo", "Direction", "StopSequence", "Distance", "BusStopCode"])

maxValueReturn = 500
number_of_returned_data = 500
count = 0
number_of_bus_route_index = count * 500
buscodedf = pandas.read_csv("BusStop.csv")
punggolBusStop = buscodedf["BusStopCode"].tolist()
print(punggolBusStop)
while (number_of_returned_data >= 500):
  number_of_bus_route_index = count * 500
  print(number_of_bus_route_index)
  headers = {'AccountKey' : 'GwbEwk8bR3upUkmGRByXNA==', 'accept' : 'application/json'}
  uri = 'http://datamall2.mytransport.sg/'
  path = '/ltaodataservice/BusRoutes?$skip=' + str(number_of_bus_route_index)
  count += 1

  target = urlparse(uri+path)
  print(target.geturl())
  method = 'GET'
  body = ''

  h = http.Http()

  response, content = h.request(target.geturl(), method, body, headers)

  jsonObj = json.loads(content)
  number_of_returned_data = len(jsonObj["value"])
  #print(number_of_returned_data)
  #print(json.dumps(jsonObj, sort_keys=True, indent=4))
  punggolServiceList = []
  for data in jsonObj["value"]:
    if str(data["BusStopCode"]).isdigit():
      busStopCode = int(data["BusStopCode"])
      if int(data["BusStopCode"]) in punggolBusStop:
        punggolServiceList.append(data["ServiceNo"])
  with open("BusRoute.csv","a",newline='') as file:
    writer = csv.writer(file)
    
    for data in jsonObj["value"]:
      if data["ServiceNo"] in punggolServiceList:
        datalist = [data["ServiceNo"], data["Direction"], data["StopSequence"], data["Distance"], data["BusStopCode"]]
        print(datalist)
        writer.writerow(datalist)

maxValueReturn = 500
number_of_returned_data = 500
count = 0
number_of_bus_stop = count * 500
busroutedf = pandas.read_csv("BusRoute.csv")
punggolBusRouteStop = busroutedf["BusStopCode"].tolist()
while (number_of_returned_data >= 500):
  number_of_bus_stop = count * 500
  print(number_of_bus_stop)
  headers = {'AccountKey' : 'GwbEwk8bR3upUkmGRByXNA==', 'accept' : 'application/json'}
  uri = 'http://datamall2.mytransport.sg/'
  path = '/ltaodataservice/BusStops?$skip=' + str(number_of_bus_stop)
  count += 1

  target = urlparse(uri+path)
  print(target.geturl())
  method = 'GET'
  body = ''

  h = http.Http()

  response, content = h.request(target.geturl(), method, body, headers)

  jsonObj = json.loads(content)
  number_of_returned_data = len(jsonObj["value"])
  #print(number_of_returned_data)
  #print(json.dumps(jsonObj, sort_keys=True, indent=4))
  for data in jsonObj["value"]:
    with open("BusStop.csv","a",newline='') as file:
      writer = csv.writer(file)
      if int(data["BusStopCode"]) in punggolBusRouteStop:
        datalist = [data["BusStopCode"], data["Description"], data["Latitude"], data["Longitude"], data["RoadName"]]
        print(datalist)
        writer.writerow(datalist)