#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import models


place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id',
           String(60),
           ForeignKey("places.id"),
           primary_key=True),
    Column('amenity_id',
           String(60),
           ForeignKey("amenities.id"),
           primary_key=True))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship('Review',
                           cascade='all, delete-orphan',
                           backref='place')
    amenities = relationship('Amenity',
                             secondary='place_amenity',
                             viewonly=False,
                             back_populates='place_amenities')

    if models.storage_type != 'db':
        @property
        def reviews(self):
            """Review getter for filestorage."""
            from models.review import Review
            return [review for review in models.storage.all(Review)
                    if self.id == review.place_id]

        @property
        def amenities(self):
            """Amenities getter for filestorage."""
            return [amenity for amenity in
                    models.storage.all(models.amenity.Amenity).values()
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj=None):
            """ Appends amenity ids to the attribute """
            if (type(obj) is models.amenity.Amenity
               and obj.id not in self.amenity_ids):
                self.amenity_ids.append(obj.id)
