# coding=utf-8

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import TestCase
from .models import CustomField, CustomFieldValue
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

    def create_and_test_custom_field_unicode_method(self, char_string):
        custom_field = CustomFieldValue.objects.create(
            field = self.custom_field,
            value = char_string,
            object_id = self.custom_field.id
        )
        self.assertEqual(type(custom_field.__unicode__()),str)

    def test_crazy_string_that_should_be_unicode_but_isnt(self):
        chars = "ȧƈƈḗƞŧḗḓ ŧḗẋŧ ƒǿř ŧḗşŧīƞɠ"
        self.create_and_test_custom_field_unicode_method(chars)

    def test_crazy_unicode_string(self):
        chars = "ȧƈƈḗƞŧḗḓ ŧḗẋŧ ƒǿř ŧḗşŧīƞɠ"
        self.create_and_test_custom_field_unicode_method(chars)

    def test_normal_string(self):
        chars = "Hello World"
        self.create_and_test_custom_field_unicode_method(chars)

    def test_unicode_string(self):
        chars = u'\xa0'
        self.create_and_test_custom_field_unicode_method(chars)


