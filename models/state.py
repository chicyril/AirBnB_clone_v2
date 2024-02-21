#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """Defines a State class for table and instance."""
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship('City',
                          backref='state',
                          cascade='all, delete-orphan')

    if models.storage_type != 'db':
        @property
        def cities(self):
            """get all cities with the current state id
            from filestorage
            """
            return [city for key, city in models.storage.all(City).items()
                    if city.state_id == self.id]
