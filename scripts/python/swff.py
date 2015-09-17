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
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


#Get desired flight path and info from user
while True:

	originAirport = raw_input( "\nEnter the airport code of your origin: " )
	destAirport = raw_input( "Enter the airport code of your destination: " )
	departMonth = raw_input( "Enter the month of departure [1 - 12]: " )
	departDay = raw_input( "Enter the day of departure [1 - 31]: " )

	print( "\nYou entered the following information, is this correct? " )
	print( "Departing from: " + originAirport )
	print( "Arriving in: " + destAirport )
	print( "Departure date: " + departMonth + "/" + departDay )
	flightQueryCont = raw_input( "\nEnter 'y' to begin search. Enter any other letter to resubmit request: " )
	
	if flightQueryCont == 'y':
		break
	else:
		continue
		
#Open webrowser and enter in data and perform search
browser = webdriver.Firefox()
browser.get( "https://www.southwest.com/" )

#test = browser.find_element_by_tag_name( "body" )
#test.send_keys( Keys.CONTROL + "t" )
#browser.get( "www.google.com" )

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

#Now on results page. Scrape table data
data = []
for tr in browser.find_elements_by_xpath('//table[@id="faresOutbound"]//tr'):
	tds = tr.find_elements_by_tag_name('td')
	data.append([td.text for td in tds])
print type( data[0] )
#for i in range( 0, len( data ) ):
	#print data[ i ]
#data =  data[ 1 ]
#data = data[ len( data )-1 ]
#data = data.replace( ",", "" )
#data = int( data ) #now have integer number






print( "\n\nDONE" )

































		