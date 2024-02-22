#!/usr/bin/python3
"""test for file storage"""
import unittest
import pep8
import json
import os
from os import getenv
import MySQLdb
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
class TestDBStorage(unittest.TestCase):
    '''this will test the DBStorage'''

    @classmethod
    def setUpClass(self):
        """set up for test"""
        self.User = getenv("HBNB_MYSQL_USER")
        self.Passwd = getenv("HBNB_MYSQL_PWD")
        self.Db = getenv("HBNB_MYSQL_DB")
        self.Host = getenv("HBNB_MYSQL_HOST")
        self.db = MySQLdb.connect(host=self.Host, user=self.User,
                                  passwd=self.Passwd, db=self.Db,
                                  charset="utf8")
        self.query = self.db.cursor()
        self.storage = DBStorage()
        self.storage.reload()

    @classmethod
    def teardown(self):
        """at the end of the test this will tear it down"""
        self.query.close()
        self.db.close()

    def testall_Dbstorage(self):
        """ test for Dbstorage and alll method
        no element in tables"""
        user = User(email="pas@gh.com",
                    password='yuyy', first_name='jj', last_name='oj')
        state = State(name="California")
        self.storage.new(user)
        self.storage.new(state)
        self.storage.save()
        self.storage.reload()
        text = "select * from users"
        self.query.execute(text)
        count = self.query.fetchall()
        dict = {}
        dict = self.storage.all('User')
        self.assertEqual(len(count), len(dict))
        text = "select * from states"
        self.query.execute(text)
        count = self.query.fetchall()
        dict = self.storage.all('State')
        self.assertEqual(len(count), len(dict))
        text = "SELECT id FROM states WHERE id = 1"
        self.query.execute(text)
        stateid = self.query.fetchone()
        if stateid is not None:
            stateid = stateid[0]
            city = City(state_id=stateid, name="San_Francisco")
            self.storage.new(city)
            self.storage.save()
            self.storage.reload()
            text = "select * from cities"
            self.query.execute(text)
            count = self.query.fetchall()
            dict = self.storage.all('City')
            self.assertEqual(len(count), len(dict))


if __name__ == "__main__":
    unittest.main()
