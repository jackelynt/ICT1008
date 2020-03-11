import httplib2 as http
import requests
import csv
import json
import urllib
from onemapsg import OneMapClient

with open("HDBBlocks.csv","w",newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["blk_no", "street"])
url = 'https://data.gov.sg/api/action/datastore_search?resource_id=482bfa14-2977-4035-9c61-c85f871daf4e'

number_of_returned_data = 100
maxValueReturn = 100
count = 0
number_of_blocks = count * 100
while (number_of_returned_data >= 100):
    number_of_blocks = count * 100
    print(number_of_blocks)
    tmp_offset_str = ''
    if(count != 0):
        tmp_offset_str = 'offset=' + str(number_of_blocks) + '&'
    url = 'https://data.gov.sg/api/action/datastore_search?' + tmp_offset_str + 'resource_id=482bfa14-2977-4035-9c61-c85f871daf4e'
    reponse = requests.get(url)
    jsonObj = json.loads(reponse.content)
    count += 1

    number_of_returned_data = len(jsonObj["result"]["records"])
    print(number_of_returned_data)

    
    
    for data in jsonObj["result"]["records"]:
        with open("HDBBlocks.csv","a",newline='') as file:
            writer = csv.writer(file)
            searchPara = data["blk_no"] + " " + data["street"]
            onemapurl = "https://developers.onemap.sg/commonapi/search?searchVal=" + searchPara + "&returnGeom=Y&getAddrDetails=Y&pageNum=1"
            onemapreponse = requests.get(onemapurl)
            onemapjson = json.loads(onemapreponse.content)
            #print(onemapjson["results"][0])
            #onemapdata = json.loads(onemapjson["results"][0])
            #print(onemapjson)
            if onemapjson["found"] != 0:
                datalist = [data["blk_no"], data["street"], onemapjson["results"][0]["BLK_NO"], onemapjson["results"][0]["ROAD_NAME"], onemapjson["results"][0]["ADDRESS"], onemapjson["results"][0]["LATITUDE"], onemapjson["results"][0]["LONGTITUDE"]]
                print(datalist)
                writer.writerow(datalist)
            else:
                datalist = [data["blk_no"], data["street"]]
                print(datalist)
                writer.writerow(datalist)
