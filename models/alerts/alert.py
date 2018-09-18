import uuid
import datetime
import smtplib
from common.database import Database
from models.alerts import constants as AlertConstants
from models.items.item import Item



class Alert(object):
    def __init__(self, user_email, price_limit, item_id, last_checked=None,active=True, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.last_checked = datetime.datetime.now() if last_checked is None else last_checked
        self.user_email = user_email
        self.price_limit = price_limit
        self.item_id = item_id
        self.item = Item.get_by_id(self.item_id)
        self.active = active


    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email, self.item, self.price_limit)


    # This method send the email to the client using API key with SMTP sever

    def send(self):
        # ALTERED EMAIL SENDING CODE
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(AlertConstants.EMAIL_ADDR, AlertConstants.PASSWORD)
        message = 'Subject: Price Limit reached for {}\n\n"we have got a deal for the item {} and here is the link to Store {}'.format(self.item.name, self.item.name,self.item.url)
        server.sendmail(AlertConstants.EMAIL_ADDR, self.user_email, message)
        server.close()



        # client = Client(AlertConstants.ACCOUNT_SID, AlertConstants.AUTH_TOKEN)
        # client.messages.create(from_="+12526801615",
        #                        to="+923072718623",
        #                        body=".                      Hey..! We have got a Deal for you :)  Price Limit is reached for item")


# ORIGINAL EMAIL SENDING CODE
        # requests.post(
        #     AlertConstants.URL, auth=("api",AlertConstants.API_KEY),
        #     data={
        #         "from":AlertConstants.FROM,
        #         "to":self.user.email,
        #         "subject":"price limit reached for {}".format(self.item),
        #         "text":"we have got a deal for the item {} and here is the link (link)".format(self.item)
        #     }
        # )

    # Check if the Time of update is reached
    # and then return data for further process
    @classmethod
    def find_needing_update(cls, min_since_updated=AlertConstants.ALERT_TIMEOUT):
        last_time_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=min_since_updated)
        return [cls(**ele) for ele in Database.find(AlertConstants.COLLECTION,{"last_checked":{"$lte": last_time_updated_limit},"active":True})]

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION,{"_id":self._id},self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email":self.user_email,
            "item_id": self.item_id,
            "active" : self.active
        }


    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.now()
        self.save_to_mongo()
        self.item.save_to_mongo()
        return self.item.price

    def send_email_if_price_reachced(self):
        if float(self.item.price) < float(self.price_limit):
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {"user_email":user_email})]

    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {"_id": alert_id}))

    def deactivate(self):
        self.active = False
        self.save_to_mongo()


    def activate(self):
        self.active = True
        self.save_to_mongo()


    def remove(self):
        Database.remove(AlertConstants.COLLECTION,{"_id":self._id})
