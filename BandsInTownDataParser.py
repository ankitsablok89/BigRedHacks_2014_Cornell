import json
import urllib2

# this variable stores the appID we are going to use while hitting the BandsInTown API to extract useful data
bandsInTownAppID = 'BigRedHacks_2014'

# this function is used to return the 'json' response relative to a specific artist which is basically a dictionary consisting of different attributes of the artist
def getArtistsJsonString(artistName):
	# refer this for more details - http://www.bandsintown.com/api/1.0/requests#artists-get
	artistJsonStringResponse = urllib2.urlopen('http://api.bandsintown.com/artists/' + artistName + '.json?app_id=' + bandsInTownAppID)
	
	# convert the json response obtained above into a Python dictionary
	artistJsonStringResponseDictionary = json.load(artistJsonStringResponse)

	return artistJsonStringResponseDictionary


# this function is used to return a list of 'dictionaries' where each dictionary constitutes an event and its attributes
def getArtistsEventsJsonDictionaryList(artistName):
	# refer this for more details - http://www.bandsintown.com/api/1.0/requests#artists-get
	artistEventsJsonStringResponse = urllib2.urlopen('http://api.bandsintown.com/artists/' + artistName + '/events.json?app_id=' + bandsInTownAppID)
	
	# convert the json response obtained into a Python dictionary
	artistEventsJsonStringResponseDictionary = json.load(artistEventsJsonStringResponse)

	return artistEventsJsonStringResponseDictionary

if __name__ == '__main__':
	artistName = raw_input("Enter the artists you are searching for : ")
	artistsEventList = getArtistsEventsJsonDictionaryList(artistName)

	for event in artistsEventList:
		print event
		print