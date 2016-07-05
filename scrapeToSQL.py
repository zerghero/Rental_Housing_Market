from datetime import datetime
import os
os.getcwd()

import sqlite3

import requests
from bs4 import BeautifulSoup as bs
import csv
import time
import os
import zipLibrary as zl

class Property():
	def __init__(self,xml):
		self.latitude = str(find_by_itemprop(xml,'latitude'))
		self.longitude = str(find_by_itemprop(xml,'longitude'))
		self.address = str(find_by_itemprop_text(xml,'streetAddress')).replace(',','')
		self.state = str(find_by_itemprop_text(xml, "addressRegion")).replace(',','')
		self.zip = str(find_by_itemprop_text(xml,'postalCode')).replace(',','')
		self.city = str(find_by_itemprop_text(xml,'addressLocality')).replace(',','')
		self.fullAddress = str(self.address + ', '+ self.city +', '+ self.state + ','+ self.zip)
		if xml.find(class_ = 'listBordered mbn') is not None:
			self.construct_big(xml)
		else:
			self.construct_simple(xml)
		#self.for_sale = if 'For Sale' in str(xml.find(class_='h5 typeEmphasize srpTitleLocation')):
		      #self.for_sale = True
		  #else:
		   #   False

	def construct_simple(self,xml):
		self.type = 'single'
		try:
		  self.price = str((xml.find(class_ = 'lastCol').find_all('span')[1].text.replace('$','').replace(',','')))
		except UnicodeEncodeError:
		    self.price = None
		try:
		    self.bedrooms = str(((xml.find(class_ = 'cols3').find('small').text.split(' ')[0])))
		except ValueError:
		    self.bedrooms = None
		except AttributeError:
		    self.bedrooms = None
		try:
      		    self.bathrooms = str((xml.find(class_ = 'cols3').find_all('small')[1].text.split(' ')[0]))
                except AttributeError:
                    self.bathrooms = None		
		try:
			self.sqft = str((xml.find(class_ = 'cols4').find_all('small')[1].text.split(' ')[0]))
		except IndexError:
			self.sqft = None
		
	def construct_big(self,xml):
		self.type = 'apartment'
		self.units = []
		for apt in xml.find_all('li',class_ = 'pvs mvn pll')[0:-1]:
			self.units.append(Apartment(apt))
		       
	def output(self):
		if self.type == 'single':
			return ((\
			self.latitude,\
			self.longitude,\
			writeNone(self.fullAddress),\
			writeNone(self.zip),\
			writeNone(self.price),\
			writeNone(self.bedrooms),\
			writeNone(self.bathrooms),\
			writeNone(self.sqft), \
			(time.strftime("%d/%m/%Y"))\
			))
		else:
			return (((self.latitude,\
			self.longitude,\
			writeNone(self.fullAddress),\
			writeNone(self.zip),\
			writeNone(apt.price), \
			writeNone(apt.roomType), \
			writeNone(apt.bathrooms),\
			writeNone(apt.sqft), \
			(time.strftime("%d/%m/%Y")))\
			)for apt in self.units)
			
            
class Apartment():
	def __init__(self,xml):
		  self.roomType = str(xml.find(class_ = 'txtL col cols7').text.replace(' ','')).splitlines()[1]
		  self.bathrooms = str(xml.find(class_= 'txtC col cols4').text.split(' ')[0].rstrip())
		  try:
		      self.sqft= str(xml.find_all(class_= 'txtC col cols6')[0].text.replace(' ','').replace('+','').replace('sqft','')).splitlines()[1]
		  except TypeError:
		          self.sqft = None
		  try:
		      self.price = str(xml.find_all(class_= 'txtC col cols6')[1].text.replace('$','')\
		      .replace('+/mo','').replace('/mo','').replace('+','').rstrip().replace(' ','')).splitlines()[1]
		  except TypeError:
		          self.price = None
		  except IndexError: 
		          self.price = None
		             

def writeNone(val):
	if val is None:
		return ''
	else:
		return val
	
def find_by_itemprop(xml,prop):
	mytag = xml.find(attrs={'itemprop' : prop})
	try:
	    return mytag.get('content')
	except AttributeError:
	    return ''
	    
def find_by_itemprop_text(xml,prop):
    mytag = xml.find(attrs={'itemprop' : prop})
    try:
        return mytag.text
    except AttributeError:
        return ''

def scrape_zips(zips):
    all_pages = []
    pages_completed = 0
    start_time = time.time()
    path = 'data'
    try:
        os.chdir(path)
    except WindowsError or IOError:
        pass
    #connect to sql db
    conn = sqlite3.connect('housing_data.db')
    c = conn.cursor()
    #start parsin some zips
    #### figure out how many pages for each zip code and make a list of all the pages ###
    for z in zips:
        base_page = 'http://www.trulia.com/for_rent/'+str(z)+'_zip/'
        soup = bs(requests.get(base_page).text,'lxml')
        #create list of pages to scrape
        pages = [base_page]
        #create soup of area to look for number of pages
        if len(soup.find_all(class_='srpPagination_list')) == 0:
            pass
        else:
            pages_area = soup.find_all(class_='srpPagination_list')
            try:
                number_of_pages= int(bs(str(pages_area)).find_all('a')[-1].text)
                for i in range(2,number_of_pages+1):
                    pages.append(base_page + str(i)+'_p')
            except IndexError:
                number_of_pages = 1
            all_pages= all_pages + pages
            print('zip: ' + str(z) + ' added to job.  ~Listings: '+ str(number_of_pages*30))
    
    ##### go through each page and make it into some soup ####
    print('total pages to scrape: ' + str(len(all_pages)))
    time.sleep(2)
    for page in all_pages:
        soup = bs(requests.get(page).text,'lxml')
        mylist = soup.find_all(class_='property-data-elem')
        ##### add listings for each page to the database ###
        for listing in mylist:
            home = Property(listing)
            if home.type == 'single':
                c.execute("INSERT INTO rental_data\
                (Longitude, Latitude, Address, Zip, Price, RoomType, Bathrooms, Sqft, Date_Scraped)\
                VALUES(?,?,?,?,?,?,?,?,?)",home.output())
            else:
                for apt in home.units:
                    c.executemany("INSERT INTO rental_data\
                    (Longitude, Latitude, Address, Zip, Price,RoomType, Bathrooms, Sqft, Date_Scraped)\
                    VALUES(?,?,?,?,?,?,?,?,?)",home.output())
          
        print("--- %s seconds ---" % (time.time() - start_time))
        pages_completed +=1
        pages_remaining = len(all_pages)-pages_completed
        print('number of pages remaining: ' + str(pages_remaining)\
        + ' . ~Minuntes to completion: ' + str(pages_remaining*2/60))
    conn.commit()   
    os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))
    return ("--- %s seconds ---" % (time.time() - start_time))
    
 