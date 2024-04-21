#!/usr/venv/bin/python
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime,
                        nullable=False,
                        default=lambda: func.utcnow())
    updated_at = Column(DateTime,
                        nullable=False,
                        default=lambda: func.utcnow(),
                        onupdate=lambda: func.utcnow())

    def __init__(self, **kwargs):
        """Instatntiates a new model"""
        if kwargs:
            if 'id' in kwargs:
                del kwargs['__class__']
                kwargs['updated_at'] = (datetime
                                        .strptime(kwargs['updated_at'],
                                                  '%Y-%m-%dT%H:%M:%S.%f'))
                kwargs['created_at'] = (datetime
                                        .strptime(kwargs['created_at'],
                                                  '%Y-%m-%dT%H:%M:%S.%f'))

            else:
                self.id = str(uuid.uuid4())
                self.created_at = self.updated_at = datetime.now()

            self.__dict__.update(kwargs)

        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Save new instance or it's update to storage."""
        if (f'{self.__class__.__name__}.{self.id}' in
           models.storage.all(self.__class__)):
            self.updated_at = datetime.now()
        else:
            models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        if '_sa_instance_state' in self.__dict__:
            del self.__dict__['_sa_instance_state']
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """Delete and instance from storage."""
        models.storage.delete(self)
