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

    if models.storage_type == 'db':
        cities = relationship('City',
                              cascade='all, delete-orphan',
                              back_populates='state')

    else:
        @property
        def cities(self):
            """get all cities with the current state id
            from filestorage
            """
            return [city for city in models.storage.all(City).values()
                    if city.state_id == self.id]
