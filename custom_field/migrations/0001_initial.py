# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomField",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=75)),
                (
                    "field_type",
                    models.CharField(
                        default=b"t",
                        max_length=1,
                        choices=[
                            (b"t", b"Text"),
                            (b"i", b"Integer"),
                            (b"b", b"Boolean (Yes/No)"),
                        ],
                    ),
                ),
                (
                    "default_value",
                    models.CharField(
                        help_text=b"You may leave blank. For Boolean use True or False",
                        max_length=255,
                        blank=True,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        to="contenttypes.ContentType", on_delete=models.CASCADE
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="CustomFieldValue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("value", models.CharField(max_length=255, null=True, blank=True)),
                ("object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        blank=True,
                        to="contenttypes.ContentType",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "field",
                    models.ForeignKey(
                        related_name="instance",
                        to="custom_field.CustomField",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name="customfieldvalue", unique_together=set([("field", "object_id")]),
        ),
        migrations.AlterUniqueTogether(
            name="customfield", unique_together=set([("name", "content_type")]),
        ),
    ]
