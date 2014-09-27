# import the following libraries to perform parsin of the BandsInTown API data
import json
import urllib2

# this class is used to store the location information of different events where the artists will be performing in the future
class EventLocationInfo:

	# this is the constructor method for the EventLocationInfo object
	def __init__(self, eventURL, eventCity, eventVenueName, eventRegion, eventCountry, eventCityLatitude, eventCityLongitude):
		self.eventURL = eventURL
		self.eventCity = eventCity
		self.eventVenueName = eventVenueName
		self.eventRegion = eventRegion
		self.eventCountry = eventCountry
		self.eventCityLatitude = eventCityLatitude
		self.eventCityLongitude = eventCityLongitude

# this class is used to form an object of type 'Artist' which stores all the information relative to an Artist
class ArtistInfo:

	# this is the appID we use to access the 'BandsInTown' API
	bandsInTownAppID = 'BigRedHacks_2014'

	# this is the constructor method for the ArtistInfo class which is used to initialize various attributes of the ArtistInfo object
	def __init__(self, artistName):

		# hit the BandsInTown API to get the list of attributes for the artistName passed using the get request - http://www.bandsintown.com/api/1.0/requests#artists-get 
		artistInfoJsonResponse = urllib2.urlopen('http://api.bandsintown.com/artists/' + artistName + '.json?app_id=BigRedHacks_2014')		
		# convert the json object obtained above into a Python dictionary object
		artistInfoJsonDictionary = json.load(artistInfoJsonResponse)

		# set the different attributes of the ArtistInfo object
		self.artistName = artistName
		self.artistURLOnBandsInTown = artistInfoJsonDictionary['url']
		self.artistMBID = artistInfoJsonDictionary['mbid']
		self.artistUpcomingEventsCount = artistInfoJsonDictionary['upcoming_events_count']

		# now we try to get a list of all the venues where the artist is performing by hitting the BandsInTownAPI again - http://www.bandsintown.com/api/1.0/responses#events-json
		artistEventsInfoJsonResponse = urllib2.urlopen('http://api.bandsintown.com/artists/' + self.artistName + '/events.json?app_id=BigRedHacks_2014')
		# convert the json response obtained above into a python list which consists of event objects which in turn are dictionaries
		artistEventsInfoJsonResponseList = json.load(artistEventsInfoJsonResponse)
		# this is the list of EventLocationInfo objects corresponding to the artist
		eventArtistList = []
		for event in artistEventsInfoJsonResponseList:
			venueDictionary = event['venue']
			eventInfoObject = EventLocationInfo(event['url'],venueDictionary['city'],venueDictionary['name'],venueDictionary['region'], venueDictionary['country'], venueDictionary['latitude'], venueDictionary['longitude'])
			eventArtistList.append(eventInfoObject)	
		
		# initialize the a list object for the artist
		self.artistEventList = eventArtistList

if __name__ == '__main__':
	artistName = raw_input('Enter the artist name : ')
	artist = ArtistInfo(artistName)
	for event in artist.artistEventList:
		print event.eventVenueName
