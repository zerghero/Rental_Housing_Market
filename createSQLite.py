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

