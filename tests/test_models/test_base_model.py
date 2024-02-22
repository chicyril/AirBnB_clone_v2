#!/usr/bin/python3
"""Unittest module for base_model module."""
import unittest
from models.base_model import BaseModel
from datetime import datetime
import inspect


class TestBaseModelInstance(unittest.TestCase):
    """Test class for BaseModel instance."""

    def setUp(self):
        """Setup action."""
        self.b = BaseModel()

    def test_doc_str(self):
        """Test for the module's doc string."""
        self.assertIsNotNone(self.b.__doc__)
        self.assertTrue(len(self.b.__doc__.split()) > 1)
        self.methods = inspect.getmembers(self.b, inspect.isfunction)
        for method in self.methods:
            self.assertIsNotNone(method.__doc__)
            self.assertTrue(len(method.__doc__.split()) > 1)

    def test_instance_type(self):
        """Test the type of a BaseModel instance."""
        self.assertEqual(type(self.b), BaseModel)

    def test_instance_attr_type(self):
        """Test the type of a BaseModel instance attribute."""
        self.assertEqual(type(self.b.id), str)
        self.assertEqual(type(self.b.created_at), datetime)
        self.assertEqual(type(self.b.updated_at), datetime)

    def test_datetimeType_attr(self):
        """Test instance's datetime-type attribute."""
        now = datetime.now()
        self.assertEqual(self.b.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
                         self.b.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertTrue(self.b.created_at <= now and self.b.updated_at <= now)
        b2 = BaseModel()
        self.assertTrue(self.b.created_at < b2.created_at and
                        self.b.updated_at < b2.updated_at)
        self.b.save()
        self.assertNotEqual(self.b.created_at, self.b.updated_at)

    def test_uuidType_attr(self):
        """Test id instance attribute."""
        self.assertRegex(self.b.id,
                         '^[0-9a-f]{8}-[0-9a-f]{4}'
                         '-[0-9a-f]{4}-[0-9a-f]{4}'
                         '-[0-9a-f]{12}$')
        b2 = BaseModel()
        self.assertNotEqual(self.b.id, b2.id)

    def test_str(self):
        """Test the output of the str method"""
        out = f'[{self.b.__class__.__name__}] ({self.b.id}) {self.b.__dict__}'
        self.assertEqual(str(self.b), out)

    def test_save(self):
        """Test save method"""
        old_created_at = self.b.created_at
        old_updated_at = self.b.updated_at
        self.b.save()
        new_created_at = self.b.created_at
        new_updated_at = self.b.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)

    def test_instance_to_dict_keys(self):
        """Test keys of dictionary for json from converting objects."""
        self.b.name = "Holberton"
        self.b.my_number = 89
        dico = self.b.to_dict()
        keys = ["id", "created_at", "updated_at",
                "name", "my_number", "__class__"]
        for key in keys:
            self.assertIn(key, dico.keys())

    def test_instance_to_dict_vals(self):
        """Test values of dictionary for json from converting objects."""
        dico = self.b.to_dict()
        self.assertEqual(dico['__class__'], type(self.b).__name__)
        self.assertEqual(dico['created_at'],
                         self.b.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f'))
        self.assertEqual(dico['updated_at'],
                         self.b.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f'))


if __name__ == "__main__":
    unittest.main()
