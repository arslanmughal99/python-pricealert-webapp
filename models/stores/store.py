from common.database import Database
import uuid
from models.stores import constant as StoreConstants
import models.stores.errors as StoreErrors


class Store(object):
	def __init__(self, name, url_prefix, tag_name, query, _id=None):
		self.name = name
		self.url_prefix = str(url_prefix)
		self.tag_name = tag_name
		self.query = query
		self._id = uuid.uuid4().hex if not None else _id



	def __repr__(self):
		return "<Store {}>".format(self.name)


	def json(self):
		return {
			"name":self.name,
			"tag_name":self.tag_name,
			"url_prefix":self.url_prefix,
			"query":self.query,
			"_id": self._id
		}

	def save_to_mongo(self):
		Database.insert(StoreConstants.COLLECTION, self.json())

	@classmethod
	def get_by_id(cls, _id):
		return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id":_id}))


	@classmethod
	def get_by_name(cls, store_name):
		cls(**Database.find_one(StoreConstants.COLLECTION, {"name":store_name}))


	@classmethod
	def get_by_url_prefix(cls,url_prefix):
		return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix":{"$regex":"^{}".format(url_prefix)}}))

	@classmethod
	def get_by_url(cls, url):
		try:
			for i in range(0,len(url)+1):
				store_data = cls.get_by_url_prefix(url[:i+13])
				i += 1
				store = store_data
				return store



		except:
			raise StoreErrors.StoreNotFoundException("The store you are trying to reach could'nt find :(")

