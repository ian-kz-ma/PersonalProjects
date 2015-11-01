#Looks for available flights given a starting airport and multiple destination airports, sorts results by mileage points for
#	southwest flights only
#Current version supports multiple airports, displays results in table format. User must know airport code before hand.
#Submitted airport codes will be checked with database.

import sys
import urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def loadAiportCodes( url ):
	airportCodes = urllib2.urlopen( url )
	airportCodes = airportCodes.read()
	airportCodes = airportCodes.split()
	return airportCodes

	
def initFlightData( flightDict, destinationList, airportCodes ):
	while True:
		destAirport = ""
		allValid = True
		del destinationList[ : ]
		
		flightDict[ "originAirport" ] = raw_input( "\nEnter the airport code of your origin: " ).upper()
		if flightDict[ "originAirport" ] not in airportCodes:
			print( "The code %s does not exist. Please re-enter your origin code." % ( flightDict[ "originAirport" ] ) )
			continue
		print( "Enter the airport code(s) of your destination(s). Press enter after each code, submit 'done' when finished: " )
		
		while destAirport != "DONE":
			destAirport = raw_input().upper()
			if ( destAirport not in airportCodes and destAirport != "DONE" ):
				print "The code %s does not exist. Please re-enter your airport codes." % ( destAirport )
				allValid = False
				break
			destinationList.append( destAirport )
		if allValid == False:
			continue
		destinationList.pop()
				
		flightDict[ "departMonth" ] = raw_input( "Enter the month of departure [1 - 12]: " )
		flightDict[ "departDay" ] = raw_input( "Enter the day of departure [1 - 31]: " )
		print( "\nYou entered the following information, is this correct? " )
		print( "Departure date: %s / %s" % ( flightDict[ "departMonth" ], flightDict[ "departDay" ] ) )
		print( "Departing from: %s" % ( flightDict[ "originAirport" ]) )
		print( "Comparing the following arrival airport costs (points): "),
		for i in range( 0, len( destinationList ) ):
			print( destinationList[ i ] + " " ),
		flightQueryCont = raw_input( "\nEnter 'y' to begin search. Enter any other letter to resubmit request: " )
		if flightQueryCont == 'y':
			break
		else:
			continue

			
def scrapeResults( flightPointCosts, htmlTableData, browser, destAirport, resultsDict ):
	#Cost in points is always last element where list is of size > 2
	#Definetely a better way to do this....
	for tr in browser.find_elements_by_xpath('//table[@id="faresOutbound"]//tr'):
		tds = tr.find_elements_by_tag_name('td')
		htmlTableData.append([td.text for td in tds])
	for cell in htmlTableData:
		if len( cell ) > 2:
			value = cell[ len( cell ) - 1 ]
			if( any( i.isdigit() for i in value ) ):
				flightPointCosts.append( int( value.replace( "," , "" ) ) )
			else:
				continue
	flightPointCosts.sort()
	if flightPointCosts[ 0 ] < resultsDict[ "lowestFareCost" ]:
		resultsDict[ "lowestFareAirport" ] = destAirport
		resultsDict[ "lowestFareCost" ] = flightPointCosts[ 0 ]

	
def inputFlightData( flightDict, destAirport, browser ):
	tripTypeElem = browser.find_element_by_id( "trip-type-one-way" )
	tripTypeElem.click()

	originAirportElem = browser.find_element_by_id( "air-city-departure" )
	originAirportElem.send_keys( flightDict[ "originAirport" ] )

	destAirportElem = browser.find_element_by_id( "air-city-arrival" )
	destAirportElem.send_keys( destAirport )

	departureElem = browser.find_element_by_id( "air-date-departure" )
	departureElem.clear()
	departureElem.send_keys( flightDict[ "departMonth" ] + "/" + flightDict[ "departDay" ] )

	priceTypeElem = browser.find_element_by_id( "price-type-points" )
	priceTypeElem.click()

	submitElem = browser.find_element_by_id( "jb-booking-form-submit-button" )
	submitElem.click()
	
	
def displayResult( resultsDict ):
	print "\n\nCheapest destination airport: %s @ %s points" % ( resultsDict[ "lowestFareAirport" ].upper(), resultsDict[ "lowestFareCost" ] )
	
	
def main():
	url = "https://raw.githubusercontent.com/ian-kz-ma/PersonalProjects/master/scripts/dataSets/airport-codes.txt"
	destinationList = []
	airportCodes = []
	flightDict = { "originAirport" : "", "departDay" : "", "departMonth" : "" }
	resultsDict = { "lowestFareAirport" : "", "lowestFareCost" : 999999 }
	airportCodes = loadAiportCodes( url )	
	initFlightData( flightDict, destinationList, airportCodes )	

	print "\nCalculating cost(s) in points...\n"
	print flightDict[ "originAirport" ].upper() + " ->:   ",
	browser = webdriver.Firefox()
	for destAirport in destinationList:
		htmlTableData = []
		flightPointCosts = []
		browser.get( "https://www.southwest.com/" )	
		inputFlightData( flightDict, destAirport, browser )
		scrapeResults( flightPointCosts, htmlTableData, browser, destAirport, resultsDict )
		if destAirport == destinationList[ 0 ]:
			print destAirport.upper() + "  | ",
			for elem in flightPointCosts:
				print str( elem ) + " | ",
		else:
			print "\n           " + destAirport.upper() + "  | ",
			for elem in flightPointCosts:
				print str( elem ) + " | ",
		if destAirport != destinationList[ -1 ]:
			tabGen = browser.find_element_by_tag_name( "body" )
			tabGen.send_keys( Keys.CONTROL + "t" )
			
	displayResult( resultsDict )
	print "\n\nDONE\n\n"

main()


		