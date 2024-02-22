#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.


Unittest classes:
   TestFileStorage_instantiation
   TestFileStorage_methods
"""
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
import models
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import os


class TestFileStorageInstantiation(unittest.TestCase):
    """Unittests for testing filestorage class instantiation."""

    def test_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_private_class_attributes(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storageObj_type(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorageMethods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        b = BaseModel()
        u = User()
        s = State()
        p = Place()
        c = City()
        a = Amenity()
        r = Review()
        models.storage.new(b)
        models.storage.new(u)
        models.storage.new(s)
        models.storage.new(p)
        models.storage.new(c)
        models.storage.new(a)
        models.storage.new(r)
        self.assertIn(f"BaseModel.{b.id}", models.storage.all().keys())
        self.assertIn(b, models.storage.all().values())
        self.assertIn(f"User.{u.id}", models.storage.all().keys())
        self.assertIn(u, models.storage.all().values())
        self.assertIn(f"State.{s.id}", models.storage.all().keys())
        self.assertIn(s, models.storage.all().values())
        self.assertIn(f"City.{c.id}", models.storage.all().keys())
        self.assertIn(c, models.storage.all().values())
        self.assertIn(f"Place.{p.id}", models.storage.all().keys())
        self.assertIn(p, models.storage.all().values())
        self.assertIn(f"Amenity.{a.id}", models.storage.all().keys())
        self.assertIn(a, models.storage.all().values())
        self.assertIn(f"Review.{r.id}", models.storage.all().keys())
        self.assertIn(r, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 199)

    def test_new_with_number(self):
        with self.assertRaises(AttributeError):
            models.storage.new(9)

    def test_save(self):
        b = BaseModel()
        u = User()
        s = State()
        c = City()
        p = Place()
        a = Amenity()
        v = Review()
        models.storage.new(b)
        models.storage.new(u)
        models.storage.new(s)
        models.storage.new(c)
        models.storage.new(p)
        models.storage.new(a)
        models.storage.new(v)
        models.storage.save()
        txt = ""
        with open("file.json", "r") as f:
            txt = f.read()
            self.assertIn(f"BaseModel.{b.id}", txt)
            self.assertIn(f"User.{u.id}", txt)
            self.assertIn(f"State.{s.id}", txt)
            self.assertIn(f"Place.{p.id}", txt)
            self.assertIn(f"City.{c.id}", txt)
            self.assertIn(f"Amenity.{a.id}", txt)
            self.assertIn(f"Review.{v.id}", txt)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        b = BaseModel()
        u = User()
        s = State()
        c = City()
        p = Place()
        a = Amenity()
        r = Review()
        models.storage.new(b)
        models.storage.new(u)
        models.storage.new(s)
        models.storage.new(c)
        models.storage.new(p)
        models.storage.new(a)
        models.storage.new(r)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn(f"BaseModel.{b.id}", objs)
        self.assertIn(f"User.{u.id}", objs)
        self.assertIn(f"State.{s.id}", objs)
        self.assertIn(f"Place.{p.id}", objs)
        self.assertIn(f"City.{c.id}", objs)
        self.assertIn(f"Amenity.{a.id}", objs)
        self.assertIn(f"Review.{r.id}", objs)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
