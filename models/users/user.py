import uuid
from common.database import Database
from common.utils import Utils
import models.users.errors as UserErrors
from models.alerts.alert import Alert
from models.users import constant as UserConstant


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    #This method represent Data in specific format
    def __repr__(self):
        return "<User {}>".format(self.email)


    @staticmethod
    def is_login_valid(email, password):
        """This method verify that email and password is valid or not
        password is a ha512 hashed password
        will if valid else false otherwise"""
        user_data = Database.find_one(UserConstant.COLLECTION, {"email": email})
        if user_data is None:
            # Tell the user that their email doesn't exist
            raise UserErrors.UserNotExistError("your User does not exist")
        if not Utils.hash_password(password, user_data['password']):
            # tell user that the password is wrong
            raise UserErrors.IncorrectPasswordError("your password is in correct ")
        return True



    @staticmethod
    def register_user(email, password):
        """
        This method register a user with email and sha-512 password
        :param email: user email
        :param password: already comes in sha_512 encryption
        :return: returns true if the credentials are valid Else return False
        """
        user_data = Database.find_one(UserConstant.COLLECTION, {"email": email})
        if user_data is not None:
            #Tell user that they are already registered
            raise UserErrors.UserAlreadyExist("The email you are trying to register already exist")
        if not Utils.email_is_valid(email):
            # Tell that there email is not valid
            raise UserErrors.InvalidEmail("The email your are trying to register is not valid")
        User(email, Utils.hashed_password(password)).save_to_db()
        return True

        # tHIS method returns user Data

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    #This Method Save data to MongoDB
    def save_to_db(self):
        Database.insert(UserConstant.COLLECTION, self.json())

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstant.COLLECTION,{"email":email}))


    def get_alerts(self):
        return Alert.find_by_user_email(self.email)









