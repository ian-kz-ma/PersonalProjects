#Looks for available flights given a starting airport and multiple destination airports, sorts by mileage points
#This script takes: <swff.py> <startingAirPort> <destAirport1>....
#==========================================
#Current version supports only the following:
#One-way 
#points
#one starting airport, one dest airport
#1 adult

import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#Get desired flight path and info from user
destinationList = []
destAirport = ""

while True:
	originAirport = raw_input( "\nEnter the airport code of your origin: " )
	print( "Enter the airport code(s) of your destination(s). Press enter after each code, submit 'done' when finished: " )
	while destAirport  != "done":
		destAirport = raw_input()
		destinationList.append( destAirport )
	destinationList.pop()
	departMonth = raw_input( "Enter the month of departure [1 - 12]: " )
	departDay = raw_input( "Enter the day of departure [1 - 31]: " )

	print( "\nYou entered the following information, is this correct? " )
	print( "Departure date: " + departMonth + "/" + departDay )
	print( "Departing from: " + originAirport )
	print( "Comparing the following arrival airport costs (points): "),
	for i in range( 0, len( destinationList ) ):
		print( destinationList[ i ] + " " ),
	flightQueryCont = raw_input( "\nEnter 'y' to begin search. Enter any other letter to resubmit request: " )
	
	if flightQueryCont == 'y':
		break
	else:
		continue

#Open webrowser and enter in tableData and perform search
browser = webdriver.Firefox()
print "\nCalculating...\n"
print originAirport.upper() + " ->:   ",
for destAirport in destinationList:
	browser.get( "https://www.southwest.com/" )

	tripTypeElem = browser.find_element_by_id( "trip-type-one-way" )
	tripTypeElem.click()

	originAirportElem = browser.find_element_by_id( "air-city-departure" )
	originAirportElem.send_keys( originAirport )

	destAirportElem = browser.find_element_by_id( "air-city-arrival" )
	destAirportElem.send_keys( destAirport )

	departureElem = browser.find_element_by_id( "air-date-departure" )
	departureElem.clear()
	departureElem.send_keys( departMonth + "/" + departDay )

	priceTypeElem = browser.find_element_by_id( "price-type-points" )
	priceTypeElem.click()

	submitElem = browser.find_element_by_id( "jb-booking-form-submit-button" )
	submitElem.click()

	#Now on results page, scrape table 
	tableData = []
	flightPointCosts = []
	for tr in browser.find_elements_by_xpath('//table[@id="faresOutbound"]//tr'):
		tds = tr.find_elements_by_tag_name('td')
		tableData.append([td.text for td in tds])

	#extract only points cost from table data and sort
	for cell in tableData:
		if len( cell ) > 2:
			value = cell[ len( cell ) - 1 ]
			if value == "Sold Out":
				continue
			else:
				flightPointCosts.append( int( value.replace( "," , "" ) ) )
	flightPointCosts = sorted( flightPointCosts )
	
	#display results of currect destination and new tab if more dests exist
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














		