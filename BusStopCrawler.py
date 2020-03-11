import json
import urllib
from urllib.parse import urlparse
import csv

import httplib2 as http #External library

with open("BusStop.csv","w",newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["BusStopCode", "Description", "Latitude", "Longitude", "RoadName"])

maxValueReturn = 500
number_of_returned_data = 500
count = 0
number_of_bus_stop = count * 500
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
  print(number_of_returned_data)
  print(json.dumps(jsonObj, sort_keys=True, indent=4))
  
  for data in jsonObj["value"]:
    with open("BusStop.csv","a",newline='') as file:
      writer = csv.writer(file)
      datalist = [str(data["BusStopCode"]), str(data["Description"]), str(data["Latitude"]), str(data["Longitude"]), str(data["RoadName"])]
      writer.writerow(datalist)
