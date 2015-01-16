# coding=utf-8

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import TestCase
from .models import (
    CustomField, CustomFieldValue,convert_string_of_unknown_type_to_unicode
    )
from .custom_field import CustomFieldAdmin


class CustomFieldTest(TestCase):
    def setUp(self):
        custom_field_ct = ContentType.objects.get(app_label="custom_field",
                                                  model="customfield")
        self.custom_field = CustomField.objects.create(
            name="test_field",
            content_type=custom_field_ct,
            field_type="i",
        )
        user_custom_field_ct = ContentType.objects.get(app_label="auth",
                                                  model="user")
        self.user_custom_field = CustomField.objects.create(
            name="test_user_field",
            content_type=custom_field_ct,
            field_type="i",
            default_value=42,
        )
        user = User.objects.create_user('temporary', 'temporary@gmail.com',
                                        'temporary')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.client.login(username='temporary', password='temporary')

    def test_validation(self):
        custom_value = CustomFieldValue.objects.create(
            field=self.custom_field,
            value='5.0',
            object_id=self.custom_field.id,
        )
        custom_value.clean()
        custom_value.save()
        self.assertEquals(custom_value.value, '5')
        custom_value.value = 'fdsf'
        try:
            custom_value.clean()
            self.fail('Was able to save string as custom integer field!')
        except ValidationError:
            pass

    def test_admin(self):
        from django.contrib import admin
        response = self.client.get('/admin/custom_field/customfield/1/')
        self.assertContains(response, '42', count=2)
        response = self.client.get('/admin/custom_field/customfield/1/') 
        # Make sure we aren't adding it on each get
        self.assertContains(response, '42', count=2)

    def test_crazy_string_that_should_be_unicode_but_isnt(self):
        chars = "ȧƈƈḗƞŧḗḓ ŧḗẋŧ ƒǿř ŧḗşŧīƞɠ"
        decoded_chars = convert_string_of_unknown_type_to_unicode(chars)
        self.assertEqual(type(decoded_chars), unicode)

    def test_crazy_unicode_string(self):
        chars = "ȧƈƈḗƞŧḗḓ ŧḗẋŧ ƒǿř ŧḗşŧīƞɠ"
        decoded_chars = convert_string_of_unknown_type_to_unicode(chars)
        self.assertEqual(type(decoded_chars), unicode)

    def test_normal_string(self):
        chars = "Hello World"
        decoded_chars = convert_string_of_unknown_type_to_unicode(chars)
        self.assertEqual(type(decoded_chars), unicode)

    def test_unicode_string(self):
        chars = u'\xa0'
        decoded_chars = convert_string_of_unknown_type_to_unicode(chars)
        self.assertEqual(type(decoded_chars), unicode)

    def test_unicode_string(self):
        chars = u'\kjnsdfjkbnsdjknkijbnskbhdf'
        decoded_chars = convert_string_of_unknown_type_to_unicode(chars)
        self.assertEqual(type(decoded_chars), unicode)


