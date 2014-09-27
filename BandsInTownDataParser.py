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


if __name__ == '__main__':
	print getArtistsJsonString('Skrillex')