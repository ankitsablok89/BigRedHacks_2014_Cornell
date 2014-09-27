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
		artistInfoJsonResponse = urllib2.urlopen('http://api.bandsintown.com/artists/' + artistName + '.json?app_id=' + bandsInTownAppID)		
		# convert the json object obtained above into a Python dictionary object
		artistInfoJsonDictionary = json.load(artistInfoJsonResponse)

		# set the different attributes of the ArtistInfo object
		self.artistName = artistName
		self.artistURLOnBandsInTown = artistInfoJsonDictionary['url']
		self.artistMBID = artistInfoJsonDictionary['mbid']
		self.artistUpcomingEventsCount = artistInfoJsonDictionary['upcoming_events_count']		