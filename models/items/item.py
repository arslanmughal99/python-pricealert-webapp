import re
import uuid
import requests
from bs4 import BeautifulSoup
from models.stores.store import Store
from models.items import constant as ItemConstants
from common.database import Database


class Item(object):

    def __init__(self, name, url, price=None, _id=None):
        store = Store.get_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.name = name
        self.url = url
        self._id = uuid.uuid4().hex if not None else _id
        self.price = price if not None else self.load_price()



    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)




    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        str_price = soup.find(self.tag_name, attrs=self.query)
        string_price = str_price.text.strip()
        pattern = re.compile("(\d*\.?\d*)")
        match = pattern.findall(string_price)
        join_string = "".join(match)
        price = float(join_string)
        return price

    @classmethod
    def get_by_id(cls,item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION,{"_id":item_id}))


    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION,{"_id":self._id}, self.json())



    def json(self):
        return {"name":self.name,
                "_id":self._id,
                "url":self.url,
                "price":self.load_price()}





