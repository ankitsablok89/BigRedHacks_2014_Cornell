# import the following libraries to perform parsin of the BandsInTown API data
import re
import sys
import json
import math
import pprint
import oauth2
import urllib
import urllib2
import datetime
import argparse
import dateutil.parser
from operator import itemgetter

# this function is used to compute the distance between 2 latitude/longitude pairs relative to earth's radius
def computeDistanceFromCoordinates(lat1,long1,lat2,long2):
		
	# convert latitude and longitude to spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
    	
    # angles of the 2 co-ordinates in radians based on latitudes of 2 points
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # this equation computes the spherical distance
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # this returns the distance of lat2,long2 from lat1,long1 in miles - http://www.johndcook.com/lat_long_details.html
    return arc*3960

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
	artistName = raw_input("ENTER THE ARTIST WHOSE CONCERT YOU ARE INTERESTED IN VISITING : ")
	artistInfo = ArtistInfo(artistName)
	
	print artistName + " IS PLAYING AT THE FOLLOWING VENUES -: \n"

	for event in artistInfo.artistEventList:
		print event.eventVenueName

	# now we prompt the user to enter the venue where he wants to see the band playing
	userVenue = raw_input("\nENTER THE VENUE THAT INTERESTS YOU THE MOST : ")

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

	# this is a list of all hotels sorted in descending order of a cumulative score which is calculated as per the following customer patterns observed - http://corp.marketmetrix.com/how-guests-select-hotels-around-the-world-global-results/
	hotelListSortedOnCumulativeScore = []
	for hotel in eventHotelInfoObjects:
		# first evaluate the distance of the hotel from the event that the customer is trying to visit
		distanceOfHotelFromVenue = computeDistanceFromCoordinates(float(unicode(userEvent.eventCityLatitude)), float(unicode(userEvent.eventCityLongitude)), hotel.latitude, hotel.longitude)

		# here we compute a cumulative score that is used to best match a hotel to a customer
		hotelCumulativeScore = 0.04*distanceOfHotelFromVenue + 0.302*hotel.locationScore + 0.157*hotel.pwysRate + 0.033*hotel.starRating + 0.055*hotel.originalRank + 0.075*hotel.diningScore + 0.119*hotel.overallRatingScore		
		
		# append the tuple of (hotelCumulativeScore, hotel) to the hotelListSortedOnCumulativeScore list
		hotelListSortedOnCumulativeScore.append((hotelCumulativeScore, hotel))

	# sort the hotelListSortedOnCumulativeScore based on the descending order of scores and print them
	hotelListSortedOnCumulativeScore.sort(key = itemgetter(0), reverse=True)
	print '\nTHE LIST OF HOTELS THAT YOU MIGHT WANT TO CONSIDER IN A RANKED ORDER IS AS FOLLOWS -: \n'
	for (cumulativeScore, hotel) in hotelListSortedOnCumulativeScore:
		print hotel.hotelName

	# ask the user if he wants to know more about a specific hotel or not
	specificHotelDetails = raw_input("ENTER THE NAME OF THE HOTEL ABOUT WHICH YOU WOULD LIKE TO KNOW MORE : ")
	
		
