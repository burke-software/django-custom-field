from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import CustomField, CustomFieldValue


class CustomFieldTest(TestCase):
    def setUp(self):
        custom_field_ct = ContentType.objects.get(
            app_label="custom_field", model="customfield"
        )
        self.custom_field = CustomField.objects.create(
            name="test_field", content_type=custom_field_ct, field_type="i",
        )
        self.user_custom_field = CustomField.objects.create(
            name="test_user_field",
            content_type=custom_field_ct,
            field_type="i",
            default_value=42,
        )
        user = User.objects.create_user("temporary", "temporary@gmail.com", "temporary")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.client.login(username="temporary", password="temporary")

    def test_validation(self):
        custom_value = CustomFieldValue.objects.create(
            field=self.custom_field, value="5", object_id=self.custom_field.id,
        )
        custom_value.clean()
        custom_value.save()
        self.assertEquals(custom_value.value, "5")
        custom_value.value = "fdsf"
        try:
            custom_value.clean()
            self.fail("Was able to save string as custom integer field!")
        except ValidationError:
            pass

    def test_admin(self):
        change_url = reverse("admin:custom_field_customfield_change", args=[1])
        response = self.client.get(change_url)
        self.assertContains(response, "42")
        response = self.client.get(change_url)
        # Make sure we aren't adding it on each get
        self.assertContains(response, "42")
