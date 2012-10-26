# encoding: utf-8
from django.forms import ValidationError
from django.test import SimpleTestCase

from ..forms import LVPhoneField
from ..forms import LVIdentityNumberField
from ..forms import LVPostalCodeField


class LVPhoneFieldTestCase(SimpleTestCase):
    def test_valid(self):
        """ test valid phone number """
        field = LVPhoneField()
        self.assertEquals(field.clean("27175629"), "27175629")

    def test_invalid(self):
        """ test invalid phone number """
        field = LVPhoneField()
        self.assertRaises(ValidationError, field.clean, "7175629")


class LVIdentityNumberFieldTestCase(SimpleTestCase):
    def setUp(self):
        self.field = LVIdentityNumberField()

    def test_valid(self):
        """
        test valid identity number field un publicly known identity number of
        Aivars Lembergs
        """
        self.assertEquals(self.field.clean("260953-11667"), "260953-11667")

    def test_with_invalid_date_and_valid_checksum(self):
        """ test with invalid date and valid checksum """
        self.assertRaises(ValidationError, self.field.clean, "300290-11545")

    def test_with_valid_date_and_invalid_checksum(self):
        """ ValidationError on valid date and invalid checksum """
        self.assertRaises(ValidationError, self.field.clean, "251278-11634")

    def test_with_characters_inside(self):
        """ test that identity should fail if it contains characters """
        self.assertRaises(ValidationError, self.field.clean, "abcdef-12145")

    def test_length_validation(self):
        self.assertRaises(ValidationError, self.field.clean, "080690-111711")
        self.assertRaises(ValidationError, self.field.clean, "080690-1177")


class LVPostalCodeFieldTestCase(SimpleTestCase):
    def setUp(self):
        self.field = LVPostalCodeField()

    def test_with_invalid_prefix(self):
        """ all postal code`s have prefix LV """
        self.assertRaises(ValidationError, self.field.clean, "LR-1024")

    def test_with_invalid_code(self):
        """ all postal codes contain prefix, dash and numbers """
        self.assertRaises(ValidationError, self.field.clean, "LV-10S3")

    def test_with_invalid_digits(self):
        """ there is just 4 digits """
        self.assertRaises(ValidationError, self.field.clean, "LV-10244")
        self.assertRaises(ValidationError, self.field.clean, "LV-102")

    def test_valid(self):
        self.assertEqual(self.field.clean("LV-1024"), "LV-1024")
