import sys

from django import forms
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

if sys.version < "3":
    text_type = unicode
else:
    text_type = str


@python_2_unicode_compatible
class CustomField(models.Model):
    """
    A field abstract -- it describe what the field is.  There are one of these
    for each custom field the user configures.
    """

    name = models.CharField(max_length=150)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    field_type = models.CharField(
        max_length=1,
        choices=(
            ("t", "Text"),
            ("a", "Large Text Field"),
            ("i", "Integer"),
            ("f", "Floating point decimal"),
            ("b", "Boolean (Yes/No)"),
            ("m", "Dropdown Choices"),
            ("d", "Date"),
            ("h", "Date Time"),
        ),
        default="t",
    )
    default_value = models.CharField(
        max_length=5000,
        blank=True,
        help_text="You may leave blank. For Boolean use True or False",
    )
    is_required = models.BooleanField(default=False)
    mask = models.CharField(
        max_length=5000,
        blank=True,
        help_text="You may leave blank. For user Jquery Mask, ex: '00/00/0000' for date.",
    )
    field_choices = models.CharField(
        max_length=2000,
        blank=True,
        help_text="List the choices you want displayed, seperated by commas. "
        "This is only valid for Dropdown, Multiple, and Checkbox field types",
    )

    def get_value_for_object(self, obj):
        return CustomFieldValue.objects.get_or_create(field=self, object_id=obj.id)[0]

    def __str__(self):
        return self.name

    def get_form_field(self):
        universal_kwargs = {
            "initial": self.default_value,
            "required": self.is_required,
        }
        if self.field_type == "b":
            return forms.BooleanField(**universal_kwargs)
        elif self.field_type == "i":
            return forms.IntegerField(**universal_kwargs)
        elif self.field_type == "f":
            return forms.FloatField(**universal_kwargs)
        elif self.field_type == "a":
            return forms.CharField(widget=forms.Textarea, **universal_kwargs)
        elif self.field_type == "m":
            choices = self.field_choices.split(",")
            if self.is_required is True:
                select_choices = ()
            else:
                select_choices = (("", "---------"),)
            for choice in choices:
                select_choices = select_choices + ((choice, choice),)
            return forms.ChoiceField(choices=select_choices, **universal_kwargs)
        elif self.field_type == "d":
            return forms.DateField(**universal_kwargs)
        elif self.field_type == "h":
            return forms.DateTimeField(**universal_kwargs)
        return forms.CharField(**universal_kwargs)

    class Meta:
        unique_together = ("name", "content_type")


@python_2_unicode_compatible
class CustomFieldValue(models.Model):
    """
    A field instance -- contains the actual data.  There are many of these, for
    each value that corresponds to a CustomField for a given model.
    """

    field = models.ForeignKey(
        CustomField, related_name="instance", on_delete=models.CASCADE
    )
    value = models.CharField(max_length=5000, blank=True, null=True)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    content_object = fields.GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return text_type(self.value)

    def save(self, *args, **kwargs):
        super(CustomFieldValue, self).save(*args, **kwargs)
        if not self.content_type:
            self.content_type = self.field.content_type
            self.save()

    def clean(self):
        form_field = self.get_form_field()
        form_field.clean(self.value)
        return super(CustomFieldValue, self).clean()

    def get_form_field(self):
        return self.field.get_form_field()

    class Meta:
        unique_together = ("field", "object_id")
