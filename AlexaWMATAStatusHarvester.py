import requests

api_key_file = open('api_key', 'r')
api_key = api_key_file.readlines()[0].rstrip()
station_list_url = 'https://api.wmata.com/Rail.svc/json/jStations'
station_list_get_parameters = { 'api_key': api_key }
station_list_json = requests.get(station_list_url, station_list_get_parameters).json()

def listRailCodes():
    railCodes = []
    for stations in station_list_json['Stations']:
        for railOption in range(1,5):
            lineCodeValue = stations['LineCode' + str(railOption)]
            if (lineCodeValue != None and lineCodeValue not in railCodes):
                railCodes.append(lineCodeValue)
    for code in railCodes:
        print (code)

def listStations():
    stationList = []
    for stations in station_list_json['Stations']:
        stationList.append(stations['Name'])
    for station in stationList:
        print (station)

print ('--- List of Lines ---')
listRailCodes()

print ('--- List of Stations ---')
listStations()
