# import the following libraries to perform parsin of the BandsInTown API data
import re
import json
import urllib2
import datetime
import dateutil.parser

# this class is used to store the different attributes of a Hotel object, these are the hotels that are nearby the event
class HotelInfo:

	# this is the constructor method for the hotel objects
	def __init__(self, pricelineJsonResponseDict):
		self.pclnHotelID = pricelineJsonResponseDict['pclnHotelID']
		self.longitude = pricelineJsonResponseDict['lon']
		self.merchPrice = pricelineJsonResponseDict['merchPrice']
		self.overallRatingScore = pricelineJsonResponseDict['overallRatingScore']
		self.starRating = pricelineJsonResponseDict['starRating']
		self.hotelName = pricelineJsonResponseDict['hotelName']
		self.numGuestReviewsWithText = pricelineJsonResponseDict['numGuestReviewsWithText']
		self.pwysRate = pricelineJsonResponseDict['pwysRate']
		self.isRateRefundable = pricelineJsonResponseDict['isRateRefundable']
		self.freeCancelAvail = pricelineJsonResponseDict['freeCancelAvail']
		self.latitude = pricelineJsonResponseDict['lat']
		self.customHMIRank = pricelineJsonResponseDict['customHMIRank']
		self.proximity = pricelineJsonResponseDict['proximity']
		self.originalRank = pricelineJsonResponseDict['originalRank']
		self.remainingRooms = pricelineJsonResponseDict['remainingRooms']
		self.cleanlinessScore = pricelineJsonResponseDict['cleanlinessScore']
		self.diningScore = pricelineJsonResponseDict['diningScore']
		self.locationScore = pricelineJsonResponseDict['locationScore']
		self.staffScore = pricelineJsonResponseDict['staffScore']
		self.guestPopularity = pricelineJsonResponseDict['guestPopularity']
		self.tripAdvisorGuestRating = pricelineJsonResponseDict['tripAdvisorGuestRating']
		self.tripAdvisorNumOfReviews = pricelineJsonResponseDict['tripAdvisorNumOfReviews']

# this class is used to store the location information of different events where the artists will be performing in the future
class EventLocationInfo:

	# this is the constructor method for the EventLocationInfo object
	def __init__(self, eventURL, eventCity, eventVenueName, eventRegion, eventCountry, eventCityLatitude, eventCityLongitude, eventDateTime):

		self.eventURL = eventURL
		self.eventCity = eventCity
		self.eventVenueName = eventVenueName
		self.eventRegion = eventRegion
		self.eventCountry = eventCountry
		self.eventCityLatitude = eventCityLatitude
		self.eventCityLongitude = eventCityLongitude
		self.eventDateTime = dateutil.parser.parse(eventDateTime)

	# this function is used to print the different components of the EventLocationInfo object
	def printEventInfo(self):
		print "eventURL : ", self.eventURL, "\neventCity : ", self.eventCity, "\neventVenueName : ", self.eventVenueName, "\neventRegion : ", self.eventRegion, "\neventCountry : ", self.eventCountry, "\neventCityLatitude : ", self.eventCityLatitude, "\neventCityLongitude : ", self.eventCityLongitude, "\neventDateTime : ", self.eventDateTime
		print		

# this class is used to form an object of type 'Artist' which stores all the information relative to an Artist
class ArtistInfo:
	
	# this is the appID we use to access the 'BandsInTown' API
	bandsInTownAppID = 'BigRedHacks_2014'

	# this is the constructor method for the ArtistInfo class which is used to initialize various attributes of the ArtistInfo object
	def __init__(self, artistName):

		# hit the BandsInTown API to get the list of attributes for the artistName passed using the get request - http://www.bandsintown.com/api/1.0/requests#artists-get 
		artistInfoJsonResponse = urllib2.urlopen('http://api.bandsintown.com/artists/' + artistName + '.json?app_id=' + ArtistInfo.bandsInTownAppID)		
		# convert the json object obtained above into a Python dictionary object
		artistInfoJsonDictionary = json.load(artistInfoJsonResponse)

		# set the different attributes of the ArtistInfo object
		self.artistName = artistName
		self.artistURLOnBandsInTown = artistInfoJsonDictionary['url']
		self.artistMBID = artistInfoJsonDictionary['mbid']
		self.artistUpcomingEventsCount = artistInfoJsonDictionary['upcoming_events_count']

		# now we try to get a list of all the venues where the artist is performing by hitting the BandsInTownAPI again - http://www.bandsintown.com/api/1.0/responses#events-json
		artistEventsInfoJsonResponse = urllib2.urlopen('http://api.bandsintown.com/artists/' + self.artistName + '/events.json?app_id=' + ArtistInfo.bandsInTownAppID)
		# convert the json response obtained above into a python list which consists of event objects which in turn are dictionaries
		artistEventsInfoJsonResponseList = json.load(artistEventsInfoJsonResponse)
		# this is the list of EventLocationInfo objects corresponding to the artist
		eventArtistList = []
		for event in artistEventsInfoJsonResponseList:
			venueDictionary = event['venue']
			eventInfoObject = EventLocationInfo(event['url'],venueDictionary['city'],venueDictionary['name'],venueDictionary['region'], venueDictionary['country'], venueDictionary['latitude'], venueDictionary['longitude'], event['datetime'])
			eventArtistList.append(eventInfoObject)	
		
		# initialize the a list object for the artist
		self.artistEventList = eventArtistList

if __name__ == '__main__':
	
	# this is the name of the artist that the user entered
	artistName = raw_input("Enter Artist Name : ")
	artistInfo = ArtistInfo(artistName)
	
	print artistName + " is playing at the following venues -: \n"

	for event in artistInfo.artistEventList:
		print event.eventVenueName

	# now we prompt the user to enter the venue where he wants to see the band playing
	userVenue = raw_input("Enter the venue that interests you the most : ")

	# this is the event that the user is most interested in visiting
	userEvent = None
	# check which event is the user most interested to visit out of a list of events
	for event in artistInfo.artistEventList:
		if event.eventVenueName == userVenue:
			userEvent = event

	# now that we have the event the user is most likely to visit we now come up with the list of best 50 hotels in the region near the hotel
	eventHotelInfoObjects = []

	for event in artistInfo.artistEventList:

		if userEvent.eventVenueName == event.eventVenueName:

			# these are the checkin and checkout dates of an event for the user
			checkInDate = event.eventDateTime.date().strftime('%Y%m%d')
			checkOutDate = (event.eventDateTime + datetime.timedelta(days=1)).date().strftime('%Y%m%d')

			# get the hotel info corresponding to an event in json
			hotelInfoJsonResponse = urllib2.urlopen('http://www.priceline.com/api/hotelretail/listing/v3/' + event.eventCityLatitude + ',' + event.eventCityLongitude + '/' + checkInDate + '/' + checkOutDate + '/' + '1' + '/' + '50?offset=0')
			hotelInfoJsonResponseDict = json.load(hotelInfoJsonResponse)	

			# iterate over all the key value pairs in the 'hotels' field's value
			for value in hotelInfoJsonResponseDict['hotels'].values():
				hotelInfoObject = HotelInfo(value)
				eventHotelInfoObjects.append(hotelInfoObject)

			break;

	for hotels in eventHotelInfoObjects:
		print hotels.hotelName
