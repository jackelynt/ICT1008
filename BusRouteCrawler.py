import json
import urllib
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
  print(number_of_returned_data)
  print(json.dumps(jsonObj, sort_keys=True, indent=4))
  
  for data in jsonObj["value"]:
    with open("BusRoute.csv","a",newline='') as file:
      writer = csv.writer(file)
      datalist = [data["ServiceNo"], data["Direction"], data["StopSequence"], data["Distance"], data["BusStopCode"] ]
      writer.writerow(datalist)
