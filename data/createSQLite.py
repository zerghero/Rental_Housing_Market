Skip to content
This repository
Search
Pull requests
Issues
Gist
 @AaronMyran
 Unwatch 1
  Star 0
 Fork 0 AaronMyran/Rental_Housing_Market
 Code  Issues 0  Pull requests 0  Wiki  Pulse  Graphs  Settings
Branch: master Find file Copy pathRental_Housing_Market/createSQLite.py
e28fdb7  4 minutes ago
@AaronMyran AaronMyran create SQLite db
1 contributor
RawBlameHistory     24 lines (18 sloc)  1.01 KB
import sqlite3
conn = sqlite3.connect('housing_data.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

c = conn.cursor()

c.execute('''CREATE TABLE rental_data1
                                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    Longitude TEXT,
                                    Latitude TEXT,
                                    Address TEXT,
                                    Zip TEXT,
                                    Price TEXT,
                                    RoomType TEXT,
                                    Bathrooms TEXT,
                                    Sqft TEXT,
                                    Date_Scraped TEXT,
                                    ts TIMESTAMP)''')
                                    

c.execute("INSERT INTO rental_data(Longitude, Latitude, Address, Zip, Price,RoomType, Bathrooms, Sqft, Date_scraped, ts) VALUES(44, 55,'27 harvard st', '02139', 300, '1 bedrrom', 2, 300, 'march 1', current_time)")
conn.commit()
c.close()

Status API Training Shop Blog About
© 2016 GitHub, Inc. Terms Privacy Security Contact Help
