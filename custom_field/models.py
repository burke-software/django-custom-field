from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes import generic

class CustomField(models.Model):
    """
    A field abstract -- it describe what the field is.  There are one of these
    for each custom field the user configures.
    """
    name = models.CharField(max_length=75)
    content_type = models.ForeignKey(ContentType)
    field_type = models.CharField(
        max_length=1,
        choices=(('t','Text'),('i','Integer'),('b','Boolean (Yes/No)'),),
        default='t')
    default_value = models.CharField(
        max_length=255,
        blank=True,
        help_text="You may leave blank. For Boolean use True or False")

    def get_value_for_object(self, obj):
        return CustomFieldValue.objects.get_or_create(
            field=self,
            object_id=obj.id)[0]

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'content_type')


class CustomFieldValue(models.Model):
    """
    A field instance -- contains the actual data.  There are many of these, for
    each value that corresponds to a CustomField for a given model.
    """
    field = models.ForeignKey(CustomField, related_name='instance')
    value = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return convert_string_of_unknown_type_to_unicode(self.value)

    def save(self, *args, **kwargs):
        super(CustomFieldValue, self).save(*args, **kwargs)
        if not self.content_type:
            self.content_type = self.field.content_type
            self.save()

    def clean(self):
        """ Check value against field_type """
        if self.field.field_type == 'i' and self.value:
            try:
                # the float is to deal with things like '2.0'
                self.value = str(int(float(self.value)))
            except ValueError:
                raise ValidationError(
                    u'{0} must be an integer.'.format(self.field))
        elif self.field.field_type == 'b':
            if (str(self.value).lower() in ["t", "true", 'yes'] or
               self.value is True):
                self.value = "True"
            else:
                self.value = "False"
        return super(CustomFieldValue, self).clean()

    class Meta:
        unique_together = ('field', 'object_id')

def convert_string_of_unknown_type_to_unicode(string):
    try:
        return string.decode('utf-8')
    except UnicodeDecodeError:
        return string.decode("ascii", "ignore")
    except UnicodeEncodeError:
        return string.encode("utf-8")

