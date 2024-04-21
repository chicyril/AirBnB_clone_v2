#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if not cls:
            return self.__class__.__objects.copy()
        return {key: obj for key, obj in self.__class__.__objects.items()
                if key.split('.')[0] == cls.__name__}

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = f'{obj.__class__.__name__}.{obj.id}'
        if key not in self.all(obj.__class__):
            self.__class__.__objects.update({key: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__class__.__file_path, 'w') as f:
            obj_cache = {}
            for key, obj in self.all().items():
                obj_cache[key] = obj.to_dict()
            json.dump(obj_cache, f)

    def cls_ref(self):
        """Returns a dictionary referencing all valid classes."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        valid_classes = {'BaseModel': BaseModel,
                         'User': User,
                         'State': State,
                         'City': City,
                         'Amenity': Amenity,
                         'Place': Place,
                         'Review': Review
                         }
        return valid_classes

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__class__.__file_path, 'r') as f:
                temp = json.load(f)
                for val in temp.values():
                    self.new(self.cls_ref()[val['__class__']](**val))
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            pass

    def delete(self, obj=None):
        """Delete an object 'obj' from storage cache."""
        if obj:
            key = f'{obj.__class__.__name__}.{obj.id}'
            if key in self.all():
                del self.__class__.__objects[key]
                self.save()

    def close(self):
        """Call reload."""
        self.reload()
