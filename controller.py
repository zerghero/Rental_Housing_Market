import os
#change working directory to what it should be
import scrape_zip_excel as excel
import zipLibrary as z
import scrapeToSQL as database

#use the 'scrape_zip_excel' module to scrape housing market data to the datafile csv in the data folder.
#use the scrapeToSQL module if you have a database set up which you would like to scrape the data to.  this will involve further conifguration on your end.
# the zipLibrary module has a list of all the zip codes for cities with more than 50,000 people in the United states.

# Here is an example on line 12 using the library to scrape all the zip codes for Boston to an excel file.
# excel.scrape_zips(z.boston_zips)

#here is an example to scrape all of the cities in the U.S. with more than 50K people.
#excel.scrape_zips(z.bigscrape)

#here is an example of just scraping a custom zip code list
#excel.scrape_zips(['02139','02108'])

#to configure scraping to a database, see the readme documetion.