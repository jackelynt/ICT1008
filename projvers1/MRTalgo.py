# use greedy algo for MRT/LRT
import csv
def mrtalgofunc():
    with open('mrt_lrt_data.csv') as holdcsv:
        mrtcsv_data=next(csv.reader(holdcsv),None) #skip first row
        data = [(int(line[2]),int(line[3])) for line in csv.reader(holdcsv) if line]
        print(data)