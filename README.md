# Rental_Housing_Market
This project allows users to collect information from rental market websites regarding the longitude, latitude, cost, sqft, # of bathrooms and bedrooms, zip code, state and address.  Data can be scraped in two ways, either directly to 'datafile.csv' housed in the data folder or to a database.  

To create  simple SQLite database that will work with the 'scrapeToSQL' module, deploy the 'createSQLite.py' file in the 'data' folder.

To use this program, run 'controller.py' with a list of the zip codes you would like to scrape.  The 'ZipLibrary.py' lists all of the zip codes in the U.S. with cities that have over 50,000 residents, broken down by state.

This program is written in Python V 2.7.
