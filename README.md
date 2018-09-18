/*
*Name : Python Price Alert Web app
*Author : Arslan Mughal
*/

~~

# Price Alert

~~

**Introduction :** 
This is a python flask web app with which you can keep track item price in different Online stores and notify user by email when the price limit is reached for that client all you have to do is just signup and then create new alert for creating alert you have to simple place the URL of the item ,item name and the price at which you want the app to notify you when price reached . 


**requirements :**
*1 : python 3.x
2 : flask
3 : pymongo*
*4: MonoDB*
for database install [**MongoDB**](MongoDB)

================================
**Configurations** 
To set up app first go to models/alerts/constants.py
and place your gmail credentials make sure that before placing credentials you have enable gmail SMTP setting in your gmail account that you gonna be use .

**Runing App:** 
To tun app first make sure that you have installed all the pakages and database before going ahead :)
before runing the app first open a terminal (for windows cmd) and start MongoDB first make sure that mongoDB is running on port **27017** if you are using differnt port than change the configuration in /database/database.py open database.py file in any text edditor and change URI = "mongodb://127.0.0.1:**27017**" port number to your desier port .
After setting up the database open a terminal in source folder location and type this command
root@kali~# **python3 run.py**
this will start the flask server at prot 4545 you can change port by going to run.py file and editing the port to your desier one .
go to your browser localhost:4545 and first register user and than you can login :)


**Adding Stores :**
So On fresh startup there are no stores in the database you have to manually add stores for that run a separate python shell and do the following :
\>> from common.database import Database
\>> from models.stores import store
\>> Database.initialize()
\>> store = Store(name, url_prefix, tag_name, query)
\>> store.save_to_mongo()

**tires:**
**name** == "type the store name in string above :)"
**url_prefix** == "type the url for store in string see the example below"
**tag_name** == "inspect the the element for item in specific store and see what tag is holding price element in html see example below"
**query** == "name of html attibutes with in the tag that is holding the price of item example below"

**forexample :** 
\>>*store = Store("ebay", "http://www.ebay/com", "span", {"itemprop":"price"})*
\>> *store.save_to_mongo()*
and this will add the store to database and like this you can add many stores but since project is not fully developed so there can be issue adding  some stores these are the stores that i have personally tried :
**ebay.com
aliexpress.com
daraz.pk**
and all is working fine with these stores  

