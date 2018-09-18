from passlib.hash import pbkdf2_sha512
import re

class Utils(object):


    #This method will check email validity
    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hashed_password(password):
        """
        double encrypt the password
        :param password: hashed password in a double hashed password
        :return: double encrypted password
        """

        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def hash_password(password, hashed_password):
        """
        Check that the password the user send matches that of database.
        The database password is encrypted more than the user's password at this         stage .
        :param password: sha512_hashed
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if the password matches , Otherwise False
        """
        return pbkdf2_sha512.verify(password, hashed_password)

















