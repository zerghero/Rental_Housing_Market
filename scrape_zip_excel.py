import requests
from bs4 import BeautifulSoup as bs
import html5lib
import csv
import time
import os
import zipLibrary as z

class Property():
	def __init__(self,xml):
		self.latitude = str(find_by_itemprop(xml,'latitude'))
		self.longitude = str(find_by_itemprop(xml,'longitude'))
		self.address = str(find_by_itemprop_text(xml,'streetAddress'))
		self.zip = str(find_by_itemprop_text(xml,'postalCode'))
		self.city = str(find_by_itemprop_text(xml,'addressLocality'))
		self.fullAddress = str(self.address + ' '+ self.city +' '+ self.zip).replace(',','')
		if xml.find(class_ = 'listBordered mbn') is not None:
			self.construct_big(xml)
		else:
			self.construct_simple(xml)

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
			return [[self.latitude,self.longitude,writeNone(self.fullAddress),writeNone(self.zip), writeNone(self.price),writeNone(self.bedrooms),writeNone(self.bathrooms),writeNone(self.sqft), (time.strftime("%m/%d/%Y"))]]
		else:
			return [([self.latitude,self.longitude,writeNone(self.fullAddress),writeNone(self.zip), writeNone(apt.price), writeNone(apt.roomType), writeNone(apt.bathrooms),writeNone(apt.sqft), (time.strftime("%m/%d/%Y"))]) for apt in self.units]
            
class Apartment():
	def __init__(self,xml):
		  self.roomType = str(xml.find(class_ = 'txtL col cols7').text.replace(' ','')).splitlines()[1]
		  self.bathrooms = str(xml.find(class_= 'txtC col cols4').text.split(' ')[0].rstrip())
		  try:
		      self.sqft= str(xml.find_all(class_= 'txtC col cols6')[0].text.replace(' ','').replace('+','').replace('sqft','')).splitlines()[1]
		  except TypeError:
		          self.sqft = None
		  try:
		      self.price = str(xml.find_all(class_= 'txtC col cols6')[1].text.replace('$','').replace('+/mo','').replace('/mo','').replace('+','').rstrip().replace(' ','')).splitlines()[1]
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



#scrape_city()

def scrape_zips(zips):
    #create a blank list with all of the Property Objects for parsed homes
    #create a list for the CSV outputs
    start_time = time.time()
    #main()
    csv_output =[]
    parsed_homes = []
    file_name = zips[-1]
    for z in zips:
        base_page = 'http://www.trulia.com/for_rent/'+str(z)+'_zip/'
        soup = bs(requests.get(base_page).text,'html5lib')
        #create list of pages to scrape
        pages = [base_page]
        #create soup of area to look for number of pages
        pages_area = soup.find_all(class_='srpPagination_list')
        #create variable for number of pages
        try:
            number_of_pages= int(bs(str(pages_area)).find_all('a')[-1].text)
            #loop over the number of pages to create a list with all of the urls
            for i in range(2,number_of_pages+1):
                pages.append(base_page + str(i)+'_p')
        except IndexError:
            number_of_pages = 1
        print('you are scraping ' + str(number_of_pages)+ ' pages and approximately ' + str(number_of_pages*30) + ' listings for zip: '+ str(z))
        #tracker to see which house we're on.
        listing_comp= 0
        #pageinate through all of the pages and append each listing to the CSV file
        print("--- %s seconds ---" % (time.time() - start_time))
        for page in pages:
            soup = bs(requests.get(page).text,'html5lib')
            mylist = soup.find_all(class_='property-data-elem')
            #if my list is zero, break!!!!!!!!!!!!!!
            listing_comp +=30
            print('listings completed :' + str(listing_comp) + '/' + str(number_of_pages*30))
            for home in mylist:
                parsed_homes.append(Property(home))
                csv_output += Property(home).output()

    #set the working directory to the desktop
    try:
        os.chdir('data')
    except OSError or WindowsError:
        pass
        
    #save a copy of this scrape
    with open('data'+z+'_'+((time.strftime("%d/%m/%Y").replace('/',' ')))+'.csv','wb') as stored_file:
	wr = csv.writer(stored_file)
	wr.writerows(csv_output)
    #append this scrape to the master database
    with open('datafile.csv','a') as core_file:
	wrC = csv.writer(core_file)
	wrC.writerows(csv_output)
    #duration_time = (time.time() - start_time())
    #number_of_listings = number_of_pages*30
    #listings_per_second = number_of_listings%duration_time
    print("--- %s seconds ---" % (time.time() - start_time))
    return ("--- %s seconds ---" % (time.time() - start_time))


