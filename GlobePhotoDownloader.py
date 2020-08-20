#First install four packages:
# 1. Pillow
# 2. BeautifulSoup4
# 3. requests
# 4. lxml

from bs4 import BeautifulSoup
import json
import requests
import io
import PIL.Image as Image
import csv

# input date range. Follow this format: 'YYYY-MM-DD'
# start date:
startDate = '2020-04-27'
EndDate = '2020-07-23'
# 1. make sure column in csv is labeled "userid"
# 2. make sure to place the csv file into the same file
# 3. what is the name of the csv file? *keep quotes
# Warning: Some computers hide the '.csv' ending of the file name. Adding an extra .csv will cause the program to fail.
csvname = 'useridlist.csv'
#Input your desired Image Resolution. ImageResolution = (Width in Pixels),(height in Pixels)
ImageResolution = 1920, 1080
#Would you like to start with UserID or SiteName? Set the variable to 0 for UserID and 1 for SiteName
NameStart = 0

#open the csv file containing the User IDs
with open(csvname, 'r') as userID_file:
  userID_reader = csv.DictReader(userID_file)

  # create another csv file to write the Globe Photo names into. Used for cross-checking downloaded photos to make sure they are all there.
  with open('GlobeDownloadedPhotoNames.csv', 'w', newline='') as PhotoNameCSV:
    NewCSVWriter = csv.writer(PhotoNameCSV, delimiter=',')
    # Write the headers into the new csv file
    NewCSVWriter.writerow(['Globe Photo Names'])

    # loop through user IDs in inputted csv file
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
        siteName = landcover['siteName']
        measuredDate = landcover['measuredDate']
        latitude = landcover['data']['landcoversMeasurementLatitude']
        longitude = landcover['data']['landcoversMeasurementLongitude']
        protocol = landcover['protocol']
        MUC = landcover['data']['landcoversMucCode']
        UpURL = landcover['data']['landcoversUpwardPhotoUrl']
        DownURL = landcover['data']['landcoversDownwardPhotoUrl']
        EastURL = landcover['data']['landcoversEastPhotoUrl']
        WestURL = landcover['data']['landcoversWestPhotoUrl']
        NorthURL = landcover ['data']['landcoversNorthPhotoUrl']
        SouthURL = landcover['data']['landcoversSouthPhotoUrl']

      #download and name the images:
        #download the East image

        #obtain image content
        GetBytesfromURL = requests.get(EastURL)
        image_bytes = GetBytesfromURL.content

        # convert the bytes to image
        image = Image.open(io.BytesIO(image_bytes))

        #get the original size of the image
        width, height = image.size

        #resize the image using the user designated resolution
        ResizedImage = image.resize(ImageResolution, Image.ANTIALIAS)

        #Change the order of UserID or SiteName depending on user preference
        if NameStart == 0:
          FirstinName = userid
          SecondinName = siteName
        else:
          FirstinName = siteName
          SecondinName = userid
        # name and save it. Naming convention: GlobeObserver_(UserID or SiteName)_(SiteName or UserID)_Protocol_latitude_longitude_MeasuredDate_MUC_Direction_OriginalWidthofPicture_OriginalHeightofPicture_(ResizedWidth, ResizedHeight).jpg
        ResizedImage.save('GLOBEObserver_' + str(FirstinName) + '_' + str(SecondinName) + '_' + protocol + '_' + str(latitude) + '_' + str(
          longitude) + '_' + str(measuredDate) + '_' + str(MUC) + '_' + 'East' + '_' + str(width) + 'x' + str(
          height) + '_' + str(ImageResolution) + '.jpg')

        #write the name into the 'GlobeDownloadedPhotoNames' csv file
        NewCSVWriter.writerow(['GLOBEObserver_' + str(FirstinName) + '_' + str(SecondinName) + '_' + protocol + '_' + str(latitude) + '_' + str(
          longitude) + '_' + str(measuredDate) + '_' + str(MUC) + '_' + 'East' + '_' + str(width) + 'x' + str(
          height) + '.jpg'])

        #Repeat for remaining directions
        #West
        GetBytesfromURL = requests.get(WestURL)
        image_bytes = GetBytesfromURL.content
        image = Image.open(io.BytesIO(image_bytes))
        width, height = image.size
        ResizedImage = image.resize(ImageResolution, Image.ANTIALIAS)
        ResizedImage.save('GLOBEObserver_' + str(FirstinName) + '_' + str(SecondinName) + '_' + protocol + '_' + str(latitude) + '_' + str(
          longitude) + '_' + str(measuredDate) + '_' + str(MUC) + '_' + 'West' + '_' + str(width) + 'x' + str(
          height) + '_' + str(ImageResolution) + '.jpg')

        # write the name into the 'GlobeDownloadedPhotoNames' csv file
        NewCSVWriter.writerow(
          ['GLOBEObserver_' + str(FirstinName) + '_' + str(SecondinName) + '_' + protocol + '_' + str(latitude) + '_' + str(
            longitude) + '_' + str(measuredDate) + '_' + str(MUC) + '_' + 'West' + '_' + str(width) + 'x' + str(
            height) + '.jpg'])

        #North
        GetBytesfromURL = requests.get(NorthURL)
        image_bytes = GetBytesfromURL.content
        image = Image.open(io.BytesIO(image_bytes))
        width, height = image.size
        ResizedImage = image.resize(ImageResolution, Image.ANTIALIAS)
        ResizedImage.save('GLOBEObserver_' + str(FirstinName) + '_' + str(SecondinName) + '_' + protocol + '_' + str(latitude) + '_' + str(
          longitude) + '_' + str(measuredDate) + '_' + str(MUC) + '_' + 'North' + '_' + str(width) + 'x' + str(
          height) + '_' + str(ImageResolution) + '.jpg')

        # write the name into the 'GlobeDownloadedPhotoNames' csv file
        NewCSVWriter.writerow(
          ['GLOBEObserver_' + str(FirstinName) + '_' + str(SecondinName) + '_' + protocol + '_' + str(latitude) + '_' + str(
            longitude) + '_' + str(measuredDate) + '_' + str(MUC) + '_' + 'North' + '_' + str(width) + 'x' + str(
            height) + '.jpg'])

        #South
        GetBytesfromURL = requests.get(SouthURL)
        image_bytes = GetBytesfromURL.content
        image = Image.open(io.BytesIO(image_bytes))
        width, height = image.size
        ResizedImage = image.resize(ImageResolution, Image.ANTIALIAS)
        ResizedImage.save('GLOBEObserver_' + str(FirstinName) + '_' + str(SecondinName) + '_' + protocol + '_' + str(latitude) + '_' + str(
          longitude) + '_' + str(measuredDate) + '_' + str(MUC) + '_' + 'South' + '_' + str(width) + 'x' + str(
          height) + '_' + str(ImageResolution) + '.jpg')

        # write the name into the 'GlobeDownloadedPhotoNames' csv file
        NewCSVWriter.writerow(
          ['GLOBEObserver_' + str(FirstinName) + '_' + str(SecondinName) + '_' + protocol + '_' + str(latitude) + '_' + str(
            longitude) + '_' + str(measuredDate) + '_' + str(MUC) + '_' + 'South' + '_' + str(width) + 'x' + str(
            height) + '.jpg'])

        #Up
        GetBytesfromURL = requests.get(UpURL)
        image_bytes = GetBytesfromURL.content
        image = Image.open(io.BytesIO(image_bytes))
        width, height = image.size
        ResizedImage = image.resize(ImageResolution, Image.ANTIALIAS)
        ResizedImage.save('GLOBEObserver_' + str(FirstinName) + '_' + str(SecondinName) + '_' + protocol + '_' + str(latitude) + '_' + str(
          longitude) + '_' + str(measuredDate) + '_' + str(MUC) + '_' + 'Upwards' + '_' + str(width) + 'x' + str(
          height) + '_' + str(ImageResolution) + '.jpg')

        # write the name into the 'GlobeDownloadedPhotoNames' csv file
        NewCSVWriter.writerow(
          ['GLOBEObserver_' + str(FirstinName) + '_' + str(SecondinName) + '_' + protocol + '_' + str(latitude) + '_' + str(
            longitude) + '_' + str(measuredDate) + '_' + str(MUC) + '_' + 'Upwards' + '_' + str(width) + 'x' + str(
            height) + '.jpg'])

        #Down
        GetBytesfromURL = requests.get(DownURL)
        image_bytes = GetBytesfromURL.content
        image = Image.open(io.BytesIO(image_bytes))
        width, height = image.size
        ResizedImage = image.resize(ImageResolution, Image.ANTIALIAS)
        ResizedImage.save('GLOBEObserver_' + str(FirstinName) + '_' + str(SecondinName) + '_' + protocol + '_' + str(latitude) + '_' + str(
          longitude) + '_' + str(measuredDate) + '_' + str(MUC) + '_' + 'Downwards' + '_' + str(width) + 'x' + str(
          height) + '_' + str(ImageResolution) + '.jpg')

        # write the name into the 'GlobeDownloadedPhotoNames' csv file
        NewCSVWriter.writerow(
          ['GLOBEObserver_' + str(FirstinName) + '_' + str(SecondinName) + '_' + protocol + '_' + str(latitude) + '_' + str(
            longitude) + '_' + str(measuredDate) + '_' + str(MUC) + '_' + 'Downwards' + '_' + str(width) + 'x' + str(
            height) + '.jpg'])
