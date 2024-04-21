#!/usr/bin/python3
"""Defines a database storage class."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """Database storage class."""
    __engine = None
    __session = None

    def __init__(self):
        """Create a database engine"""
        uname = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        dbname = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        dburl = f'mysql+mysqldb://{uname}:{passwd}@{host}/{dbname}'
        self.__engine = create_engine(dburl, pool_pre_ping=True)

        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def cls_ref(self):
        """Returns a dictionary referencing all valid classes."""
        valid_classes = {'BaseModel': BaseModel,
                         'User': User,
                         'State': State,
                         'City': City,
                         'Amenity': Amenity,
                         'Place': Place,
                         'Review': Review
                         }
        return valid_classes

    def all(self, cls=None):
        """Querry the database on all object depending on the class"""
        new_dict = {}
        querry_list = [cls.__name__] if cls else [*self.cls_ref()]
        for _cls in querry_list:
            objs = self.__session.query(self.cls_ref()[_cls]).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add new object obj to the current database session"""
        if isinstance(obj, BaseModel):
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        try:
            self.__session.commit()
        except Exception as e:
            print(f'Error: {e}')

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create tables from the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """remove a scoped session"""
        self.__session.remove()
