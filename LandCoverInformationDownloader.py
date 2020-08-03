from bs4 import BeautifulSoup
import json
import requests
import csv

# input date range. Follow this format: 'YYYY-MM-DD'
# start date:
startDate = '2020-04-27'
EndDate = '2020-07-23'
# 1. make sure column in csv is labeled "userid"
# 2. make sure to place the csv file into the same file
# 3. what is the name of the csv file? *keep quotes
csvname = 'CSVREADERTEST.csv'

#open the csv file containing the user IDs
with open(csvname, 'r') as userID_file:
  userID_reader = csv.DictReader(userID_file)

  # create another csv file to write data into
  with open('GlobeInformation.csv', 'w', newline = '') as InfoCSVFile:
    NewCSVWriter = csv.writer(InfoCSVFile, delimiter = ',')
    #Write the headers into the new csv file
    NewCSVWriter.writerow(['userid', 'longitude', 'latitude', 'siteID', 'Measured Date', 'protocol', 'MUC', 'UpURL', 'DownURL', 'EastURL', 'WestURL', 'NorthURL', 'SouthURL'])

    #loop through user IDs in inputted csv file
    for line in userID_reader:
      userid = line['userid']

      #use Globe API to get data
      GlobeAPI_URL = requests.get('https://api.globe.gov/search/v1/measurement/protocol/measureddate/userid/?protocols=land_covers&startdate=' + startDate + '&enddate='+ EndDate + '&userid=' + str(userid) +'&geojson=FALSE&sample=FALSE').text
      #set up BeautifulSoup4
      BSoup4 = BeautifulSoup(GlobeAPI_URL, 'lxml')

      #Isolate the Json data and put it into a string called "paragraph"
      body = BSoup4.find('body')
      paragraph = body.p.text

      #load the string into a python object
      data = json.loads(paragraph)

      #pick out the needed information and store them
      for landcover in data['results']:
        siteId = landcover['siteId']
        measuredDate = landcover['measuredDate']
        latitude = landcover['latitude']
        longitude = landcover['longitude']
        protocol = landcover['protocol']
        MUC = landcover['data']['landcoversMucCode']
        UpURL = landcover['data']['landcoversUpwardPhotoUrl']
        DownURL = landcover['data']['landcoversDownwardPhotoUrl']
        EastURL = landcover['data']['landcoversEastPhotoUrl']
        WestURL = landcover['data']['landcoversWestPhotoUrl']
        NorthURL = landcover ['data']['landcoversNorthPhotoUrl']
        SouthURL = landcover['data']['landcoversSouthPhotoUrl']
        NewCSVWriter.writerow([userid, longitude, latitude, siteId, measuredDate, protocol, MUC, UpURL, DownURL, EastURL, WestURL, NorthURL, SouthURL])





