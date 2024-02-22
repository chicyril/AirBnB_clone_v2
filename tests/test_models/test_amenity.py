#!/usr/bin/python3
"""unittests for amenity module."""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenityInstantiation(unittest.TestCase):
    """Unittests for testing Amenity instances."""

    def test_with_no_args(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_instance_in_objects_attr(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_attr(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_attr(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_attr(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name(self):
        am = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", am.__dict__)

    def test_amenities_unique_ids(self):
        am1 = Amenity()
        am2 = Amenity()
        self.assertNotEqual(am1.id, am2.id)

    def test_different_created_at(self):
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        self.assertLess(am1.created_at, am2.created_at)

    def test_different_updated_at(self):
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        self.assertLess(am1.updated_at, am2.updated_at)

    def test_str_representation(self):
        dtme = datetime.today()
        dt_repr = repr(dtme)
        a = Amenity()
        a.id = "123456"
        a.created_at = a.updated_at = dtme
        amstr = a.__str__()
        self.assertIn("[Amenity] (123456)", amstr)
        self.assertIn("'id': '123456'", amstr)
        self.assertIn("'created_at': " + dt_repr, amstr)
        self.assertIn("'updated_at': " + dt_repr, amstr)

    def test_unused_args(self):
        a = Amenity(None)
        self.assertNotIn(None, a.__dict__.values())

    def test_instantiation(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_kwargs(self):
        """instantiation with kwargs test method"""
        dtme = datetime.today()
        dt_iso = dtme.isoformat()
        am = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(am.id, "345")
        self.assertEqual(am.created_at, dtme)
        self.assertEqual(am.updated_at, dtme)


class TestAmenitySave(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def testSaves(self):
        a = Amenity()
        sleep(0.05)
        first_updated_at = a.updated_at
        a.save()
        second_updated_at = a.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        a.save()
        self.assertLess(second_updated_at, a.updated_at)

    def test_save_with_arg(self):
        a = Amenity()
        with self.assertRaises(TypeError):
            a.save(None)

    def test_save_updated_file(self):
        a = Amenity()
        a.save()
        amn = "Amenity." + a.id
        with open("file.json", "r") as f:
            self.assertIn(amn, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        a = Amenity()
        self.assertIn("id", a.to_dict())
        self.assertIn("created_at", a.to_dict())
        self.assertIn("updated_at", a.to_dict())
        self.assertIn("__class__", a.to_dict())

    def test_to_dict(self):
        am = Amenity()
        self.assertNotEqual(am.to_dict(), am.__dict__)

    def test_to_dict_contains_added_attributes(self):
        a = Amenity()
        a.middle_name = "Holberton"
        a.my_number = 98
        self.assertEqual("Holberton", a.middle_name)
        self.assertIn("my_number", a.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        a = Amenity()
        a_dict = a.to_dict()
        self.assertEqual(str, type(a_dict["id"]))
        self.assertEqual(str, type(a_dict["created_at"]))
        self.assertEqual(str, type(a_dict["updated_at"]))

    def test_to_dict_output(self):
        d = datetime.today()
        amen = Amenity()
        amen.id = "123456"
        amen.created_at = amen.updated_at = d
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': d.isoformat(),
            'updated_at': d.isoformat(),
        }
        self.assertDictEqual(amen.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        am = Amenity()
        with self.assertRaises(TypeError):
            am.to_dict(None)


if __name__ == "__main__":
    unittest.main()
