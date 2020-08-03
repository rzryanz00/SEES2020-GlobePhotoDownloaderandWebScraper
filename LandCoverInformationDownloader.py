from bs4 import BeautifulSoup
import json
import requests
import csv
import io
import PIL.Image as Image

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
    NewCSVWriter.writerow(['userid', 'longitude', 'latitude', 'siteID', 'Measured Date', 'protocol', 'MUC', 'UpURL', 'DownURL', 'EastURL', 'WestURL', 'NorthURL', 'SouthURL', 'Up Image Size', 'Down Image Size', 'East Image Size', 'West Image Size', 'North Image Size', 'South Image Size'])

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

        #get image sizes

        #Up
        GetBytesfromURL = requests.get(UpURL)
        image_bytes = GetBytesfromURL.content
        image = Image.open(io.BytesIO(image_bytes))
        Uwidth, Uheight = image.size

        #Down
        GetBytesfromURL = requests.get(NorthURL)
        image_bytes = GetBytesfromURL.content
        image = Image.open(io.BytesIO(image_bytes))
        Dwidth, Dheight = image.size

        #North
        GetBytesfromURL = requests.get(NorthURL)
        image_bytes = GetBytesfromURL.content
        image = Image.open(io.BytesIO(image_bytes))
        Nwidth, Nheight = image.size

        #South
        GetBytesfromURL = requests.get(NorthURL)
        image_bytes = GetBytesfromURL.content
        image = Image.open(io.BytesIO(image_bytes))
        Swidth, Sheight = image.size

        #East
        GetBytesfromURL = requests.get(EastURL)
        image_bytes = GetBytesfromURL.content
        image = Image.open(io.BytesIO(image_bytes))
        Ewidth, Eheight = image.size

        #West
        GetBytesfromURL = requests.get(WestURL)
        image_bytes = GetBytesfromURL.content
        image = Image.open(io.BytesIO(image_bytes))
        Wwidth, Wheight = image.size

        #write the information to the csv file
        NewCSVWriter.writerow([userid, longitude, latitude, siteId, measuredDate, protocol, MUC, UpURL, DownURL, EastURL, WestURL, NorthURL, SouthURL, str(Uwidth) +'x'+str(Uheight), str(Dwidth) +'x'+str(Dheight), str(Ewidth) +'x'+str(Eheight), str(Wwidth) +'x'+str(Wheight), str(Nwidth) +'x'+str(Nheight), str(Swidth) +'x'+str(Sheight)])





